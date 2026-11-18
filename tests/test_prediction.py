import sys
from pathlib import Path

import pytest

# Memastikan folder src dapat ditemukan
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from prediction import predict_url

# ==========================================
# TEST PREDIKSI URL
# ==========================================


@pytest.mark.parametrize(
    "url",
    [
        "https://www.google.com/",
        "https://www.example.com/login",
        "http://192.168.1.1/login",
        "https://example.com/login?id=123",
        "http://example.com/verify-account",
    ],
)
def test_prediction_returns_valid_result(url):

    result = predict_url(url)

    # Memastikan struktur hasil prediksi
    assert "prediction" in result
    assert "label" in result
    assert "probability" in result
    assert "features" in result

    # Memastikan label valid
    assert result["prediction"] in [0, 1]
    assert result["label"] in ["Benign", "Phishing"]

    # Memastikan hasil prediksi sesuai label
    if result["prediction"] == 1:
        assert result["label"] == "Phishing"
    else:
        assert result["label"] == "Benign"

    # Memastikan skor berada dalam rentang 0-1
    assert 0 <= result["probability"] <= 1

    # Memastikan seluruh 22 fitur tersedia
    assert len(result["features"]) == 22


# ==========================================
# TEST KONSISTENSI PREDIKSI
# ==========================================


def test_prediction_is_consistent():

    url = "https://www.google.com/"

    first_result = predict_url(url)
    second_result = predict_url(url)

    assert first_result["prediction"] == second_result["prediction"]
    assert first_result["label"] == second_result["label"]
    assert first_result["probability"] == second_result["probability"]
