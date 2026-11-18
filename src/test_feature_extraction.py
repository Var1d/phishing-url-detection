import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from feature_extraction import extract_features

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "dataset" / "Dataset.csv"

df = pd.read_csv(DATASET_PATH)

# Ambil satu contoh URL dari dataset
sample = df.iloc[0]

original_url = sample["url"]

extracted_features = extract_features(original_url)

print("URL:", original_url)

print("\n=== PERBANDINGAN FITUR ===")

for feature, extracted_value in extracted_features.items():

    original_value = sample[feature]

    if isinstance(original_value, float):
        match = abs(original_value - extracted_value) < 1e-6
    else:
        match = original_value == extracted_value

    status = "COCOK" if match else "BERBEDA"

    print(
        f"{feature:15} | "
        f"Dataset: {original_value} | "
        f"Program: {extracted_value} | "
        f"{status}"
    )
