import pandas as pd
from pathlib import Path

# 1. MENENTUKAN LOKASI DATASET
BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "dataset" / "Dataset.csv"
OUTPUT_PATH = BASE_DIR / "dataset" / "cleaned_dataset.csv"

# 2. MEMBACA DATASET
print("Membaca dataset...")

df = pd.read_csv(DATASET_PATH)

print("\n=== INFORMASI DATASET AWAL ===")
print("Jumlah baris:", len(df))
print("Jumlah kolom:", len(df.columns))
print("\nDaftar kolom:")
print(df.columns.tolist())

# 3. MEMERIKSA DISTRIBUSI LABEL
print("\n=== DISTRIBUSI LABEL AWAL ===")

print(df["label"].value_counts())

# 4. MEMERIKSA DATA KOSONG
print("\n=== DATA KOSONG ===")

print(df.isnull().sum()[df.isnull().sum() > 0])

# 5. MEMERIKSA DATA DUPLIKAT
duplicate_count = df.duplicated(subset=["url"]).sum()

print("\nJumlah URL duplikat:", duplicate_count)

# Memastikan satu URL tidak memiliki label berbeda
conflicting_urls = (df.groupby("url")["label"].nunique() > 1).sum()

print("URL dengan label berbeda:", conflicting_urls)

if conflicting_urls > 0:
    raise ValueError(
        "Ditemukan URL dengan label berbeda. "
        "Periksa data sebelum menghapus duplikat."
    )

# 6. MEMBERSIHKAN DATA DUPLIKAT
df_clean = df.drop_duplicates(subset=["url"], keep="first").copy()

print("\n=== HASIL PEMBERSIHAN ===")
print("Jumlah data awal:", len(df))
print("Jumlah data setelah dibersihkan:", len(df_clean))
print("Data yang dihapus:", len(df) - len(df_clean))

# 7. MEMERIKSA FITUR NUMERIK
excluded_columns = ["url", "dom", "tld", "label"]

feature_columns = [col for col in df_clean.columns if col not in excluded_columns]

print("\nJumlah fitur:", len(feature_columns))
print("Fitur yang digunakan:")
print(feature_columns)

# Memastikan seluruh fitur berupa angka
X = df_clean[feature_columns]

if not all(pd.api.types.is_numeric_dtype(X[col]) for col in X.columns):
    raise ValueError("Terdapat fitur yang bukan numerik.")

# Memeriksa nilai kosong pada fitur
if X.isnull().any().any():
    raise ValueError("Terdapat nilai kosong pada fitur numerik.")

# 8. MENYIMPAN DATASET BERSIH
df_clean.to_csv(OUTPUT_PATH, index=False)

print("\nDataset berhasil dibersihkan!")
print("Disimpan di:", OUTPUT_PATH)
