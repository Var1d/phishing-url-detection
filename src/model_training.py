import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

# 1. MENENTUKAN LOKASI FILE
BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "dataset" / "cleaned_dataset.csv"
MODEL_PATH = BASE_DIR / "models" / "random_forest.pkl"

# 2. MEMBACA DATASET
print("Membaca dataset...")

df = pd.read_csv(DATASET_PATH)

# Kolom yang tidak digunakan sebagai fitur
excluded_columns = ["url", "dom", "tld", "label"]

feature_columns = [col for col in df.columns if col not in excluded_columns]

X = df[feature_columns]
y = df["label"]

print("\n=== INFORMASI DATA ===")
print("Jumlah data:", len(df))
print("Jumlah fitur:", len(feature_columns))
print("Distribusi label:")
print(y.value_counts())

# 3. MEMBAGI DATASET
print("\nMembagi dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print("\n=== HASIL PEMBAGIAN DATA ===")
print("Training:", len(X_train))
print("Testing:", len(X_test))

# 4. MEMBUAT MODEL RANDOM FOREST
print("\nMembuat model Random Forest...")

model = RandomForestClassifier(
    n_estimators=200, random_state=42, class_weight="balanced", n_jobs=-1
)

# 5. MELATIH MODEL
print("\nMemulai training model...")

model.fit(X_train, y_train)

print("Training selesai!")

# 6. MELAKUKAN PREDIKSI
print("\nMelakukan prediksi pada data testing...")

y_pred = model.predict(X_test)

# 7. EVALUASI MODEL
accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(y_test, y_pred, pos_label=1, zero_division=0)

recall = recall_score(y_test, y_pred, pos_label=1, zero_division=0)

f1 = f1_score(y_test, y_pred, pos_label=1, zero_division=0)

print("\n=== HASIL EVALUASI MODEL ===")

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1-Score : {f1:.4f}")

print("\n=== CLASSIFICATION REPORT ===")

print(
    classification_report(
        y_test, y_pred, target_names=["Benign", "Phishing"], zero_division=0
    )
)

# 8. CONFUSION MATRIX
cm = confusion_matrix(y_test, y_pred, labels=[0, 1])

tn, fp, fn, tp = cm.ravel()

print("\n=== CONFUSION MATRIX ===")

print("True Negative :", tn)
print("False Positive:", fp)
print("False Negative:", fn)
print("True Positive :", tp)

# 9. FEATURE IMPORTANCE
importance = pd.DataFrame(
    {"Feature": feature_columns, "Importance": model.feature_importances_}
)

importance = importance.sort_values(by="Importance", ascending=False)

print("\n=== TOP 10 FEATURE IMPORTANCE ===")
print(importance.head(10).to_string(index=False))

# 10. MENYIMPAN MODEL
artifact = {"model": model, "feature_columns": feature_columns}

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(artifact, MODEL_PATH)

print("\nModel berhasil disimpan!")
print("Lokasi:", MODEL_PATH)
