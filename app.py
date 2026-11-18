import streamlit as st
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path
from urllib.parse import urlsplit
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

# ==========================================
# KONFIGURASI DAN PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"

sys.path.insert(0, str(BASE_DIR / "src"))

from prediction import predict_url, load_model

st.set_page_config(page_title="Phishing URL Detection", page_icon="🛡️", layout="wide")

# ==========================================
# VALIDASI FORMAT URL
# ==========================================


def validate_url(url):

    url = url.strip()

    if not url:
        return False, "URL tidak boleh kosong."

    if any(char.isspace() for char in url):
        return False, "URL tidak boleh mengandung spasi."

    try:
        parsed = urlsplit(url)

        if parsed.scheme.lower() not in ["http", "https"]:
            return False, "URL harus menggunakan http:// atau https://."

        if not parsed.netloc or not parsed.hostname:
            return False, "URL harus memiliki nama host atau alamat IP."

        # Memeriksa format port jika dicantumkan
        port = parsed.port

        if port is not None and not (1 <= port <= 65535):
            return False, "Nomor port tidak valid."

        if parsed.username is not None or parsed.password is not None:
            return False, "URL dengan informasi username/password tidak didukung."

    except ValueError:
        return False, "Format URL tidak valid."

    return True, "URL valid."


# ==========================================
# MEMUAT MODEL
# ==========================================


@st.cache_resource
def get_model_artifact():
    return load_model()


# ==========================================
# MEMBACA DATASET OVERVIEW
# ==========================================


@st.cache_data
def load_dataset_overview():

    raw_path = DATASET_DIR / "Dataset.csv"
    clean_path = DATASET_DIR / "cleaned_dataset.csv"

    if not raw_path.exists():
        raise FileNotFoundError("Dataset.csv tidak ditemukan.")

    if not clean_path.exists():
        raise FileNotFoundError("cleaned_dataset.csv tidak ditemukan.")

    raw_data = pd.read_csv(raw_path, usecols=["label"])
    clean_data = pd.read_csv(clean_path, usecols=["label"])

    label_counts = clean_data["label"].value_counts()

    return {
        "raw_total": len(raw_data),
        "clean_total": len(clean_data),
        "removed": len(raw_data) - len(clean_data),
        "benign": int(label_counts.get(0, 0)),
        "phishing": int(label_counts.get(1, 0)),
    }


# ==========================================
# EVALUASI MODEL SECARA OTOMATIS
# ==========================================


@st.cache_data
def calculate_model_evaluation():

    dataset_path = DATASET_DIR / "cleaned_dataset.csv"

    if not dataset_path.exists():
        raise FileNotFoundError("cleaned_dataset.csv tidak ditemukan.")

    artifact = get_model_artifact()

    model = artifact["model"]
    feature_columns = artifact["feature_columns"]

    df = pd.read_csv(dataset_path)

    X = df[feature_columns]
    y = df["label"]

    # Pembagian data harus sama dengan proses training
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # Prediksi pada data testing
    y_pred = model.predict(X_test)

    # Menghitung metrik evaluasi
    accuracy = accuracy_score(y_test, y_pred)

    precision = precision_score(y_test, y_pred, pos_label=1, zero_division=0)

    recall = recall_score(y_test, y_pred, pos_label=1, zero_division=0)

    f1 = f1_score(y_test, y_pred, pos_label=1, zero_division=0)

    matrix = confusion_matrix(y_test, y_pred, labels=[0, 1])

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "matrix": matrix,
        "test_total": len(y_test),
    }


# ==========================================
# JUDUL DAN DESKRIPSI
# ==========================================

st.title("🛡️ Phishing URL Detection System")

st.write(
    "Aplikasi berbasis Machine Learning untuk mengklasifikasikan "
    "URL menjadi **Benign** atau **Phishing** menggunakan algoritma "
    "Random Forest."
)

st.info(
    "Aplikasi menganalisis karakteristik teks URL. "
    "Aplikasi tidak membuka atau mengunjungi situs yang diperiksa."
)


# ==========================================
# DATASET OVERVIEW
# ==========================================

st.divider()
st.header("📁 Dataset Overview")

st.write(
    "Ringkasan dataset URL-Phish Version 2 " "yang digunakan dalam pengembangan model."
)

try:

    dataset_info = load_dataset_overview()

    col1, col2, col3 = st.columns(3)

    col1.metric("Dataset Awal", f'{dataset_info["raw_total"]:,}')

    col2.metric("Setelah Cleaning", f'{dataset_info["clean_total"]:,}')

    col3.metric("Baris Dihapus", f'{dataset_info["removed"]:,}')

    st.subheader("Distribusi Kelas")

    distribution = pd.DataFrame(
        {"Jumlah URL": [dataset_info["benign"], dataset_info["phishing"]]},
        index=["Benign", "Phishing"],
    )

    st.bar_chart(distribution)

    col1, col2 = st.columns(2)

    col1.metric("Benign URLs", f'{dataset_info["benign"]:,}')

    col2.metric("Phishing URLs", f'{dataset_info["phishing"]:,}')

    st.caption(
        "Dataset setelah cleaning digunakan untuk proses "
        "pelatihan dan pengujian model."
    )

except Exception as error:
    st.warning(f"Gagal membaca dataset: {error}")


# ==========================================
# INPUT URL
# ==========================================

st.divider()
st.header("🔎 Periksa URL")

url = st.text_input(
    "Masukkan URL yang ingin diperiksa:",
    placeholder="Contoh: https://www.example.com/login",
)

analyze_button = st.button("Analisis URL", type="primary", use_container_width=True)


# ==========================================
# RIWAYAT ANALISIS
# ==========================================

if "history" not in st.session_state:
    st.session_state.history = []


# ==========================================
# PROSES PREDIKSI
# ==========================================

if analyze_button:

    if not url.strip():

        st.warning("Silakan masukkan URL terlebih dahulu.")

    else:

        is_valid, message = validate_url(url)

        if not is_valid:
            st.warning(message)

        else:

            try:

                with st.spinner("Sedang menganalisis URL..."):

                    result = predict_url(url.strip())

                    label = result["label"]
                    probability = result["probability"]
                    features = result["features"]

                # Menyimpan hasil analisis
                result_history = {
                    "URL": url.strip(),
                    "Hasil": label,
                    "Skor Model": f"{probability * 100:.2f}%",
                }

                st.session_state.history.insert(0, result_history)

                st.divider()
                st.header("📊 Hasil Analisis")

                if label == "Phishing":

                    st.error("⚠️ Hasil Prediksi: PHISHING")

                    st.write(
                        "Model mengklasifikasikan URL ini sebagai phishing. "
                        "Berhati-hatilah sebelum mengaksesnya."
                    )

                else:

                    st.success("✅ Hasil Prediksi: BENIGN")

                    st.write(
                        "Model mengklasifikasikan URL ini sebagai benign. "
                        "Namun, hasil ini bukan jaminan bahwa situs sepenuhnya aman."
                    )

                st.metric(
                    label="Skor Prediksi Model", value=f"{probability * 100:.2f}%"
                )

                st.caption(
                    "Skor ini merupakan probabilitas model untuk kelas "
                    "hasil prediksi, bukan jaminan keamanan URL."
                )

                # Menampilkan 22 fitur
                st.subheader("🔬 Detail Ekstraksi Fitur")

                feature_df = pd.DataFrame(
                    list(features.items()), columns=["Nama Fitur", "Nilai"]
                )

                st.dataframe(feature_df, use_container_width=True, hide_index=True)

            except FileNotFoundError as error:

                st.error(f"File yang diperlukan tidak ditemukan: {error}")

            except Exception as error:

                st.error(f"Terjadi kesalahan saat menganalisis URL: {error}")


# ==========================================
# RIWAYAT ANALISIS
# ==========================================

st.divider()
st.header("🕘 Riwayat Analisis")

if st.session_state.history:

    history_df = pd.DataFrame(st.session_state.history)

    st.dataframe(history_df, use_container_width=True, hide_index=True)

    if st.button("Hapus Riwayat"):

        st.session_state.history = []
        st.rerun()

else:

    st.caption("Belum ada URL yang dianalisis.")


# ==========================================
# EVALUASI MODEL
# ==========================================

st.divider()
st.header("📈 Evaluasi Model")

st.write(
    "Model dievaluasi menggunakan data testing yang dipisahkan "
    "dari data pelatihan dengan pembagian 80:20."
)

try:

    evaluation = calculate_model_evaluation()

    # --------------------------------------
    # METRIK EVALUASI
    # --------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Accuracy", f'{evaluation["accuracy"] * 100:.2f}%')

    col2.metric("Precision", f'{evaluation["precision"] * 100:.2f}%')

    col3.metric("Recall", f'{evaluation["recall"] * 100:.2f}%')

    col4.metric("F1-Score", f'{evaluation["f1"] * 100:.2f}%')

    st.caption(f"Jumlah data pengujian: {evaluation['test_total']:,} URL.")

    # --------------------------------------
    # CONFUSION MATRIX
    # --------------------------------------

    st.subheader("Confusion Matrix")

    matrix = evaluation["matrix"]

    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)

    sns.heatmap(
        matrix,
        annot=True,
        fmt=",",
        cmap="Blues",
        xticklabels=["Benign", "Phishing"],
        yticklabels=["Benign", "Phishing"],
        annot_kws={"size": 11},
        cbar=False,
        ax=ax,
    )

    ax.set_xlabel("Predicted Label", fontsize=10)
    ax.set_ylabel("Actual Label", fontsize=10)
    ax.set_title("Random Forest Confusion Matrix", fontsize=12)

    ax.tick_params(axis="both", labelsize=9)

    fig.tight_layout()

    st.pyplot(fig, use_container_width=False)

    plt.close(fig)

    st.caption(
        "Baris menunjukkan kelas sebenarnya, sedangkan kolom "
        "menunjukkan hasil prediksi model."
    )

    # Mengambil nilai TN, FP, FN, TP
    tn, fp, fn, tp = matrix.ravel()

    col1, col2 = st.columns(2)

    with col1:

        st.success(f"True Negative: {tn:,}")
        st.error(f"False Positive: {fp:,}")

    with col2:

        st.error(f"False Negative: {fn:,}")
        st.success(f"True Positive: {tp:,}")

except Exception as error:

    st.error(f"Gagal melakukan evaluasi model: {error}")


# ==========================================
# FEATURE IMPORTANCE
# ==========================================

st.divider()
st.header("🔍 Feature Importance")

st.write(
    "Feature Importance menunjukkan kontribusi relatif setiap fitur "
    "dalam proses pengambilan keputusan model Random Forest."
)

try:

    artifact = get_model_artifact()

    model = artifact["model"]
    feature_columns = artifact["feature_columns"]

    importance_df = pd.DataFrame(
        {"Fitur": feature_columns, "Importance": model.feature_importances_}
    )

    importance_df = importance_df.sort_values(by="Importance", ascending=True)

    # Grafik Feature Importance
    fig, ax = plt.subplots(figsize=(7, 5), dpi=100)

    ax.barh(importance_df["Fitur"], importance_df["Importance"])

    ax.set_xlabel("Feature Importance")
    ax.set_ylabel("Fitur")
    ax.set_title("Random Forest Feature Importance")

    fig.tight_layout()

    st.pyplot(fig, use_container_width=False)

    plt.close(fig)

    st.caption(
        "Semakin tinggi nilai importance, semakin besar kontribusi "
        "relatif fitur tersebut dalam pembagian keputusan pohon. "
        "Nilai ini bukan bukti hubungan sebab-akibat."
    )

    # Tabel Feature Importance
    st.subheader("Detail Nilai Feature Importance")

    display_df = importance_df.sort_values(by="Importance", ascending=False).copy()

    display_df["Importance"] = display_df["Importance"].map(
        lambda value: f"{value:.6f}"
    )

    st.dataframe(display_df, use_container_width=True, hide_index=True)

except Exception as error:

    st.error(f"Gagal menampilkan Feature Importance: {error}")


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Phishing URL Detection System | " "Defensive AI Project | Information Security"
)
