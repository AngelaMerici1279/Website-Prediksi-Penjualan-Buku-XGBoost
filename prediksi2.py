from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
import os
import sys

app = Flask(__name__)

# =========================================
# 1. SETUP PATH & LOAD MODEL (STATIS)
# =========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"📂 Folder Aplikasi: {BASE_DIR}")

def load_file(filename):
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        print(f"❌ FATAL: File {filename} hilang!")
        sys.exit(1)
    return path

# Global Variables untuk Data In-Memory
df_history_live = None
df_ratio_live = None
model = None
le_kategori = None
le_prov = None
MODEL_COLS = []

# =========================================
# 2. FUNGSI PREPROCESSING RAW DATA--
#    (Ini logika pindahan dari script training)
# =========================================
def process_raw_data():
    global df_history_live, df_ratio_live
    
    print("🔄 Sedang memproses Data Mentah (Raw Data)...")
    csv_path = load_file("dataKategoriNama.csv") # BACA DATA MENTAH
    
    # 1. Baca CSV
    df = pd.read_csv(csv_path, sep=';')
    df['TahunBulan'] = pd.to_datetime(df['TahunBulan'])
    
    # --- PROSES A: HITUNG RASIO GUDANG ---
    print("   -> Menghitung Rasio Gudang...")
    # Ambil data setahun terakhir untuk rasio yang relevan
    last_year_date = df['TahunBulan'].max() - pd.DateOffset(months=12)
    df_recent = df[df['TahunBulan'] >= last_year_date].copy()
    
    # Hitung total per propinsi
    grp_prop = df_recent.groupby(['kategoriNama', 'propNama'])['jumEks'].sum().reset_index()
    grp_prop.rename(columns={'jumEks': 'Total_Prop'}, inplace=True)
    
    # Hitung total per gudang
    grp_gudang = df_recent.groupby(['kategoriNama', 'propNama', 'gudangNama'])['jumEks'].sum().reset_index()
    
    # Gabung
    df_ratio_live = grp_gudang.merge(grp_prop, on=['kategoriNama', 'propNama'], how='left')
    df_ratio_live['Ratio'] = df_ratio_live['jumEks'] / df_ratio_live['Total_Prop']
    df_ratio_live['Ratio'] = df_ratio_live['Ratio'].fillna(0)
    
    # --- PROSES B: SIAPKAN HISTORY (Agregasi Provinsi) ---
    print("   -> Menyiapkan Data History...")
    # Agregasi ke level Provinsi (Gudang dihilangkan dulu)
    df_agg = df.groupby(['kategoriNama', 'propNama', 'TahunBulan'])['jumEks'].sum().reset_index()
    
    # Filter kategori aktif (Minimal ada 12 bulan data)
    # Note: Kalau mau lebih longgar, bisa dihapus filter ini
    aktif = df_agg.groupby(['kategoriNama', 'propNama']).filter(lambda x: len(x) >= 12)
    
    # Lengkapi Bulan yang Bolong (PENTING!)
    list_dfs = []
    for (k, p), g in df_agg.groupby(['kategoriNama', 'propNama']): # Pakai df_agg biar semua masuk
        if g.empty: continue
        all_dates = pd.date_range(g['TahunBulan'].min(), g['TahunBulan'].max(), freq='MS')
        temp = pd.DataFrame({'kategoriNama': k, 'propNama': p, 'TahunBulan': all_dates})
        temp = temp.merge(g, on=['kategoriNama','propNama','TahunBulan'], how='left')
        list_dfs.append(temp)
    
    if list_dfs:
        df_history_live = pd.concat(list_dfs).fillna(0)
        df_history_live = df_history_live.sort_values(['kategoriNama', 'propNama', 'TahunBulan'])
    else:
        df_history_live = pd.DataFrame(columns=['kategoriNama', 'propNama', 'TahunBulan', 'jumEks'])

    print("✅ PREPROCESSING SELESAI! Data siap digunakan.")

# =========================================
# 3. INITIALIZATION (Jalan pas Start)
# =========================================
try:
    print("🚀 MEMULAI SERVER FLASK...")
    
    # Load Otak (Model & Encoder)
    # Kita tetap butuh ini biar encoding-nya konsisten
    model = xgb.XGBRegressor()
    model.load_model(load_file("model_final.json"))
    le_kategori = joblib.load(load_file("encoder_kategori.pkl"))
    le_prov = joblib.load(load_file("encoder_provinsi.pkl"))
    
    MODEL_COLS = model.get_booster().feature_names
    print(f"✅ Model Loaded. Kolom: {MODEL_COLS}")
    
    # Proses Data Mentah jadi Data Siap Pakai
    process_raw_data()
    
except Exception as e:
    print(f"❌ Error Init: {e}")
    sys.exit(1)

# =========================================
# 4. ROUTE PREDICT
# =========================================
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    kategori = str(data.get('kategori', '')).strip()
    provinsi = str(data.get('provinsi', '')).strip()
    gudang = str(data.get('gudang', '')).strip()
    
    print(f"\n--- REQUEST: {kategori} | {provinsi} | {gudang} ---")

    # 1. Cek Encoding
    try:
        if kategori not in le_kategori.classes_:
            print(f"❌ Kategori '{kategori}' tidak dikenal model!")
            return jsonify([])
    except: pass

    # 2. Ambil History dari Data Live
    # Filter data history yang sudah kita proses di awal tadi
    history_subset = df_history_live[
        (df_history_live['kategoriNama'] == kategori) & 
        (df_history_live['propNama'] == provinsi)
    ].sort_values('TahunBulan')
    
    last_12 = history_subset.tail(12)
    
    if len(last_12) < 12:
        print("❌ Data history kurang dari 12 bulan!")
        return jsonify([]) 
        
    last_sales_array = last_12['jumEks'].values
    current_history = list(last_sales_array)

    # 3. Cari Rasio dari Data Live
    row_ratio = df_ratio_live[
        (df_ratio_live['kategoriNama'] == kategori) & 
        (df_ratio_live['propNama'] == provinsi) & 
        (df_ratio_live['gudangNama'] == gudang)
    ]
    rasio = row_ratio['Ratio'].values[0] if not row_ratio.empty else 0
    print(f"✅ Rasio: {rasio:.4f}")

    # 4. Loop Prediksi
    tahun_prediksi = 2025
    hasil_output = []
    nama_bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", 
                  "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

    for i in range(1, 13):
        row = pd.DataFrame()
        recent_window = current_history[-12:]
        
        # Fitur Lag & Rolling
        for lag in range(1, 13):
            row[f'lag_{lag}'] = [recent_window[-lag]]
        row['rolling_3'] = np.mean(recent_window[-3:])
        row['rolling_6'] = np.mean(recent_window[-6:])
        row['rolling_12'] = np.mean(recent_window[-12:])
        row['year'] = tahun_prediksi
        row['month'] = i
        row['sin_month'] = np.sin(2 * np.pi * i / 12)
        row['cos_month'] = np.cos(2 * np.pi * i / 12)
        
        # Encoding (Pake Encoder Lama)
        try:
            row['kategoriCode'] = le_kategori.transform([kategori])[0]
            row['propCode'] = le_prov.transform([provinsi])[0]
        except: continue

        # Reorder Kolom
        try:
            row = row[MODEL_COLS]
        except KeyError as e:
            print(f"❌ Kolom Mismatch: {e}")
            break

        # Prediksi
        pred_prov = model.predict(row)[0]
        pred_prov = max(0, pred_prov)
        
        current_history.append(pred_prov)
        pred_gudang = pred_prov * rasio
        
        # print(f"Bulan {i}: {pred_prov:.2f} -> {pred_gudang:.2f}") # Debug kalau perlu

        hasil_output.append({
            'bulan': f"{nama_bulan[i-1]} {tahun_prediksi}",
            'eksemplar': str(round(pred_gudang, 0))
        })
        
    return jsonify(hasil_output)

@app.route('/dropdown', methods=['GET'])
def dropdown():
    # Ambil list dari data live
    if df_ratio_live is not None:
        list_kategori = sorted(df_ratio_live['kategoriNama'].dropna().unique().tolist())
        list_provinsi = sorted(df_ratio_live['propNama'].dropna().unique().tolist())
        list_gudang = sorted(df_ratio_live['gudangNama'].dropna().unique().tolist())
        if '\\N' in list_gudang: list_gudang.remove('\\N')
        return jsonify({'kategori': list_kategori, 'provinsi': list_provinsi, 'gudang': list_gudang})
    else:
        return jsonify({'kategori': [], 'provinsi': [], 'gudang': []})
# =========================================
# ROUTE DASHBOARD: Statistik Ringkas (Card)
# =========================================
@app.route('/dashboard/summary-stats', methods=['GET'])
def dashboard_summary_stats():
    # Cek file data
    if not os.path.exists('dataKategoriNama.csv'):
        return jsonify({'2022': 0, '2023': 0, '2024': 0})

    try:
        # Baca Data
        df = pd.read_csv('dataKategoriNama.csv', sep=';')
        df['TahunBulan'] = pd.to_datetime(df['TahunBulan'])
        df['Tahun'] = df['TahunBulan'].dt.year

        # Hitung Total per Tahun
        stats = {
            '2022': int(df[df['Tahun'] == 2022]['jumEks'].sum()),
            '2023': int(df[df['Tahun'] == 2023]['jumEks'].sum()),
            '2024': int(df[df['Tahun'] == 2024]['jumEks'].sum())
        }
        return jsonify(stats)
        
    except Exception as e:
        print(f"Error Stats: {e}")
        return jsonify({'2022': 0, '2023': 0, '2024': 0})
if __name__ == '__main__':
    app.run(debug=True, port=5000)