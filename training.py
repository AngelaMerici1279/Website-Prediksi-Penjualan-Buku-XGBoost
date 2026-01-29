# import pandas as pd
# import numpy as np
# import xgboost as xgb
# from sklearn.preprocessing import LabelEncoder
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score # Import Metrik
# from sqlalchemy import create_engine
# import joblib 
# import os

# # --- KONEKSI DB ---
# DB_USER = 'root'
# DB_PASS = ''
# DB_HOST = 'localhost'
# DB_NAME = 'kanisius'
# db_connection_str = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
# db_connection = create_engine(db_connection_str)

# print("⏳ Sedang memproses data... (Mohon tunggu)")

# # 1. LOAD DATA
# df = pd.read_sql("SELECT * FROM data", db_connection)
# df.rename(columns={'tahunBulan': 'TahunBulan'}, inplace=True)

# # 2. PREPROCESSING
# df['TahunBulan'] = pd.to_datetime(df['TahunBulan'])
# df['jumEks'] = pd.to_numeric(df['jumEks'], errors='coerce').fillna(0)
# df.replace('\\N', np.nan, inplace=True)
# df['gudangNama'] = df['gudangNama'].fillna('Unknown')
# df['propNama'] = df['propNama'].fillna('Unknown')

# # Filter Aktif
# aktif = df[df['jumEks'] > 0].groupby(['kategoriNama', 'gudangNama', 'propNama']).filter(lambda x: len(x) >= 12)

# # Lengkapi Bulan
# def lengkapi_bulan_smart(df):
#     list_dfs = []
#     for (kategori, gudang, provinsi), group in df.groupby(['kategoriNama','gudangNama','propNama']):
#         all_dates = pd.date_range(group['TahunBulan'].min(), group['TahunBulan'].max(), freq='MS')
#         df_group = pd.DataFrame({'kategoriNama': kategori, 'gudangNama': gudang, 'propNama': provinsi, 'TahunBulan': all_dates})
#         df_group = df_group.merge(group, on=['kategoriNama','gudangNama','propNama','TahunBulan'], how='left')
#         list_dfs.append(df_group)
#     return pd.concat(list_dfs, ignore_index=True)

# df_full = lengkapi_bulan_smart(aktif)
# df_full['jumEks'] = df_full['jumEks'].fillna(0)
# df_full = df_full.sort_values(["kategoriNama", "propNama", "gudangNama", "TahunBulan"])

# # 3. FEATURE ENGINEERING
# for lag in range(1, 13):
#     df_full[f'lag_{lag}'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks'].shift(lag)

# df_full['rolling_3'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks'].transform(lambda x: x.rolling(3).mean().shift(1))
# df_full['rolling_6'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks'].transform(lambda x: x.rolling(6).mean().shift(1))
# df_full['rolling_12'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks'].transform(lambda x: x.rolling(12).mean().shift(1))

# df_full['month'] = df_full['TahunBulan'].dt.month
# df_full['year'] = df_full['TahunBulan'].dt.year
# # df_full['sin_month'] = np.sin(2 * np.pi * df_full['month'] / 12)
# # df_full['cos_month'] = np.cos(2 * np.pi * df_full['month'] / 12)

# # Fill NaNs created by lags
# cols_to_fill = [f'lag_{i}' for i in range(1, 13)] + ['rolling_3', 'rolling_6', 'rolling_12']
# df_full[cols_to_fill] = df_full[cols_to_fill]

# # 4. ENCODING
# le_kategori = LabelEncoder()
# le_gudang = LabelEncoder()
# le_prov = LabelEncoder()

# df_full['kategoriNama'] = le_kategori.fit_transform(df_full['kategoriNama'].astype(str))
# df_full['gudangNama'] = le_gudang.fit_transform(df_full['gudangNama'].astype(str))
# df_full['propNama'] = le_prov.fit_transform(df_full['propNama'].astype(str))

# # Simpan Encoders
# print("💾 Menyimpan Encoders...")
# joblib.dump({'kategori': le_kategori, 'gudang': le_gudang, 'provinsi': le_prov}, 'encoders.pkl')

# # =========================================================
# # 5. SPLIT DATA (INI YANG KAMU MINTA)
# # =========================================================
# print("✂️ Melakukan Split Data (Train < 2024, Test >= 2024)...")

# train = df_full[df_full['TahunBulan'] < '2024-01-01']
# test = df_full[df_full['TahunBulan'] >= '2024-01-01']

# # Hapus kolom target dan kolom waktu datetime dari fitur X
# # Kita sisakan 'year', 'month' (angka) sebagai pengganti TahunBulan
# X_train = train.drop(columns=['jumEks','TahunBulan'])
# y_train = train['jumEks']

# X_test = test.drop(columns=['jumEks','TahunBulan'])
# y_test = test['jumEks']

# # Pastikan urutan kolom sesuai untuk training
# feature_cols = ['year', 'month', 'kategoriNama', 'propNama', 'gudangNama'] + \
#                [f'lag_{i}' for i in range(1, 13)] + ['rolling_3', 'rolling_6', 'rolling_12']

# X_train = X_train[feature_cols]
# X_test = X_test[feature_cols]

# # 6. TRAINING MODEL
# print(f"🧠 Melatih XGBoost pada {len(X_train)} data latih...")
# model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=3)

# model.fit(X_train, y_train)
# # =========================================================
# # 7. EVALUASI (TAMBAHAN REVISI: MAE PER BULAN)
# # =========================================================
# print("📊 Mengevaluasi Model pada Data Test (2024)...")
# y_pred = model.predict(X_test)
# y_pred = np.maximum(0, y_pred) # Pastikan tidak negatif

# # Simpan hasil prediksi ke dalam dataframe test untuk dianalisis per bulan
# test_analysis = X_test.copy()
# test_analysis['Aktual'] = y_test.values
# test_analysis['Prediksi'] = y_pred

# # Hitung MAE Global
# mae_global = mean_absolute_error(y_test, y_pred)
# r2_global = r2_score(y_test, y_pred)

# print("\n" + "="*40)
# print(f" HASIL EVALUASI GLOBAL:")
# print(f"   MAE Keseluruhan : {mae_global:.2f}")
# print(f"   R2 Score        : {r2_global:.3f}")
# print("="*40)

# # --- INI BAGIAN REVISI: HITUNG MAE PER BULAN ---
# print("\n🔍 ANALISIS MAE PER BULAN (Permintaan Dosen):")
# print(f"{'Bulan':<15} | {'MAE':<10} | {'Jumlah Data':<12}")
# print("-" * 43)

# # mae_bulanan_dict = {}

# # Daftar nama bulan untuk tampilan
# nama_bulan = {
#     1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 
#     5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus", 
#     9: "September", 10: "Oktober", 11: "November", 12: "Desember"
# }

# # for m in range(1, 13):
# #     # Filter data berdasarkan bulan
# #     data_bulan = test_analysis[test_analysis['month'] == m]
    
# #     if not data_bulan.empty:
# #         mae_m = mean_absolute_error(data_bulan['Aktual'], data_bulan['Prediksi'])
# #         mae_bulanan_dict[m] = round(mae_m, 2)
# #         print(f"{nama_bulan[m]:<15} | {mae_m:<10.2f} | {len(data_bulan):<12}")
# #     else:
# #         print(f"{nama_bulan[m]:<15} | {'No Data':<10} | {0:<12}")

# # # Simpan MAE Bulanan ke file agar bisa dibaca oleh Flask (API)
# # joblib.dump(mae_bulanan_dict, 'mae_bulanan.pkl')
# # print("-" * 43)
# # print("💾 File 'mae_bulanan.pkl' berhasil disimpan untuk digunakan di Flask.")
# # print("="*40)

# # # Hitung MAE per kombinasi + bulan
# # mae_detail = {}

# # for (kategori, provinsi, gudang), group in test_analysis.groupby(['kategoriNama', 'propNama', 'gudangNama']):
# #     for m in range(1, 13):
# #         data_combo_bulan = group[group['month'] == m]
        
# #         if not data_combo_bulan.empty:
# #             mae_combo = mean_absolute_error(
# #                 data_combo_bulan['Aktual'], 
# #                 data_combo_bulan['Prediksi']
# #             )
            
# #             # Key: (kategori, provinsi, gudang, bulan)
# #             mae_detail[(kategori, provinsi, gudang, m)] = mae_combo

# # joblib.dump(mae_detail, 'mae_detail_per_kombinasi.pkl')
# mae_detail = {}

# for (kategori, provinsi, gudang), group in test_analysis.groupby(['kategoriNama', 'propNama', 'gudangNama']):
#     for m in range(1, 13):
#         data_combo_bulan = group[group['month'] == m]
        
#         # HANYA hitung kalau data >= 3 (lebih reliable)
#         if len(data_combo_bulan) >= 3:
#             mae_combo = mean_absolute_error(
#                 data_combo_bulan['Aktual'], 
#                 data_combo_bulan['Prediksi']
#             )
            
#             mae_detail[(kategori, provinsi, gudang, m)] = mae_combo

# joblib.dump(mae_detail, 'mae_detail_per_kombinasi2.pkl')
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sqlalchemy import create_engine
import joblib 
import os

# --- KONEKSI DB ---
DB_USER = 'root'
DB_PASS = ''
DB_HOST = 'localhost'
DB_NAME = 'kanisius'
db_connection_str = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
db_connection = create_engine(db_connection_str)

print("⏳ Sedang memproses data... (Mohon tunggu)")

# 1. LOAD DATA
df = pd.read_sql("SELECT * FROM data", db_connection)
df.rename(columns={'tahunBulan': 'TahunBulan'}, inplace=True)

# 2. PREPROCESSING
df['TahunBulan'] = pd.to_datetime(df['TahunBulan'])
df['jumEks'] = pd.to_numeric(df['jumEks'], errors='coerce').fillna(0)
df.replace('\\N', np.nan, inplace=True)
df['gudangNama'] = df['gudangNama'].fillna('Unknown')
df['propNama'] = df['propNama'].fillna('Unknown')

# Filter Aktif
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

# 3. FEATURE ENGINEERING
for lag in range(1, 13):
    df_full[f'lag_{lag}'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks'].shift(lag)

df_full['rolling_3'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks'].transform(lambda x: x.rolling(3).mean().shift(1))
df_full['rolling_6'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks'].transform(lambda x: x.rolling(6).mean().shift(1))
df_full['rolling_12'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks'].transform(lambda x: x.rolling(12).mean().shift(1))

df_full['month'] = df_full['TahunBulan'].dt.month
df_full['year'] = df_full['TahunBulan'].dt.year

# Fill NaNs created by lags
cols_to_fill = [f'lag_{i}' for i in range(1, 13)] + ['rolling_3', 'rolling_6', 'rolling_12']
df_full[cols_to_fill] = df_full[cols_to_fill]

# 4. ENCODING
le_kategori = LabelEncoder()
le_gudang = LabelEncoder()
le_prov = LabelEncoder()

df_full['kategoriNama'] = le_kategori.fit_transform(df_full['kategoriNama'].astype(str))
df_full['gudangNama'] = le_gudang.fit_transform(df_full['gudangNama'].astype(str))
df_full['propNama'] = le_prov.fit_transform(df_full['propNama'].astype(str))

# Simpan Encoders
print("💾 Menyimpan Encoders...")
joblib.dump({'kategori': le_kategori, 'gudang': le_gudang, 'provinsi': le_prov}, 'encoders.pkl')

# 5. SPLIT DATA
print("✂️ Melakukan Split Data (Train < 2024, Test >= 2024)...")

train = df_full[df_full['TahunBulan'] < '2024-01-01']
test = df_full[df_full['TahunBulan'] >= '2024-01-01']

X_train = train.drop(columns=['jumEks','TahunBulan'])
y_train = train['jumEks']

X_test = test.drop(columns=['jumEks','TahunBulan'])
y_test = test['jumEks']

feature_cols = ['year', 'month', 'kategoriNama', 'propNama', 'gudangNama'] + \
               [f'lag_{i}' for i in range(1, 13)] + ['rolling_3', 'rolling_6', 'rolling_12']

X_train = X_train[feature_cols]
X_test = X_test[feature_cols]

# 6. TRAINING MODEL
print(f"🧠 Melatih XGBoost pada {len(X_train)} data latih...")
model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=3)
model.fit(X_train, y_train)

# 7. EVALUASI
print("📊 Mengevaluasi Model pada Data Test (2024)...")
y_pred = model.predict(X_test)
y_pred = np.maximum(0, y_pred)

test_analysis = X_test.copy()
test_analysis['Aktual'] = y_test.values
test_analysis['Prediksi'] = y_pred

mae_global = mean_absolute_error(y_test, y_pred)
r2_global = r2_score(y_test, y_pred)

print("\n" + "="*60)
print(f" HASIL EVALUASI GLOBAL:")
print(f"   MAE Keseluruhan : {mae_global:.2f}")
print(f"   R2 Score        : {r2_global:.3f}")
print("="*60)

# =========================================================
# STRATEGI 3-TIER MAE: Kombinasi → Kategori → Global
# =========================================================
print("\n🎯 Menghitung MAE dengan Strategi 3-Tier...")

# TIER 1: MAE Per Kombinasi Lengkap (Kategori + Provinsi + Gudang + Bulan)
mae_detail_full = {}
stats_tier1 = {'valid': 0, 'filtered_outlier': 0, 'filtered_sample': 0}

for (kategori, provinsi, gudang), group in test_analysis.groupby(['kategoriNama', 'propNama', 'gudangNama']):
    for m in range(1, 13):
        data_combo = group[group['month'] == m]
        
        if len(data_combo) >= 1:  # Minimal 1 data
            mae_val = mean_absolute_error(data_combo['Aktual'], data_combo['Prediksi'])
            avg_pred = data_combo['Prediksi'].mean()
            
            # Filter outlier ekstrem (MAE > 300% dari prediksi)
            if avg_pred > 0 and mae_val / avg_pred <= 3.0:
                mae_detail_full[(kategori, provinsi, gudang, m)] = round(mae_val, 2)
                stats_tier1['valid'] += 1
            else:
                stats_tier1['filtered_outlier'] += 1
        else:
            stats_tier1['filtered_sample'] += 1

# TIER 2: MAE Per Kategori + Bulan (Abaikan Provinsi & Gudang)
mae_kategori_bulan = {}
stats_tier2 = {'valid': 0}

for (kategori, bulan), group in test_analysis.groupby(['kategoriNama', 'month']):
    if len(group) >= 3:  # Minimal 3 sample untuk lebih reliable
        mae_val = mean_absolute_error(group['Aktual'], group['Prediksi'])
        mae_kategori_bulan[(kategori, bulan)] = round(mae_val, 2)
        stats_tier2['valid'] += 1

# TIER 3: MAE Global Per Bulan
mae_bulanan_global = {}
nama_bulan = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus", 
    9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}

print("\n📅 TIER 3 - MAE Global per Bulan:")
print(f"{'Bulan':<15} | {'MAE':<10} | {'Sample':<8}")
print("-" * 40)

for m in range(1, 13):
    data_bulan = test_analysis[test_analysis['month'] == m]
    if not data_bulan.empty:
        mae_m = mean_absolute_error(data_bulan['Aktual'], data_bulan['Prediksi'])
        mae_bulanan_global[m] = round(mae_m, 2)
        print(f"{nama_bulan[m]:<15} | {mae_m:<10.2f} | {len(data_bulan):<8}")

# Simpan semua tier
joblib.dump(mae_detail_full, 'mae_tier1_full.pkl')
joblib.dump(mae_kategori_bulan, 'mae_tier2_kategori.pkl')
joblib.dump(mae_bulanan_global, 'mae_tier3_global.pkl')

print("\n" + "="*60)
print(" STATISTIK 3-TIER MAE:")
print("="*60)
print(f" TIER 1 (Kombinasi Lengkap):")
print(f"   - Valid          : {stats_tier1['valid']}")
print(f"   - Filtered       : {stats_tier1['filtered_outlier'] + stats_tier1['filtered_sample']}")

print(f"\n TIER 2 (Kategori + Bulan):")
print(f"   - Valid          : {stats_tier2['valid']}")

print(f"\n TIER 3 (Global per Bulan):")
print(f"   - Valid          : {len(mae_bulanan_global)} bulan")

# Statistik MAE Tier 1
if mae_detail_full:
    mae_values = list(mae_detail_full.values())
    print(f"\n MAE TIER 1 Statistics:")
    print(f"   - Minimum        : {min(mae_values):.2f}")
    print(f"   - Maximum        : {max(mae_values):.2f}")
    print(f"   - Rata-rata      : {np.mean(mae_values):.2f}")
    print(f"   - Median         : {np.median(mae_values):.2f}")

print("\n✅ File berhasil disimpan:")
print("   - mae_tier1_full.pkl (MAE kombinasi lengkap)")
print("   - mae_tier2_kategori.pkl (MAE kategori+bulan)")
print("   - mae_tier3_global.pkl (MAE global per bulan)")
print("="*60)