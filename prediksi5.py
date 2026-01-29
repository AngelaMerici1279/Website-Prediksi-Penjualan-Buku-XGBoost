from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import xgboost as xgb
from sqlalchemy import create_engine
import joblib
import os

app = Flask(__name__)
CORS(app)

#Kondigurasi ke database
DB_USER = 'root'
DB_PASS = ''
DB_HOST = 'localhost'
DB_NAME = 'kanisius'
db_connection_str = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
db_engine = create_engine(db_connection_str)

try:
    #Model
    model = xgb.XGBRegressor()
    model.load_model("model_sales.json")

    #Encoders
    encoders = joblib.load("encoders.pkl")
    le_kategori = encoders['kategori']
    le_gudang = encoders['gudang']
    le_prov = encoders['provinsi']
    

except Exception as e:
    print(f"ERROR FATAL: {e}")
    exit() #server jika file tidak ada

# Daftar fitur harus SAMA PERSIS dengan waktu training
feature_cols = ['year', 'month', 'kategoriNama', 'propNama', 'gudangNama'] + \
               [f'lag_{i}' for i in range(1, 13)] + ['rolling_3', 'rolling_6', 'rolling_12']

#endpoint prediksi
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    kategori_text = data.get('kategori')
    provinsi_text = data.get('provinsi')
    gudang_text = data.get('gudang')

    if not gudang_text or gudang_text == "Unknown":
        gudang_text = "\\N"

    try:
        # [MODIFIKASI] Ambil history panjang (5 tahun) buat grafik
        query = f"""
            SELECT tahunBulan as TahunBulan, jumEks 
            FROM data 
            WHERE kategoriNama = '{kategori_text}' 
            AND propNama = '{provinsi_text}' 
            AND gudangNama = '{gudang_text}'
            ORDER BY TahunBulan ASC 
        """
        full_history_df = pd.read_sql(query, db_engine)
  
        # Cleaning
        full_history_df['jumEks'] = pd.to_numeric(full_history_df['jumEks'], errors='coerce').fillna(0)
        full_history_df['TahunBulan'] = pd.to_datetime(full_history_df['TahunBulan'])
        
        full_history_df['month_num'] = full_history_df['TahunBulan'].dt.month
        seasonal_means = full_history_df.groupby('month_num')['jumEks'].mean().to_dict()
        seasonal_sums = full_history_df.groupby('month_num')['jumEks'].sum().to_dict()

        if len(full_history_df) < 12:
            return jsonify({'history': [], 'forecast': []})

        try:
            kat_id = le_kategori.transform([kategori_text])[0]
            prop_id = le_prov.transform([provinsi_text])[0]
            gudang_id = le_gudang.transform([gudang_text])[0]
        except ValueError:
            return jsonify({'history': [], 'forecast': []})

        # --- A. SIAPKAN DATA HISTORY UTUH (Untuk UI) ---
        history_json = []
        for index, row in full_history_df.iterrows():
            history_json.append({
                'bulan': row['TahunBulan'].strftime('%B %Y'),
                'eksemplar': int(row['jumEks'])
            })

        # --- B. PROSES PREDIKSI REKURSIF ---
        # Kita ambil 13 bulan terakhir saja untuk bahan perhitungan fitur
        calc_df = full_history_df.tail(13).copy()
        
        sales_history = calc_df['jumEks'].tolist() # List ini akan terus bertambah
        last_date = calc_df['TahunBulan'].max()
        
        forecast_json = []

        # Loop 12 Bulan ke depan (Rekursif)
        for i in range(1, 13):
            current_date = last_date + pd.DateOffset(months=i)
            m = current_date.month
            y = current_date.year

            # [PENTING] Fitur harus lengkap sesuai training (termasuk sin/cos)
            row = {
                'year': y, 'month': m, 
                'kategoriNama': kat_id, 'propNama': prop_id, 'gudangNama': gudang_id,
                # 'sin_month': np.sin(2 * np.pi * m / 12), 
                # 'cos_month': np.cos(2 * np.pi * m / 12),
                'rolling_3': np.mean(sales_history[-3:]),
                'rolling_6': np.mean(sales_history[-6:]),
                'rolling_12': np.mean(sales_history[-12:])
            }
            for l in range(1, 13):
                row[f'lag_{l}'] = sales_history[-l]
            
            # Prediksi 1 bulan
            X_pred = pd.DataFrame([row])[feature_cols]
            pred = max(0, model.predict(X_pred)[0])
            
            prev_year_date = current_date - pd.DateOffset(years=1)
            aktual_lalu = full_history_df[full_history_df['TahunBulan'] == prev_year_date]
            val_aktual_lalu = int(aktual_lalu['jumEks'].iloc[0]) if not aktual_lalu.empty else 0
            
            # Masukkan hasil prediksi ke history (agar dipakai bulan depannya)
            sales_history.append(pred)
            
            forecast_json.append({
                'bulan': current_date.strftime('%B %Y'),
                'eksemplar': f"{int(round(pred))}",
                'aktual_lalu': val_aktual_lalu,
                'total_history': int(seasonal_sums.get(m, 0)),
                'rata_rata': int(round(seasonal_means.get(m, 0)))
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
# 3. ENDPOINT DROPDOWN (Dari Encoder)
# ==========================================
@app.route('/dropdown', methods=['GET'])
def get_options():
    # Ambil list langsung dari file encoder yang diload
    # Jauh lebih cepat daripada query SELECT DISTINCT ke DB
    return jsonify({
        'kategori': sorted(le_kategori.classes_.tolist()),
        'provinsi': sorted(le_prov.classes_.tolist()),
        'gudang': sorted(le_gudang.classes_.tolist())
    })

# ==========================================
# 4. DASHBOARD STATS
# ==========================================
@app.route('/dashboard/summary-stats', methods=['GET'])
def dashboard_summary_stats():
    try:
        # Query simpel SQL Aggregate (Jauh lebih cepat daripada Pandas groupby di Python)
        query = """
            SELECT YEAR(TahunBulan) as Tahun, SUM(jumEks) as Total 
            FROM data 
            GROUP BY YEAR(TahunBulan)
        """
        df_stats = pd.read_sql(query, db_engine)
        
        # Convert ke dictionary
        stats = {str(int(row['Tahun'])): int(row['Total']) for index, row in df_stats.iterrows()}
        
        # Pastikan tahun 2020-2024 ada meski 0
        for y in ['2020', '2021', '2022', '2023', '2024']:
            if y not in stats: stats[y] = 0
            
        return jsonify(stats)
    except Exception as e:
        print(f"Error Stats: {e}")
        return jsonify({})

if __name__ == '__main__':
    app.run(debug=True, port=5000)