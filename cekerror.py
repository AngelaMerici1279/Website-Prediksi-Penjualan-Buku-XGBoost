import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
from sklearn.preprocessing import LabelEncoder
import os

print("🚀 MEMULAI TRAINING LOKAL...")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. LOAD DATA MENTAH
csv_path = os.path.join(BASE_DIR, 'dataKategoriNama.csv')
if not os.path.exists(csv_path):
    print("❌ ERROR: File 'dataKategoriNama.csv' tidak ditemukan!")
    print("   -> Tolong copy file csv data mentah ke folder ini dulu.")
    exit()

df = pd.read_csv(csv_path, sep=';')
df['TahunBulan'] = pd.to_datetime(df['TahunBulan'])

# 2. PREPROCESSING (Sama persis dengan Colab)
# Agregasi per Kategori & Provinsi
df_agg = df.groupby(['kategoriNama', 'propNama', 'TahunBulan'])['jumEks'].sum().reset_index()

# Filter data aktif (minimal 12 bulan)
aktif = df_agg.groupby(['kategoriNama', 'propNama']).filter(lambda x: len(x) >= 12)

# Lengkapi Bulan Kosong
def lengkapi_bulan(df_in):
    list_dfs = []
    for (k, p), g in df_in.groupby(['kategoriNama', 'propNama']):
        all_dates = pd.date_range(g['TahunBulan'].min(), g['TahunBulan'].max(), freq='MS')
        temp = pd.DataFrame({'kategoriNama': k, 'propNama': p, 'TahunBulan': all_dates})
        temp = temp.merge(g, on=['kategoriNama','propNama','TahunBulan'], how='left')
        list_dfs.append(temp)
    return pd.concat(list_dfs).fillna(0)

print("   -> Sedang merapikan data...")
df_full = lengkapi_bulan(aktif).sort_values(['kategoriNama', 'propNama', 'TahunBulan'])

# 3. FEATURE ENGINEERING
print("   -> Membuat fitur AI (Lag & Rolling)...")
for i in range(1, 13):
    df_full[f'lag_{i}'] = df_full.groupby(['kategoriNama','propNama'])['jumEks'].shift(i)

df_full['rolling_3'] = df_full.groupby(['kategoriNama','propNama'])['jumEks'].transform(lambda x: x.shift(1).rolling(3).mean())
df_full['rolling_6'] = df_full.groupby(['kategoriNama','propNama'])['jumEks'].transform(lambda x: x.shift(1).rolling(6).mean())
df_full['rolling_12'] = df_full.groupby(['kategoriNama','propNama'])['jumEks'].transform(lambda x: x.shift(1).rolling(12).mean())

df_full['year'] = df_full['TahunBulan'].dt.year
df_full['month'] = df_full['TahunBulan'].dt.month
df_full['sin_month'] = np.sin(2 * np.pi * df_full['month']/12)
df_full['cos_month'] = np.cos(2 * np.pi * df_full['month']/12)

# Encoding
le_kat = LabelEncoder()
le_prov = LabelEncoder()
df_full['kategoriCode'] = le_kat.fit_transform(df_full['kategoriNama'])
df_full['propCode'] = le_prov.fit_transform(df_full['propNama'])

# Hapus NaN (12 bulan pertama)
df_ready = df_full.dropna()

# 4. TRAINING XGBOOST
print("   -> Melatih Otak Model (XGBoost)...")
features = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5', 'lag_6', 'lag_7', 
            'lag_8', 'lag_9', 'lag_10', 'lag_11', 'lag_12', 
            'rolling_3', 'rolling_6', 'rolling_12', 
            'year', 'month', 'sin_month', 'cos_month', 'kategoriCode', 'propCode']

X = df_ready[features]
y = df_ready['jumEks']

model = xgb.XGBRegressor(
    n_estimators=500,
    learning_rate=0.03,
    max_depth=5,
    objective='reg:tweedie',
    tweedie_variance_power=1.5,
    n_jobs=-1
)
model.fit(X, y)

# 5. SIMPAN HASIL (Langsung di laptop!)
print("   -> Menyimpan file...")
model.save_model(os.path.join(BASE_DIR, "model_final.json"))
joblib.dump(le_kat, os.path.join(BASE_DIR, "encoder_kategori.pkl"))
joblib.dump(le_prov, os.path.join(BASE_DIR, "encoder_provinsi.pkl"))

# Simpan History Terbaru (Penting buat app.py)
last_data = df_ready[df_ready['TahunBulan'] >= '2023-01-01'].copy()
last_data.to_csv(os.path.join(BASE_DIR, "data_history_terakhir.csv"), index=False)

print("\n✅ TRAINING SELESAI!")
print("Sekarang model di laptopmu sudah 100% cocok dengan library laptopmu.")
print("Silakan restart app.py dan coba lagi.")