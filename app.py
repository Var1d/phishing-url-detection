import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Memastikan folder src dapat ditemukan
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "src"))

from prediction import predict_url

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(page_title="Phishing URL Detection", page_icon="🛡️", layout="wide")


# ==========================================
# JUDUL DAN DESKRIPSI
# ==========================================

st.title("🛡️ Phishing URL Detection System")

st.write(
    "Aplikasi berbasis Machine Learning untuk mengklasifikasikan "
    "URL menjadi **Benign** atau **Phishing** menggunakan algoritma Random Forest."
)

st.info(
    "Aplikasi ini menganalisis karakteristik teks URL. "
    "Aplikasi tidak membuka atau mengunjungi situs yang diperiksa."
)


# ==========================================
# INPUT URL
# ==========================================

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
        try:
            with st.spinner("Sedang menganalisis URL..."):

                # Memanggil fungsi prediksi
                result = predict_url(url.strip())

                # Mengambil nilai dari dictionary
                prediction = result["prediction"]
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

            # Menampilkan hasil klasifikasi
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

            # Menampilkan skor prediksi
            st.metric(label="Skor Prediksi Model", value=f"{probability * 100:.2f}%")

            st.caption(
                "Skor ini merupakan probabilitas model untuk kelas hasil "
                "prediksi, bukan jaminan keamanan URL."
            )

            # Menampilkan 22 fitur URL
            st.subheader("🔬 Detail Ekstraksi Fitur")

            feature_df = pd.DataFrame(
                list(features.items()), columns=["Nama Fitur", "Nilai"]
            )

            st.dataframe(feature_df, use_container_width=True, hide_index=True)

        except FileNotFoundError:
            st.error(
                "File model tidak ditemukan. "
                "Pastikan models/random_forest.pkl tersedia. "
                "Jika belum, jalankan src/model_training.py terlebih dahulu."
            )

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
# INFORMASI EVALUASI MODEL
# ==========================================

st.divider()
st.header("📈 Evaluasi Model")

st.write(
    "Berikut merupakan hasil evaluasi Random Forest pada data pengujian "
    "yang dipisahkan dari data pelatihan."
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Accuracy", "97.60%")
col2.metric("Precision", "90.25%")
col3.metric("Recall", "93.46%")
col4.metric("F1-Score", "91.83%")

st.subheader("Confusion Matrix")

matrix_df = pd.DataFrame(
    [[19394, 335], [217, 3101]],
    index=["Actual Benign", "Actual Phishing"],
    columns=["Predicted Benign", "Predicted Phishing"],
)

st.dataframe(matrix_df, use_container_width=True)

st.caption("TN = 19.394 | FP = 335 | FN = 217 | TP = 3.101")


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Phishing URL Detection System | " "Defensive AI Project | Information Security"
)
