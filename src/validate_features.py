
import sys
from pathlib import Path

import pandas as pd
import numpy as np

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent)
)

from feature_extraction import extract_features


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "dataset" / "cleaned_dataset.csv"

df = pd.read_csv(DATASET_PATH)

# Ambil sampel seimbang dari kedua kelas
samples = (
    df.groupby("label", group_keys=False)
    .apply(
        lambda group: group.sample(
            n=250,
            random_state=42
        )
    )
)

feature_columns = [
    col for col in df.columns
    if col not in ["url", "dom", "tld", "label"]
]

mismatch_counts = {
    col: 0 for col in feature_columns
}

error_count = 0
total_checked = 0

print("Memulai validasi 500 URL...")

for _, row in samples.iterrows():

    try:
        extracted = extract_features(row["url"])

        total_checked += 1

        for feature in feature_columns:

            original = float(row[feature])
            generated = float(extracted[feature])

            if not np.isclose(
                original,
                generated,
                rtol=0,
                atol=1e-6
            ):
                mismatch_counts[feature] += 1

    except Exception as error:

        error_count += 1

        print("\nURL gagal diproses:")
        print(row["url"])
        print("Error:", error)


print("\n=== HASIL VALIDASI ===")

print("Jumlah sampel:", len(samples))
print("Berhasil diperiksa:", total_checked)
print("Gagal diproses:", error_count)

print("\n=== PERBEDAAN FITUR ===")

for feature, count in mismatch_counts.items():

    print(f"{feature:15}: {count}")

total_mismatches = sum(mismatch_counts.values())

print("\nTotal ketidaksesuaian:", total_mismatches)

if error_count == 0 and total_mismatches == 0:

    print("\nSEMUA FITUR COCOK!")

else:

    print("\nDITEMUKAN PERBEDAAN. PERLU INVESTIGASI.")
