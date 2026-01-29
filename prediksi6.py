from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import joblib
import os

app = Flask(__name__)
CORS(app)

# ==========================================
# KONFIGURASI DATABASE
# ==========================================
DB_USER = 'kpSkripsi'
DB_PASS = 'ihvcig2F@cmF7@1v'
DB_HOST = '202.65.121.155'
DB_NAME = 'db_kbs_bi'
db_connection_str = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
db_engine = create_engine(db_connection_str)

# ==========================================
# 1. LOAD MODEL DIRECT & ENCODER
# ==========================================
print("🚀 Menyalakan Server Flask (Direct Strategy)...")

try:
    # Load Model Direct
    model = joblib.load("model_direct_sales.pkl")
    print("✅ Model Direct berhasil dimuat.")

    # Load Encoders
    encoders = joblib.load("encoders.pkl")
    le_kategori = encoders['kategori']
    le_gudang = encoders['gudang']
    le_prov = encoders['provinsi']
    print("✅ Encoders berhasil dimuat.")

except Exception as e:
    print(f"❌ ERROR FATAL: {e}")
    print("Jalankan 'python train_model_direct.py' dulu!")
    exit()

# Fitur (SAMA PERSIS DENGAN TRAINING)
feature_cols = ['year', 'month', 'kategoriNama', 'propNama', 'gudangNama', 'sin_month', 'cos_month'] + \
               [f'lag_{i}' for i in range(1, 13)] + ['rolling_3', 'rolling_6', 'rolling_12']

# ==========================================
# 2. ENDPOINT PREDIKSI (FORCE START JANUARI 2025)
# ==========================================
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    kategori_text = data.get('kategori')
    provinsi_text = data.get('provinsi')
    gudang_text = data.get('gudang')

    if not gudang_text or gudang_text == "Unknown":
        gudang_text = "\\N"

    try:
        # Ambil history lengkap
        query = f"""
            SELECT tahunBulan as TahunBulan, jumEks 
            FROM data 
            WHERE kategoriNama = '{kategori_text}' 
            AND propNama = '{provinsi_text}' 
            AND gudangNama = '{gudang_text}'
            ORDER BY TahunBulan ASC 
        """
        full_history_df = pd.read_sql(query, db_engine)
        
        full_history_df['jumEks'] = pd.to_numeric(full_history_df['jumEks'], errors='coerce').fillna(0)
        full_history_df['TahunBulan'] = pd.to_datetime(full_history_df['TahunBulan'])

        # Cek data minimal (tetap butuh sedikit history)
        if len(full_history_df) < 6:
            return jsonify({'history': [], 'forecast': []})

        try:
            kat_id = le_kategori.transform([kategori_text])[0]
            prop_id = le_prov.transform([provinsi_text])[0]
            gudang_id = le_gudang.transform([gudang_text])[0]
        except ValueError:
            return jsonify({'history': [], 'forecast': []})

        # --- A. DATA HISTORY (Untuk Grafik) ---
        history_json = []
        for index, row in full_history_df.iterrows():
            history_json.append({
                'bulan': row['TahunBulan'].strftime('%B %Y'),
                'eksemplar': int(row['jumEks'])
            })

        # HITUNG STATISTIK BULANAN
        seasonal_means = full_history_df.groupby(full_history_df['TahunBulan'].dt.month)['jumEks'].mean().to_dict()
        seasonal_sums = full_history_df.groupby(full_history_df['TahunBulan'].dt.month)['jumEks'].sum().to_dict()

        # --- B. PERSIAPAN PREDIKSI ---
        # Ambil semua data yang ada untuk sales_history
        sales_history = full_history_df['jumEks'].tolist()
        last_real_date = full_history_df['TahunBulan'].max() # Misal: Nov 2024
        
        # [LOGIKA BARU] PAKSA START DATE KE DESEMBER 2024
        # Agar prediksi selalu mulai Januari 2025
        target_last_date = pd.Timestamp("2024-12-01") 
        
        # Jika data terakhir kurang dari Desember 2024, kita isi kekosongan dengan 0
        current_fill_date = last_real_date
        while current_fill_date < target_last_date:
            current_fill_date += pd.DateOffset(months=1)
            sales_history.append(0) # Anggap penjualan 0 untuk bulan yang bolong
            # Opsional: Bisa juga append rata-rata kalau tidak mau 0
        
        # Update last_date jadi Desember 2024 (Virtual)
        last_date = target_last_date 
        m = last_date.month
        y = last_date.year
        
        # Fitur X untuk model (Ambil 12 data terakhir dari sales_history yang sudah dilengkapin)
        # Pastikan sales_history cukup panjang
        if len(sales_history) < 13:
             # Kalau history kependekan, padding depan dengan rata-rata
             avg_fill = np.mean(sales_history)
             sales_history = [avg_fill] * (13 - len(sales_history)) + sales_history

        row_feat = {
            'year': y, 'month': m, 
            'kategoriNama': kat_id, 'propNama': prop_id, 'gudangNama': gudang_id,
            # 'sin_month': np.sin(2 * np.pi * m / 12), 
            # 'cos_month': np.cos(2 * np.pi * m / 12),
            'rolling_3': np.mean(sales_history[-3:]),
            'rolling_6': np.mean(sales_history[-6:]),
            'rolling_12': np.mean(sales_history[-12:])
        }
        for l in range(1, 13):
            row_feat[f'lag_{l}'] = sales_history[-l]
            
        X_input = pd.DataFrame([row_feat])[feature_cols]

        # PREDIKSI
        preds_12_bulan = model.predict(X_input)[0] 
        
        # --- C. FORMAT HASIL ---
        forecast_json = []
        for i, val in enumerate(preds_12_bulan):
            next_date = last_date + pd.DateOffset(months=i+1) # Akan mulai Jan 2025
            bulan_angka = next_date.month
            pred_value = max(0, val)
            
            # Data Aktual Tahun Lalu
            prev_year_date = next_date - pd.DateOffset(years=1)
            prev_data = full_history_df[full_history_df['TahunBulan'] == prev_year_date]
            aktual_lalu_val = int(prev_data.iloc[0]['jumEks']) if not prev_data.empty else 0
            
            rata_rata_val = seasonal_means.get(bulan_angka, 0)
            total_history_val = seasonal_sums.get(bulan_angka, 0)

            forecast_json.append({
                'bulan': next_date.strftime('%B %Y'),
                'eksemplar': f"{int(round(pred_value))}",
                'aktual_lalu': f"{aktual_lalu_val}",
                'total_history': f"{int(round(total_history_val))}",
                'rata_rata': f"{int(round(rata_rata_val))}"
            })

        return jsonify({
            'status': 'success',
            'history': history_json,
            'forecast': forecast_json
        })

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return jsonify({'history': [], 'forecast': []})
# ==========================================
# ENDPOINT LAINNYA (TETAP SAMA)
# ==========================================
@app.route('/dropdown', methods=['GET'])
def get_options():
    return jsonify({
        'kategori': sorted(le_kategori.classes_.tolist()),
        'provinsi': sorted(le_prov.classes_.tolist()),
        'gudang': sorted(le_gudang.classes_.tolist())
    })

@app.route('/dashboard/summary-stats', methods=['GET'])
def dashboard_summary_stats():
    try:
        query = "SELECT YEAR(tahunBulan) as Tahun, SUM(jumEks) as Total FROM data GROUP BY YEAR(tahunBulan)"
        df_stats = pd.read_sql(query, db_engine)
        stats = {str(int(row['Tahun'])): int(row['Total']) for index, row in df_stats.iterrows()}
        for y in ['2020', '2021', '2022', '2023', '2024']:
            if y not in stats: stats[y] = 0
        return jsonify(stats)
    except:
        return jsonify({})

if __name__ == '__main__':
    app.run(debug=True, port=5000)