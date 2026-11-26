import sys
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, request, send_from_directory
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
DATASET_DIR = BASE_DIR / "dataset"
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"

sys.path.insert(0, str(SRC_DIR))

from prediction import load_model, predict_url

app = Flask(__name__, static_folder=str(FRONTEND_DIST), static_url_path="")


def validate_url(url):
    if not url or not url.strip():
        return "URL tidak boleh kosong."
    if any(char.isspace() for char in url):
        return "URL tidak boleh mengandung spasi."
    if not url.startswith(("http://", "https://")):
        return "URL harus menggunakan http:// atau https://."
    return None


@app.get("/")
def index():
    if (FRONTEND_DIST / "index.html").exists():
        return send_from_directory(FRONTEND_DIST, "index.html")
    return (
        "Frontend Vue belum dibangun. Jalankan: cd frontend && npm.cmd install "
        "&& npm.cmd run build",
        404,
    )


@app.get("/assets/<path:filename>")
def frontend_assets(filename):
    return send_from_directory(FRONTEND_DIST / "assets", filename)


@app.get("/api/dataset")
def dataset_summary():
    raw_path = DATASET_DIR / "Dataset.csv"
    clean_path = DATASET_DIR / "cleaned_dataset.csv"

    if not raw_path.exists() or not clean_path.exists():
        return jsonify({"error": "Dataset belum tersedia."}), 404

    raw = pd.read_csv(raw_path, usecols=["label"])
    clean = pd.read_csv(clean_path, usecols=["label"])
    counts = clean["label"].value_counts()

    return jsonify(
        {
            "raw_total": len(raw),
            "clean_total": len(clean),
            "removed": len(raw) - len(clean),
            "benign": int(counts.get(0, 0)),
            "phishing": int(counts.get(1, 0)),
        }
    )


@app.post("/api/predict")
def predict():
    url = (request.get_json(silent=True) or {}).get("url", "").strip()
    error = validate_url(url)
    if error:
        return jsonify({"error": error}), 400

    try:
        result = predict_url(url)
        return jsonify(result)
    except FileNotFoundError as error:
        return jsonify({"error": str(error)}), 404
    except Exception as error:
        return jsonify({"error": f"Gagal menganalisis URL: {error}"}), 500


@app.get("/api/evaluation")
def evaluation():
    dataset_path = DATASET_DIR / "cleaned_dataset.csv"
    if not dataset_path.exists():
        return jsonify({"error": "cleaned_dataset.csv tidak ditemukan."}), 404

    try:
        artifact = load_model()
        model = artifact["model"]
        feature_columns = artifact["feature_columns"]

        df = pd.read_csv(dataset_path)
        X = df[feature_columns]
        y = df["label"]

        _, X_test, _, y_test = train_test_split(
            X, y, test_size=0.20, random_state=42, stratify=y
        )

        y_pred = model.predict(X_test)
        matrix = confusion_matrix(y_test, y_pred, labels=[0, 1])
        tn, fp, fn, tp = matrix.ravel()

        return jsonify(
            {
                "accuracy": float(accuracy_score(y_test, y_pred)),
                "precision": float(
                    precision_score(y_test, y_pred, pos_label=1, zero_division=0)
                ),
                "recall": float(
                    recall_score(y_test, y_pred, pos_label=1, zero_division=0)
                ),
                "f1": float(f1_score(y_test, y_pred, pos_label=1, zero_division=0)),
                "test_total": len(y_test),
                "matrix": matrix.tolist(),
                "tn": int(tn),
                "fp": int(fp),
                "fn": int(fn),
                "tp": int(tp),
            }
        )
    except FileNotFoundError as error:
        return jsonify({"error": str(error)}), 404
    except Exception as error:
        return jsonify({"error": f"Gagal mengevaluasi model: {error}"}), 500


@app.get("/api/feature-importance")
def feature_importance():
    try:
        artifact = load_model()
        model = artifact["model"]
        feature_columns = artifact["feature_columns"]
        features = [
            {"feature": feature, "importance": float(importance)}
            for feature, importance in sorted(
                zip(feature_columns, model.feature_importances_),
                key=lambda item: item[1],
                reverse=True,
            )
        ]
        return jsonify(features)
    except FileNotFoundError as error:
        return jsonify({"error": str(error)}), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
