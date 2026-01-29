from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
import os
import sys

app = Flask(__name__)

# =========================================
# GLOBAL VARIABLES
# =========================================
model = None
le_kategori = None
le_gudang = None
le_prov = None
df_history = None # Untuk menyimpan data history per gudang
MODEL_COLS = []

# =========================================
# 1. FUNGSI LOGIKA LAMA (Sesuai Scriptmu)
# =========================================
def lengkapi_bulan_smart(df):
    list_dfs = []
    # Logika: Group by Kategori, Gudang, Propinsi
    for (kategori, gudang, provinsi), group in df.groupby(['kategoriNama','gudangNama','propNama']):
        all_dates = pd.date_range(group['TahunBulan'].min(), group['TahunBulan'].max(), freq='MS')
        df_group = pd.DataFrame({
            'kategoriNama': kategori,
            'gudangNama': gudang,
            'propNama': provinsi,
            'TahunBulan': all_dates
        })
        df_group = df_group.merge(group, on=['kategoriNama','gudangNama','propNama','TahunBulan'], how='left')
        list_dfs.append(df_group)
    
    if not list_dfs: return pd.DataFrame()
    return pd.concat(list_dfs, ignore_index=True)

def imputasi_hybrid(x):
    # Logika Interpolasi Linear
    if (x > 0).sum() >= 12:
        return x.interpolate(method='linear', limit_direction='both')
    else:
        return x.fillna(0)

def train_model_old_method():
    global model, le_kategori, le_gudang, le_prov, df_history, MODEL_COLS
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, 'dataKategoriNama.csv')
    
    print("🚀 [METODE LAMA] SEDANG MELATIH MODEL DARI NOL...")
    
    if not os.path.exists(csv_path):
        print("❌ ERROR: File csv tidak ditemukan!")
        sys.exit(1)

    # 1. Load Data
    df = pd.read_csv(csv_path, sep=';')
    df = df.drop(columns=['gudangId'])
    df['TahunBulan'] = pd.to_datetime(df['TahunBulan'])
    
    # 2. Clipping Outlier (Sesuai kodemu)
    # Hati-hati: ini yang bikin prediksi musim ajaran baru jadi rendah
    # df["jumEks"] = np.clip(df["jumEks"], 0, df["jumEks"].quantile(0.95))
    
    # 3. Filter Aktif
    aktif = (
        df[df['jumEks'] > 0]
        .groupby(['kategoriNama', 'gudangNama', 'propNama'])
        .filter(lambda x: len(x) >= 12)
    )
    
    # 4. Lengkapi Bulan & Imputasi
    df_full = lengkapi_bulan_smart(aktif)
    df_full['jumEks'] = (
        df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks']
        .transform(imputasi_hybrid)
    )
    # Fallback fillna 0 jika interpolate gagal di awal
    df_full['jumEks'] = df_full['jumEks'].fillna(0)
    
    df_full = df_full.sort_values(["kategoriNama", "propNama", "gudangNama", "TahunBulan"])
    
    # Simpan History untuk Prediksi Nanti
    # Kita butuh data asli (setelah imputasi) untuk lag
    df_history = df_full.copy()

    # 5. Feature Engineering
    for lag in range(1, 13):
        df_full[f'lag_{lag}'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks'].shift(lag)
        
    df_full['rolling_3'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks']\
        .transform(lambda x: x.rolling(window=3, min_periods=1).mean().shift(1))
    df_full['rolling_6'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks']\
        .transform(lambda x: x.rolling(window=6, min_periods=1).mean().shift(1))
    df_full['rolling_12'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks']\
        .transform(lambda x: x.rolling(window=12, min_periods=1).mean().shift(1))
        
    df_full['year'] = df_full['TahunBulan'].dt.year
    df_full['month'] = df_full['TahunBulan'].dt.month
    df_full['sin_month'] = np.sin(2 * np.pi * df_full['month'] / 12)
    df_full['cos_month'] = np.cos(2 * np.pi * df_full['month']/ 12)

    # Encoding
    le_kategori = LabelEncoder()
    le_gudang = LabelEncoder()
    le_prov = LabelEncoder()

    df_full['kategoriNama'] = le_kategori.fit_transform(df_full['kategoriNama'])
    df_full['gudangNama'] = le_gudang.fit_transform(df_full['gudangNama'])
    df_full['propNama'] = le_prov.fit_transform(df_full['propNama'])
    
    # Bersihkan NaN
    df_ready = df_full.dropna()

    # 6. Training
    features = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5', 'lag_6', 'lag_7',
                'lag_8', 'lag_9', 'lag_10', 'lag_11', 'lag_12', 
                'rolling_3', 'rolling_6', 'rolling_12', 
                'year', 'month', 'sin_month', 'cos_month', 
                'kategoriNama', 'gudangNama', 'propNama'] # Perhatikan kolom ini
    
    MODEL_COLS = features
    
    X = df_ready[features]
    y = df_ready['jumEks']

    # Parameter Model (Sesuai kodemu)
    model = xgb.XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=3,
        gamma=0.5,
        random_state=42,
        reg_alpha=0.5,
        reg_lambda=1
    )
    
    model.fit(X, y)
    print("✅ TRAINING METODE LAMA SELESAI!")


# =========================================
# 2. STARTUP
# =========================================
try:
    train_model_old_method()
except Exception as e:
    print(f"❌ Error Training: {e}")
    sys.exit(1)


# =========================================
# 3. ROUTE PREDICT (Logika Per Gudang)
# =========================================
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    kategori = str(data.get('kategori', '')).strip()
    provinsi = str(data.get('provinsi', '')).strip()
    gudang = str(data.get('gudang', '')).strip()
    
    print(f"\n--- REQUEST (METODE LAMA): {kategori} | {provinsi} | {gudang} ---")

    # Cek Validitas
    if kategori not in le_kategori.classes_ or \
       gudang not in le_gudang.classes_ or \
       provinsi not in le_prov.classes_:
        print("❌ Data baru (tidak ada di training set). Return 0.")
        return jsonify([])

    # Ambil History Spesifik GUDANG (Bukan Provinsi)
    history_subset = df_history[
        (df_history['kategoriNama'] == kategori) & 
        (df_history['propNama'] == provinsi) &
        (df_history['gudangNama'] == gudang)
    ].sort_values('TahunBulan')
    
    if len(history_subset) < 12:
        return jsonify([])
    
    current_history = list(history_subset.tail(12)['jumEks'].values)
    
    tahun_prediksi = 2025
    hasil_output = []
    nama_bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", 
                  "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

    for i in range(1, 13):
        row = pd.DataFrame()
        recent_window = current_history[-12:]
        
        # Fitur Lag
        for lag in range(1, 13): row[f'lag_{lag}'] = [recent_window[-lag]]
        
        # Fitur Rolling
        row['rolling_3'] = np.mean(recent_window[-3:])
        row['rolling_6'] = np.mean(recent_window[-6:])
        row['rolling_12'] = np.mean(recent_window[-12:])
        
        # Time
        row['year'] = tahun_prediksi
        row['month'] = i
        row['sin_month'] = np.sin(2 * np.pi * i / 12)
        row['cos_month'] = np.cos(2 * np.pi * i / 12)
        
        # Encoding
        try:
            row['kategoriNama'] = le_kategori.transform([kategori])[0]
            row['gudangNama'] = le_gudang.transform([gudang])[0]
            row['propNama'] = le_prov.transform([provinsi])[0]
        except: continue

        # Reorder
        row = row[MODEL_COLS]

        # Prediksi
        pred = model.predict(row)[0]
        pred = max(0, pred) # Tetap max 0 biar gak minus
        
        # Update History
        current_history.append(pred)
        
        hasil_output.append({
            'bulan': f"{nama_bulan[i-1]} {tahun_prediksi}",
            'eksemplar': str(round(pred, 0))
        })
        
    return jsonify(hasil_output)

@app.route('/dropdown', methods=['GET'])
def dropdown():
    list_kategori = sorted(df_history['kategoriNama'].unique().tolist())
    list_provinsi = sorted(df_history['propNama'].unique().tolist())
    list_gudang = sorted(df_history['gudangNama'].unique().tolist())
    return jsonify({'kategori': list_kategori, 'provinsi': list_provinsi, 'gudang': list_gudang})

if __name__ == '__main__':
    # Jalankan di PORT 5001 supaya tidak bentrok dengan metode baru
    app.run(debug=True, port=5000)