import joblib
import pandas as pd

from pathlib import Path
from feature_extraction import extract_features

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "random_forest.pkl"


def load_model():
    """
    Memuat model Random Forest.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model belum tersedia. Jalankan model_training.py.")

    return joblib.load(MODEL_PATH)


def predict_url(url):
    """
    Melakukan prediksi terhadap URL baru.
    """

    artifact = load_model()

    model = artifact["model"]
    feature_columns = artifact["feature_columns"]

    features = extract_features(url)

    input_data = pd.DataFrame([features], columns=feature_columns)

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    class_probabilities = dict(zip(model.classes_, probabilities))

    result = {
        "prediction": int(prediction),
        "label": ("Phishing" if prediction == 1 else "Benign"),
        "probability": float(class_probabilities[prediction]),
        "features": features,
    }

    return result


if __name__ == "__main__":

    test_url = "https://www.example.com/login"

    result = predict_url(test_url)

    print("\n=== HASIL PREDIKSI ===")
    print("URL:", test_url)
    print("Prediksi:", result["label"])
    print("Probabilitas:", f"{result['probability'] * 100:.2f}%")
