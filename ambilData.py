# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import pandas as pd
# import joblib
# import numpy as np
# import os

# app = Flask(__name__)
# # CORS(app)  # ✅ supaya bisa diakses dari frontend (CodeIgniter, React, dsb.)
# #         # Load model dan encoder
# # # ==========================
# # # LOAD MODEL & ENCODER SEKALI SAJA
# # # ==========================
# # MODEL_PATH = r"C:\Users\LENOVO\Downloads\model_xgboost2.pkl"
# # DATA_FULL_PATH = r"C:\Users\LENOVO\Downloads\df_full_ready.csv"
# # LE_KAT_PATH = r"C:\Users\LENOVO\Downloads\le_kategori.pkl"
# # LE_GUDANG_PATH = r"C:\Users\LENOVO\Downloads\le_gudang.pkl"
# # LE_PROV_PATH = r"C:\Users\LENOVO\Downloads\le_prov.pkl"

# # model = joblib.load(MODEL_PATH)
# # le_kategori = joblib.load(LE_KAT_PATH)
# # le_gudang = joblib.load(LE_GUDANG_PATH)
# # le_prov = joblib.load(LE_PROV_PATH)

# # # Load df_full yang sama dengan saat training
# # df_full = pd.read_csv(r"C:\Users\LENOVO\Downloads\df_full_ready (1).csv", sep =',')
# # df_full['tahunBulan'] = pd.to_datetime(df_full['tahunBulan'])

# # feature_order = [
# #     'kategoriDetail','gudangNama','provinsi',
# #     'lag_1','lag_2','lag_3','lag_4','lag_5','lag_6','lag_7','lag_8','lag_9','lag_10','lag_11','lag_12',
# #     'rolling_3','rolling_6','rolling_12',
# #     'year','month','sin_month','cos_month'
# # ]

# # ==========================
# # 1️⃣ GET OPTIONS
# # ==========================
# @app.route('/get_options', methods=['GET'])
# def get_options():
#     try:
#         df = pd.read_csv(r"C:\Users\LENOVO\Downloads\New folder (3)\databulantahungabung2.csv", sep=';')

#         kategori = sorted(df['kategoriDetail'].dropna().unique().tolist())
#         gudang = sorted(df['gudangNama'].dropna().unique().tolist())
#         provinsi = sorted(df['provinsi'].dropna().unique().tolist())

#         return jsonify({
#             'kategori': kategori,
#             'gudang': gudang,
#             'provinsi': provinsi
#         })
#     except Exception as e:
#         print("⚠️ Error get_options:", e)
#         return jsonify({'error': 'Gagal membaca data CSV'}), 500


# # @app.route('/predict', methods=['POST'])
# # def predict():
# #     try:
# #         data = request.get_json()
# #         kategori = data.get('kategori')
# #         provinsi = data.get('provinsi')
# #         gudang = data.get('gudang')

# #         # 1️⃣ LOAD MODEL & ENCODER (dari hasil training Colab)
# #         model = joblib.load(r"C:\Users\LENOVO\Downloads\model_xgboost_final.pkl")
# #         le_kategori = joblib.load(r"C:\Users\LENOVO\Downloads\le_kategori (1).pkl")
# #         le_gudang = joblib.load(r"C:\Users\LENOVO\Downloads\le_gudang (1).pkl")
# #         le_prov = joblib.load(r"C:\Users\LENOVO\Downloads\le_prov.pkl")

# #         # 2️⃣ LOAD DATA MENTAH YANG SAMA
# #         df = pd.read_csv(r"D:\laragon\www\api\databulantahungabung2.csv", sep=';')
# #         df = df.drop(columns=['kategoriNama', 'kategoriId', 'gudangId'], errors='ignore')
# #         df = df.drop_duplicates()
# #         df['tahunBulan'] = pd.to_datetime(df['tahunBulan'])

# #         # 3️⃣ FILTER DATA HISTORIS SESUAI INPUT
# #         target_group = df[
# #             (df['kategoriDetail'] == kategori) &
# #             (df['provinsi'] == provinsi) &
# #             (df['gudangNama'] == gudang)
# #         ].copy()

# #         if target_group.empty:
# #             return jsonify({'error': 'Kombinasi tidak ditemukan di data historis'}), 400

# #         target_group = target_group.sort_values('tahunBulan')

# #         # 4️⃣ FEATURE ENGINEERING (SAMA PERSIS DENGAN TRAINING)
# #         for lag in range(1, 13):
# #             target_group[f'lag_{lag}'] = target_group['eksemplar'].shift(lag)

# #         target_group['rolling_3'] = target_group['eksemplar'].shift(1).rolling(3).mean()
# #         target_group['rolling_6'] = target_group['eksemplar'].shift(1).rolling(6).mean()
# #         target_group['rolling_12'] = target_group['eksemplar'].shift(1).rolling(12).mean()

# #         target_group['year'] = target_group['tahunBulan'].dt.year
# #         target_group['month'] = target_group['tahunBulan'].dt.month
# #         target_group['sin_month'] = np.sin(2 * np.pi * target_group['month'] / 12)
# #         target_group['cos_month'] = np.cos(2 * np.pi * target_group['month'] / 12)
# #         target_group = target_group.fillna(0)

# #         # 5️⃣ ENCODING SESUAI TRAINING
# #         target_group['kategoriDetail'] = le_kategori.transform(target_group['kategoriDetail'])
# #         target_group['provinsi'] = le_prov.transform(target_group['provinsi'])
# #         target_group['gudangNama'] = le_gudang.transform(target_group['gudangNama'])

# #         # 6️⃣ PREDIKSI 12 BULAN KE DEPAN
# #         feature_order = [
# #             'kategoriDetail','gudangNama','provinsi',
# #             'lag_1','lag_2','lag_3','lag_4','lag_5','lag_6','lag_7','lag_8','lag_9','lag_10','lag_11','lag_12',
# #             'rolling_3','rolling_6','rolling_12','year','month','sin_month','cos_month'
# #         ]

# #         future_dates = pd.date_range('2025-01-01', '2025-12-01', freq='MS')
# #         predictions = []

# #         for date in future_dates:
# #             year, month = date.year, date.month
# #             last_data = target_group.iloc[-1]

# #             new_row = {
# #                 'kategoriDetail': last_data['kategoriDetail'],
# #                 'gudangNama': last_data['gudangNama'],
# #                 'provinsi': last_data['provinsi'],
# #                 'year': year, 'month': month,
# #                 'sin_month': np.sin(2 * np.pi * month / 12),
# #                 'cos_month': np.cos(2 * np.pi * month / 12)
# #             }

# #             for lag in range(1, 13):
# #                 new_row[f'lag_{lag}'] = target_group['eksemplar'].iloc[-lag] if len(target_group) >= lag else 0

# #             new_row['rolling_3']  = target_group['eksemplar'].tail(3).mean()
# #             new_row['rolling_6']  = target_group['eksemplar'].tail(6).mean()
# #             new_row['rolling_12'] = target_group['eksemplar'].tail(12).mean()

# #             X_future = pd.DataFrame([new_row])[feature_order]
# #             # pred = model.predict(X_future)[0]
# #             # pred = max(pred + np.random.normal(0, 0.3), 0)
# #             pred = float(model.predict(X_future)[0])
# #             pred = float(max(pred + np.random.normal(0, 0.3), 0))

# #             predictions.append({'tahunBulan': date.strftime('%Y-%m-%d'), 'eksemplar': float(round(pred, 2))})

# #             target_group = pd.concat(
# #                 [target_group, pd.DataFrame([{**new_row, 'eksemplar': pred}])],
# #                 ignore_index=True
# #             )

# #         total_pred = sum(p['eksemplar'] for p in predictions)

# #         return jsonify({
# #             'kategori': kategori,
# #             'provinsi': provinsi,
# #             'gudang': gudang,
# #             'prediksi': predictions,
# #             'total_tahun': round(total_pred, 2)
# #         })

#     # except Exception as e:
#     #     print("🔥 Error utama:", e)
#     #     return jsonify({'error': str(e)}), 500
# # def predict():
# #     try:
# #         data = request.get_json()
# #         kategori = data.get('kategori')
# #         provinsi = data.get('provinsi')
# #         gudang = data.get('gudang')

# #         # Encode input user biar match sama df_full
# #         kat_enc = le_kategori.transform([kategori])[0]
# #         prov_enc = le_prov.transform([provinsi])[0]
# #         gud_enc = le_gudang.transform([gudang])[0]

# #         # Filter berdasarkan df_full yang sudah di-encode
# #         target_group = df_full[
# #             (df_full['kategoriDetail'] == kat_enc) &
# #             (df_full['provinsi'] == prov_enc) &
# #             (df_full['gudangNama'] == gud_enc)
# #         ].copy()

# #         if target_group.empty:
# #             return jsonify({'error': '❌ Kombinasi tidak ditemukan di df_full.'}), 404

# #         target_group = target_group.sort_values('tahunBulan')

# #         # Prediksi 12 bulan ke depan
# #         future_dates = pd.date_range('2025-01-01', '2025-12-01', freq='MS')
# #         predictions = []

# #         for date in future_dates:
# #             year, month = date.year, date.month

# #             new_row = {
# #                 'kategoriDetail': kat_enc,
# #                 'gudangNama': gud_enc,
# #                 'provinsi': prov_enc,
# #                 'year': year,
# #                 'month': month,
# #                 'sin_month': np.sin(2 * np.pi * month / 12),
# #                 'cos_month': np.cos(2 * np.pi * month / 12),
# #             }

# #             # Lag dan rolling diambil dari df_full terakhir
# #             for lag in range(1, 13):
# #                 new_row[f'lag_{lag}'] = target_group['eksemplar'].iloc[-lag] if len(target_group) >= lag else 0
# #             new_row['rolling_3'] = target_group['eksemplar'].tail(3).mean()
# #             new_row['rolling_6'] = target_group['eksemplar'].tail(6).mean()
# #             new_row['rolling_12'] = target_group['eksemplar'].tail(12).mean()

# #             X_future = pd.DataFrame([new_row])[feature_order]
# #             pred = float(model.predict(X_future)[0])
# #             pred = max(pred, 0)

# #             predictions.append({'tahunBulan': date.strftime('%Y-%m-%d'), 'eksemplar': pred})
# #             target_group = pd.concat([target_group, pd.DataFrame([{**new_row, 'eksemplar': pred}])], ignore_index=True)

# #         total_pred = sum(p['eksemplar'] for p in predictions)

# #         return jsonify({
# #             'kategori': kategori,
# #             'provinsi': provinsi,
# #             'gudang': gudang,
# #             'prediksi': predictions,
# #             'total_tahun': round(total_pred, 2)
# #         })

# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)