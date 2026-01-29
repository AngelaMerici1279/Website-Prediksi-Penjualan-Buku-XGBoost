from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from sqlalchemy import create_engine # Library baru untuk koneksi DB
import datetime
import os

app = Flask(__name__)
CORS(app)

# ==========================================
# KONFIGURASI DATABASE
# ==========================================
# Format: mysql+pymysql://user:password@host/nama_database
DB_USER = 'root'
DB_PASS = ''       # Kosongkan jika pakai XAMPP default
DB_HOST = 'localhost'
DB_NAME = 'kanisius'

# Buat Engine Koneksi
db_connection_str = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
db_connection = create_engine(db_connection_str)

# ==========================================
# 1. MODEL TRAINING
# ==========================================
print("🚀 Server Flask sedang menyalakan mesin AI...")
print("⏳ Mengambil data dari DATABASE dan melatih model...")

# --- LOAD DATA DARI DATABASE ---
try:
    # Query ambil semua data dari tabel 'data'
    query = "SELECT * FROM data"
    df = pd.read_sql(query, db_connection)
    
    # ⚠️ PENTING: Pastikan nama kolom di Database sesuai dengan kodingan
    # Di Screenshot kolomnya 'tahunBulan' (huruf kecil), tapi di kodingan 'TahunBulan'
    # Kita samakan dulu biar tidak error:
    df.rename(columns={'tahunBulan': 'TahunBulan'}, inplace=True)
    
    print(f"✅ Berhasil memuat {len(df)} baris data dari database.")

except Exception as e:
    print(f"❌ Gagal konek database: {e}")
    # Fallback darurat (opsional, bisa dihapus kalau yakin database nyala)
    try:
        df = pd.read_csv("dataKategoriNama.csv", sep=';')
        print("⚠️ Menggunakan file CSV cadangan.")
    except:
        print("❌ Tidak ada data sama sekali (DB & CSV Gagal).")
        df = pd.DataFrame() # Biar gak crash, tapi kosong

# --- CLEANING & PREP (SAMA SEPERTI SEBELUMNYA) ---
if not df.empty:
    # 1. Pastikan TahunBulan format datetime
    df['TahunBulan'] = pd.to_datetime(df['TahunBulan']) 

    # 2. BERSIHKAN DATA KOTOR DULU (\N dari database)
    df.replace('\\N', np.nan, inplace=True)

    # 3. [PERBAIKAN UTAMA] Paksa jumEks jadi Angka
    # errors='coerce' akan mengubah text aneh (kayak \N atau huruf) jadi NaN
    df['jumEks'] = pd.to_numeric(df['jumEks'], errors='coerce')

    # 4. Baru isi NaN dengan 0
    df['jumEks'] = df['jumEks'].fillna(0)
    
    # 5. Lanjut cleaning kolom lain
    df['gudangNama'] = df['gudangNama'].fillna('Unknown')
    df['propNama'] = df['propNama'].fillna('Unknown')

    # Filter Aktif (Sekarang aman karena jumEks sudah pasti angka)
    aktif = df[df['jumEks'] > 0].groupby(['kategoriNama', 'gudangNama', 'propNama']).filter(lambda x: len(x) >= 12)
    # Lengkapi Bulan
    def lengkapi_bulan_smart(df):
        list_dfs = []
        for (kategori, gudang, provinsi), group in df.groupby(['kategoriNama','gudangNama','propNama']):
            all_dates = pd.date_range(group['TahunBulan'].min(), group['TahunBulan'].max(), freq='MS')
            df_group = pd.DataFrame({'kategoriNama': kategori, 'gudangNama': gudang, 'propNama': provinsi, 'TahunBulan': all_dates})
            df_group = df_group.merge(group, on=['kategoriNama','gudangNama','propNama','TahunBulan'], how='left')
            list_dfs.append(df_group)
        return pd.concat(list_dfs, ignore_index=True)

    df_full = lengkapi_bulan_smart(aktif)
    df_full['jumEks'] = df_full['jumEks'].fillna(0)
    df_full = df_full.sort_values(["kategoriNama", "propNama", "gudangNama", "TahunBulan"])

    # Feature Engineering
    for lag in range(1, 13):
        df_full[f'lag_{lag}'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks'].shift(lag)

    df_full['rolling_3'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks'].transform(lambda x: x.rolling(3).mean().shift(1))
    df_full['rolling_6'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks'].transform(lambda x: x.rolling(6).mean().shift(1))
    df_full['rolling_12'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks'].transform(lambda x: x.rolling(12).mean().shift(1))

    df_full['month'] = df_full['TahunBulan'].dt.month
    df_full['year'] = df_full['TahunBulan'].dt.year
    df_full['sin_month'] = np.sin(2 * np.pi * df_full['month'] / 12)
    df_full['cos_month'] = np.cos(2 * np.pi * df_full['month'] / 12)

    cols_to_fill = [f'lag_{i}' for i in range(1, 13)] + ['rolling_3', 'rolling_6', 'rolling_12', 'sin_month', 'cos_month']
    df_full[cols_to_fill] = df_full[cols_to_fill].fillna(0)

    # Encoder
    le_kategori = LabelEncoder()
    le_gudang = LabelEncoder()
    le_prov = LabelEncoder()

    df_full['kategoriNama'] = le_kategori.fit_transform(df_full['kategoriNama'].astype(str))
    df_full['gudangNama'] = le_gudang.fit_transform(df_full['gudangNama'].astype(str))
    df_full['propNama'] = le_prov.fit_transform(df_full['propNama'].astype(str))

    # Training
    feature_cols = ['year', 'month', 'kategoriNama', 'propNama', 'gudangNama', 'sin_month', 'cos_month'] + \
                   [f'lag_{i}' for i in range(1, 13)] + ['rolling_3', 'rolling_6', 'rolling_12']

    model = xgb.XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=3, objective='reg:tweedie', tweedie_variance_power=1.5)
    model.fit(df_full[feature_cols], df_full['jumEks'])
    print("✅ Model SIAP! Server Flask berjalan.")

# ==========================================
# 2. ENDPOINT API PREDICT (SAMA SEPERTI SEBELUMNYA)
# ==========================================
@app.route('/predict', methods=['POST'])
def predict():
    if df.empty: return jsonify([]) # Handle jika DB mati

    data = request.get_json()
    kategori_text = data.get('kategori')
    provinsi_text = data.get('provinsi')
    gudang_text = data.get('gudang')
    
    if gudang_text == "Unknown" or gudang_text is None or gudang_text == "":
        gudang_text = "\\N"

    print(f"📡 Request masuk: {kategori_text} | {provinsi_text} | {gudang_text}")

    try:
        kat_id = le_kategori.transform([kategori_text])[0]
        prop_id = le_prov.transform([provinsi_text])[0]
        gudang_id = le_gudang.transform([gudang_text])[0]
    except ValueError:
        return jsonify([])

    mask = (df_full['kategoriNama'] == kat_id) & (df_full['propNama'] == prop_id) & (df_full['gudangNama'] == gudang_id)
    history = df_full[mask].sort_values('TahunBulan').tail(13)
    
    if len(history) < 12:
        return jsonify([])

    sales_history = history['jumEks'].tolist()
    last_date = history['TahunBulan'].max()
    
    hasil_json = []
    
    for i in range(1, 13):
        current_date = last_date + pd.DateOffset(months=i)
        m = current_date.month
        y = current_date.year
        
        row = {
            'year': y, 'month': m, 'kategoriNama': kat_id, 'propNama': prop_id, 'gudangNama': gudang_id,
            'sin_month': np.sin(2 * np.pi * m / 12), 'cos_month': np.cos(2 * np.pi * m / 12),
            'rolling_3': np.mean(sales_history[-3:]),
            'rolling_6': np.mean(sales_history[-6:]),
            'rolling_12': np.mean(sales_history[-12:])
        }
        for l in range(1, 13):
            row[f'lag_{l}'] = sales_history[-l]
            
        X_pred = pd.DataFrame([row])[feature_cols]
        pred = max(0, model.predict(X_pred)[0])
        sales_history.append(pred)
        
        hasil_json.append({
            'bulan': current_date.strftime('%B %Y'),
            'eksemplar': f"{int(round(pred))}"
        })

    return jsonify(hasil_json)

# ==========================================
# 3. ENDPOINT DROPDOWN (SAMA)
# ==========================================
@app.route('/dropdown', methods=['GET'])
def get_options():
    if df.empty: return jsonify({'kategori': [], 'provinsi': [], 'gudang': []})
    
    list_kategori = sorted(le_kategori.classes_.tolist())
    list_provinsi = sorted(le_prov.classes_.tolist())
    list_gudang = sorted(le_gudang.classes_.tolist())

    return jsonify({
        'kategori': list_kategori,
        'provinsi': list_provinsi,
        'gudang': list_gudang
    })

# ==========================================
# 4. DASHBOARD SUMMARY (UPDATE PAKE DB)
# ==========================================
@app.route('/dashboard/summary-stats', methods=['GET'])
def dashboard_summary_stats():
    try:
        # Kita pakai saja Dataframe global 'df' yang sudah diload di awal
        # Biar gak perlu query ulang ke DB (lebih cepat)
        
        # Tapi kalau mau Realtime banget (misal ada input baru saat app jalan):
        # query = "SELECT * FROM data"
        # df_rt = pd.read_sql(query, db_connection)
        
        # Untuk performa, pakai df global saja:
        df_stats = df.copy() 
        df_stats['Tahun'] = df_stats['TahunBulan'].dt.year

        stats = {
            '2020': int(df_stats[df_stats['Tahun'] == 2020]['jumEks'].sum()),
            '2021': int(df_stats[df_stats['Tahun'] == 2021]['jumEks'].sum()),
            '2022': int(df_stats[df_stats['Tahun'] == 2022]['jumEks'].sum()),
            '2023': int(df_stats[df_stats['Tahun'] == 2023]['jumEks'].sum()),
            '2024': int(df_stats[df_stats['Tahun'] == 2024]['jumEks'].sum())
        }
        return jsonify(stats)
        
    except Exception as e:
        print(f"Error Stats: {e}")
        return jsonify({'2020': 0, '2021': 0, '2022': 0, '2023': 0, '2024': 0})

if __name__ == '__main__':
    app.run(debug=True, port=5000)