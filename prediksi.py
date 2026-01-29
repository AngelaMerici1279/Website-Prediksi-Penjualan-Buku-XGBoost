from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
import xgboost as xgb  # Kita butuh ini buat baca JSON
import os
import sys

app = Flask(__name__)

# =========================================
# 1. LOAD DATA & MODEL (FORMAT JSON)
# =========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"📂 Folder Aplikasi: {BASE_DIR}")

def load_file(filename):
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        print(f"❌ FATAL: File {filename} hilang!")
        sys.exit(1)
    return path

try:
    print("Loading model & data...")
    
    # --- PERUBAHAN PENTING (BACA JSON) ---
    # 1. Bikin wadah kosong dulu
    model = xgb.XGBRegressor() 
    # 2. Isi otaknya dengan file JSON
    model.load_model(load_file("model_final.json"))
    print("✅ Model JSON berhasil dimuat!")
    # -------------------------------------

    le_kategori = joblib.load(load_file("encoder_kategori.pkl"))
    le_prov = joblib.load(load_file("encoder_provinsi.pkl"))
    df_ratio = pd.read_csv(load_file("tabel_ratio_gudang.csv"))
    df_history = pd.read_csv(load_file("data_history_terakhir.csv"))
    df_history['TahunBulan'] = pd.to_datetime(df_history['TahunBulan'])
    
    # Ambil daftar kolom otomatis dari JSON
    # Ini RAHASIA kenapa JSON lebih bagus: Dia ingat nama kolomnya!
    MODEL_COLS = model.get_booster().feature_names
    print(f"📝 Model minta {len(MODEL_COLS)} kolom: {MODEL_COLS}")

except Exception as e:
    print(f"❌ Error Load: {e}")
    sys.exit(1)

# =========================================
# 2. FUNGSI BANTUAN
# =========================================
def get_latest_features(kategori, provinsi):
    history = df_history[
        (df_history['kategoriNama'] == kategori) & 
        (df_history['propNama'] == provinsi)
    ].sort_values('TahunBulan')
    
    last_12 = history.tail(12)
    if len(last_12) < 12: return None
    return last_12['jumEks'].values

# =========================================
# 3. ROUTE PREDICT
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
            print(f"❌ Kategori '{kategori}' tidak dikenal!")
            return jsonify([])
    except: pass 

    # 2. Ambil History
    last_sales_array = get_latest_features(kategori, provinsi)
    if last_sales_array is None:
        print("❌ Data history kurang/kosong!")
        return jsonify([]) 

    print(f"📊 Input History (Akhir): {last_sales_array[-1]}")
    current_history = list(last_sales_array)

    # 3. Cari Rasio
    row_ratio = df_ratio[
        (df_ratio['kategoriNama'] == kategori) & 
        (df_ratio['propNama'] == provinsi) & 
        (df_ratio['gudangNama'] == gudang)
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
        
        # Encoding
        try:
            row['kategoriCode'] = le_kategori.transform([kategori])[0]
            row['propCode'] = le_prov.transform([provinsi])[0]
        except: continue

        # REORDER KOLOM SESUAI JSON (SUPER PENTING)
        # Kita paksa urutan kolom sama persis dengan yang diminta JSON
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
        
        print(f"Bulan {i}: InputLag={recent_window[-1]:.0f} -> Output={pred_prov:.2f}")

        hasil_output.append({
            'bulan': f"{nama_bulan[i-1]} {tahun_prediksi}",
            'eksemplar': str(round(pred_gudang, 0))
        })
        
    return jsonify(hasil_output)

@app.route('/dropdown', methods=['GET'])
def dropdown():
    list_kategori = sorted(df_ratio['kategoriNama'].dropna().unique().tolist())
    list_provinsi = sorted(df_ratio['propNama'].dropna().unique().tolist())
    list_gudang = sorted(df_ratio['gudangNama'].dropna().unique().tolist())
    if '\\N' in list_gudang: list_gudang.remove('\\N')
    return jsonify({'kategori': list_kategori, 'provinsi': list_provinsi, 'gudang': list_gudang})

if __name__ == '__main__':
    app.run(debug=True, port=5000)