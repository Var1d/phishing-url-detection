import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from prediction import load_model

# PATH
BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "dataset" / "cleaned_dataset.csv"
OUTPUT_DIR = BASE_DIR / "evaluation"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# MEMUAT DATA DAN MODEL
print("Memuat dataset dan model...")

df = pd.read_csv(DATASET_PATH)

artifact = load_model()

model = artifact["model"]
feature_columns = artifact["feature_columns"]

X = df[feature_columns]
y = df["label"]

# MEMBAGI DATA TRAINING DAN TESTING
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# Mengambil URL asli sesuai indeks data testing
test_urls = df.loc[X_test.index, "url"]

# MELAKUKAN PREDIKSI
print("Melakukan prediksi pada data testing...")

predictions = model.predict(X_test)

probabilities = model.predict_proba(X_test)

# Mencari posisi kelas Phishing (label 1)
phishing_index = list(model.classes_).index(1)

phishing_probabilities = probabilities[:, phishing_index]

# MEMBUAT TABEL HASIL
results = pd.DataFrame(
    {
        "URL": test_urls.values,
        "Actual Label": y_test.values,
        "Predicted Label": predictions,
        "Phishing Score": phishing_probabilities,
    }
)

results["Actual Label"] = results["Actual Label"].map({0: "Benign", 1: "Phishing"})

results["Predicted Label"] = results["Predicted Label"].map(
    {0: "Benign", 1: "Phishing"}
)

# MENGIDENTIFIKASI KESALAHAN
false_positive = results[
    (results["Actual Label"] == "Benign") & (results["Predicted Label"] == "Phishing")
]

false_negative = results[
    (results["Actual Label"] == "Phishing") & (results["Predicted Label"] == "Benign")
]

# Menggabungkan seluruh kesalahan
misclassified = pd.concat(
    [
        false_positive.assign(Error_Type="False Positive"),
        false_negative.assign(Error_Type="False Negative"),
    ]
)

# MENAMPILKAN HASIL
print("\n" + "=" * 50)
print("HASIL ANALISIS KESALAHAN MODEL")
print("=" * 50)

print("Total data testing:", len(results))
print("False Positive:", len(false_positive))
print("False Negative:", len(false_negative))
print("Total kesalahan:", len(misclassified))

print("\n--- CONTOH FALSE POSITIVE ---")

if len(false_positive) > 0:
    print(
        false_positive[["URL", "Actual Label", "Predicted Label", "Phishing Score"]]
        .head(10)
        .to_string(index=False)
    )
else:
    print("Tidak ditemukan False Positive.")

print("\n--- CONTOH FALSE NEGATIVE ---")

if len(false_negative) > 0:
    print(
        false_negative[["URL", "Actual Label", "Predicted Label", "Phishing Score"]]
        .head(10)
        .to_string(index=False)
    )
else:
    print("Tidak ditemukan False Negative.")

# MENYIMPAN HASIL
output_path = OUTPUT_DIR / "misclassified_urls.csv"

misclassified.to_csv(output_path, index=False)

print("\nHasil kesalahan disimpan di:")
print(output_path)
