import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from sklearn.multioutput import MultiOutputRegressor # <--- INI KUNCINYA
from sqlalchemy import create_engine
import joblib 
import os

# ==========================================
# KONFIGURASI DATABASE
# ==========================================
DB_USER = 'root'
DB_PASS = ''
DB_HOST = 'localhost'
DB_NAME = 'kanisius'
db_connection_str = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
db_connection = create_engine(db_connection_str)

print("🚀 Memulai Training DIRECT STRATEGY (12 Bulan Sekaligus)...")

# 1. LOAD DATA
print("⏳ Mengambil data dari database...")
df = pd.read_sql("SELECT * FROM data", db_connection)
df.rename(columns={'tahunBulan': 'TahunBulan'}, inplace=True) # Jaga-jaga kalau di DB huruf kecil

# 2. PREPROCESSING DASAR
df['TahunBulan'] = pd.to_datetime(df['TahunBulan'])
df['jumEks'] = pd.to_numeric(df['jumEks'], errors='coerce').fillna(0)
df.replace('\\N', np.nan, inplace=True)
df['gudangNama'] = df['gudangNama'].fillna('Unknown')
df['propNama'] = df['propNama'].fillna('Unknown')

# Filter Aktif (Minimal 12 bulan data)
aktif = df[df['jumEks'] > 0].groupby(['kategoriNama', 'gudangNama', 'propNama']).filter(lambda x: len(x) >= 12)

# Lengkapi Bulan (Resampling)
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

# 3. FEATURE ENGINEERING (INPUT X)
print("⚙️ Membuat Fitur (Lags, Rolling, Date)...")
for lag in range(1, 13):
    df_full[f'lag_{lag}'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks'].shift(lag)

df_full['rolling_3'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks'].transform(lambda x: x.rolling(3).mean().shift(1))
df_full['rolling_6'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks'].transform(lambda x: x.rolling(6).mean().shift(1))
df_full['rolling_12'] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks'].transform(lambda x: x.rolling(12).mean().shift(1))

df_full['month'] = df_full['TahunBulan'].dt.month
df_full['year'] = df_full['TahunBulan'].dt.year
df_full['sin_month'] = np.sin(2 * np.pi * df_full['month'] / 12)
df_full['cos_month'] = np.cos(2 * np.pi * df_full['month'] / 12)

# Isi NaN hasil lag dengan 0
cols_to_fill = [f'lag_{i}' for i in range(1, 13)] + ['rolling_3', 'rolling_6', 'rolling_12']
df_full[cols_to_fill] = df_full[cols_to_fill].fillna(0)

# 4. ENCODING
le_kategori = LabelEncoder()
le_gudang = LabelEncoder()
le_prov = LabelEncoder()

df_full['kategoriNama'] = le_kategori.fit_transform(df_full['kategoriNama'].astype(str))
df_full['gudangNama'] = le_gudang.fit_transform(df_full['gudangNama'].astype(str))
df_full['propNama'] = le_prov.fit_transform(df_full['propNama'].astype(str))

# Simpan Encoders
joblib.dump({'kategori': le_kategori, 'gudang': le_gudang, 'provinsi': le_prov}, 'encoders.pkl')

# =========================================================
# 5. MENYIAPKAN TARGET (Y) UNTUK DIRECT STRATEGY
# =========================================================
print("🎯 Menyiapkan Target Multi-Output (12 Bulan ke depan)...")

# Kita buat 12 kolom target: target_1 (bulan depan), target_2 (2 bulan lagi), dst...
target_cols = []
for i in range(1, 13):
    col_name = f'target_next_{i}'
    df_full[col_name] = df_full.groupby(['kategoriNama','gudangNama','propNama'])['jumEks'].shift(-i)
    target_cols.append(col_name)

# Hapus baris paling akhir yang targetnya jadi NaN (karena di-shift ke atas)
df_clean = df_full.dropna(subset=target_cols)

# Definisikan Fitur X (Kondisi Saat Ini)
feature_cols = ['year', 'month', 'kategoriNama', 'propNama', 'gudangNama', 'sin_month', 'cos_month'] + \
               [f'lag_{i}' for i in range(1, 13)] + ['rolling_3', 'rolling_6', 'rolling_12']

X = df_clean[feature_cols]
y = df_clean[target_cols] # Y isinya 12 kolom sekaligus

# 6. TRAINING
print(f"🧠 Melatih Model pada {len(X)} baris data...")

# Gunakan MultiOutputRegressor
# Ini otomatis membungkus XGBoost jadi 12 model terpisah
model_direct = MultiOutputRegressor(xgb.XGBRegressor(
    n_estimators=300, 
    learning_rate=0.05, 
    max_depth=5,  # Naikkan dikit biar lebih pintar
))

model_direct.fit(X, y)

# 7. SIMPAN MODEL
print("💾 Menyimpan Model Direct...")
# Kita pakai joblib karena MultiOutputRegressor bukan native XGBoost object
joblib.dump(model_direct, "model_direct_sales.pkl") 

print("✅ Selesai! Jalankan app.py sekarang.")