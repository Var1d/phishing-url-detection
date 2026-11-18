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

    test_urls = [
        "https://www.google.com/",
        "https://www.example.com/login",
        "http://192.168.1.1/login",
        "https://example.com/login?id=123",
        "http://example.com/verify-account"
    ]

    for url in test_urls:
        print("\n" + "=" * 50)

        try:
            result = predict_url(url)

            print("URL:", url)
            print("Prediksi:", result["label"])
            print(
                "Probabilitas:",
                f"{result['probability'] * 100:.2f}%"
            )

        except Exception as error:
            print("Error:", error)