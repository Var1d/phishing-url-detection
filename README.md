# 🛡️ Phishing URL Detection System

Aplikasi deteksi URL phishing berbasis **Machine Learning** menggunakan algoritma **Random Forest Classifier**. Proyek ini dikembangkan sebagai implementasi Defensive AI untuk memenuhi tugas mata kuliah Keamanan Informasi.

Aplikasi menganalisis karakteristik atau fitur dari sebuah URL untuk mengklasifikasikannya ke dalam dua kategori:

- **Benign:** URL yang dikategorikan normal berdasarkan pola yang dipelajari dari dataset.
- **Phishing:** URL yang dikategorikan sebagai phishing berdasarkan pola yang dipelajari dari dataset.

Aplikasi dibangun menggunakan Python, Scikit-learn, dan Streamlit. Pengguna dapat memasukkan URL untuk dianalisis tanpa aplikasi harus membuka atau mengunjungi situs tersebut.

Versi antarmuka baru menggunakan Vue 3 untuk frontend dan Flask untuk API Python. File `app.py` Streamlit tetap tersedia sebagai versi lama.

---

## 1. Fitur Utama

### Deteksi URL
- Menerima URL yang dimasukkan oleh pengguna.
- Memvalidasi format URL sebelum proses prediksi.
- Mengklasifikasikan URL menjadi Benign atau Phishing.
- Menampilkan skor prediksi model.

### Ekstraksi Fitur
- Mengekstraksi 22 karakteristik URL.
- Menampilkan detail nilai fitur yang digunakan dalam proses klasifikasi.

### Ringkasan Dataset
- Menampilkan jumlah data sebelum dan sesudah preprocessing.
- Menampilkan jumlah data yang dihapus.
- Menampilkan distribusi kelas Benign dan Phishing.

### Evaluasi Model
- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

### Analisis Kesalahan Model
- Mengidentifikasi False Positive.
- Mengidentifikasi False Negative.
- Menampilkan contoh URL yang salah diklasifikasikan.
- Menyediakan fitur unduh hasil kesalahan dalam format CSV.

### Feature Importance
- Menampilkan kontribusi relatif setiap fitur dalam model Random Forest.
- Menyediakan grafik dan tabel Feature Importance.

### Riwayat Analisis
- Menyimpan riwayat URL yang telah dianalisis selama sesi aplikasi.
- Menyediakan fitur untuk menghapus riwayat analisis.

---

## 2. Teknologi yang Digunakan

| Teknologi | Kegunaan |
|---|---|
| Python | Bahasa pemrograman utama |
| Pandas | Pengolahan dataset |
| NumPy | Operasi numerik |
| Scikit-learn | Implementasi Machine Learning dan evaluasi model |
| Random Forest | Algoritma klasifikasi |
| Streamlit | Pembuatan antarmuka aplikasi |
| Matplotlib | Visualisasi data |
| Seaborn | Visualisasi Confusion Matrix |
| Joblib | Penyimpanan dan pemuatan model |
| TLDExtract | Ekstraksi informasi domain |
| Pytest | Pengujian otomatis program |

---

## 3. Dataset

Proyek ini menggunakan dataset **URL-Phish Version 2** yang diperoleh dari Mendeley Data.

**Tautan dataset:**

https://data.mendeley.com/datasets/65z9twcx3r/2

Dataset berisi kumpulan URL yang telah diberi label Benign dan Phishing serta dilengkapi sejumlah fitur numerik untuk proses klasifikasi.

### Ringkasan Dataset

| Keterangan | Jumlah |
|---|---:|
| Jumlah data awal | 116.600 |
| Jumlah data setelah cleaning | 115.231 |
| Jumlah data yang dihapus | 1.369 |
| Data Benign | 98.641 |
| Data Phishing | 16.590 |

### Cara Mengunduh Dataset

1. Buka tautan Mendeley Data di atas.
2. Unduh file dataset yang tersedia.
3. Pastikan file dataset diberi nama `Dataset.csv`.
4. Letakkan file tersebut di dalam folder `dataset/` pada proyek.

Lokasi file yang diharapkan:

```text
dataset/
└── Dataset.csv
```

**Catatan:** File dataset tidak disertakan langsung dalam repository GitHub. Setiap anggota kelompok perlu mengunduh dataset dari sumber tersebut atau memperoleh salinannya dari anggota kelompok.

---

## 4. Struktur Folder Proyek

```text
Phishing-URL-Detection/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── dataset/
│   ├── Dataset.csv
│   └── cleaned_dataset.csv
│
├── models/
│   └── random_forest.pkl
│
├── src/
│   ├── data_preprocessing.py
│   ├── model_training.py
│   ├── feature_extraction.py
│   ├── prediction.py
│   ├── test_feature_extraction.py
│   ├── validate_features.py
│   └── error_analysis.py
│
├── tests/
│   └── test_prediction.py
│
└── evaluation/
    └── misclassified_urls.csv
```

### Keterangan Folder dan File

- `app.py`: File utama untuk menjalankan aplikasi Streamlit.
- `dataset/`: Menyimpan dataset asli dan dataset hasil preprocessing.
- `models/`: Menyimpan model Random Forest yang telah dilatih.
- `src/`: Berisi modul preprocessing, training, ekstraksi fitur, prediksi, validasi, dan analisis kesalahan.
- `tests/`: Menyimpan file pengujian otomatis.
- `evaluation/`: Menyimpan hasil analisis kesalahan klasifikasi.
- `requirements.txt`: Daftar pustaka Python yang diperlukan.
- `.gitignore`: Mengatur file dan folder yang tidak disertakan dalam GitHub.

---

## 5. Persiapan dan Instalasi

### Persyaratan

Sebelum menjalankan proyek, pastikan perangkat sudah memiliki:

- Python 3.10 atau versi kompatibel dengan dependensi proyek.
- Git.
- Visual Studio Code atau editor kode lainnya.

### Langkah 1 — Clone Repository

Unduh proyek dari GitHub menggunakan perintah:

```bash
git clone <URL_REPOSITORY_GITHUB>
```

Masuk ke folder proyek:

```bash
cd Phishing-URL-Detection
```

### Langkah 2 — Membuat Virtual Environment

Buat lingkungan virtual Python:

```bash
python -m venv .venv
```

Aktifkan virtual environment menggunakan PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Jika menggunakan Command Prompt:

```cmd
.venv\Scripts\activate
```

### Langkah 3 — Menginstal Dependensi

Perbarui pip:

```bash
python -m pip install --upgrade pip
```

Instal seluruh pustaka yang diperlukan:

```bash
pip install -r requirements.txt
```

---

## 6. Persiapan Dataset dan Training Model

Dataset dan model hasil training tidak disertakan dalam repository GitHub. Oleh karena itu, keduanya harus disiapkan sebelum aplikasi dijalankan.

### Langkah 1 — Mengunduh Dataset

Unduh dataset URL-Phish Version 2 melalui tautan berikut:

https://data.mendeley.com/datasets/65z9twcx3r/2

Letakkan file `Dataset.csv` di:

```text
dataset/Dataset.csv
```

### Langkah 2 — Melakukan Preprocessing

Jalankan perintah:

```bash
python src/data_preprocessing.py
```

Proses preprocessing akan menghasilkan dataset yang telah dibersihkan:

```text
dataset/cleaned_dataset.csv
```

### Langkah 3 — Melatih Model

Jalankan:

```bash
python src/model_training.py
```

Proses ini akan melatih model menggunakan algoritma Random Forest.

Model yang telah dilatih akan disimpan di:

```text
models/random_forest.pkl
```

Setelah proses tersebut selesai, model sudah dapat digunakan oleh aplikasi untuk melakukan prediksi URL.

---

## 7. Menjalankan Aplikasi

Pastikan virtual environment sudah aktif serta dataset dan model sudah tersedia.

### Versi Vue + Flask

Bangun frontend Vue:

```bash
cd frontend
npm.cmd install
npm.cmd run build
cd ..
```

Jalankan server Flask:

```text
python api.py
```

Buka `http://127.0.0.1:5000` melalui browser.

Untuk pengembangan frontend, jalankan `npm.cmd run dev` di folder `frontend` dan buka alamat Vite yang ditampilkan, biasanya `http://localhost:5173`. Frontend development akan meneruskan permintaan `/api` ke Flask.

### Versi Streamlit Lama

```bash
streamlit run app.py
```

---

## 8. Pengujian Program

Proyek ini menyediakan pengujian untuk memastikan fungsi ekstraksi fitur dan prediksi berjalan sesuai harapan.

### Menjalankan Pengujian Otomatis

```bash
python -m pytest -v
```

File pengujian yang tersedia:

- `src/test_feature_extraction.py`
- `tests/test_prediction.py`

### Validasi Ekstraksi Fitur

Untuk membandingkan hasil ekstraksi fitur dengan sampel dari dataset, jalankan:

```bash
python src/validate_features.py
```

---

## 9. Evaluasi Model

Model menggunakan pembagian dataset menjadi data training dan testing dengan rasio 80:20, `random_state=42`, dan stratifikasi berdasarkan label.

Algoritma yang digunakan adalah Random Forest Classifier dengan konfigurasi:

- Jumlah pohon keputusan: 200.
- `random_state`: 42.
- `class_weight`: balanced.

### Hasil Evaluasi

Berdasarkan pengujian pada data testing, diperoleh hasil:

| Metrik | Hasil |
|---|---:|
| Accuracy | 97,60% |
| Precision (Phishing) | 90,25% |
| Recall (Phishing) | 93,46% |
| F1-Score (Phishing) | 91,83% |

### Confusion Matrix

| Kelas Aktual / Prediksi | Benign | Phishing |
|---|---:|---:|
| Benign | 19.394 | 335 |
| Phishing | 217 | 3.101 |

### Analisis Kesalahan

Hasil pengujian juga menunjukkan adanya kesalahan klasifikasi:

| Jenis Kesalahan | Jumlah |
|---|---:|
| False Positive | 335 |
| False Negative | 217 |
| Total Kesalahan | 552 |

**False Positive** terjadi ketika URL yang sebenarnya berlabel Benign diprediksi sebagai Phishing.

**False Negative** terjadi ketika URL yang sebenarnya berlabel Phishing diprediksi sebagai Benign.

Untuk menjalankan analisis kesalahan secara terpisah, gunakan:

```bash
python src/error_analysis.py
```

Hasil analisis akan disimpan dalam:

```text
evaluation/misclassified_urls.csv
```

Dashboard juga menyediakan ringkasan jumlah kesalahan, contoh URL yang salah diklasifikasikan, serta fitur unduh hasil analisis dalam format CSV.

---

## 10. Keterbatasan Sistem

Beberapa keterbatasan sistem yang perlu diperhatikan:

1. Sistem menganalisis karakteristik teks URL, bukan isi halaman website.
2. Aplikasi tidak membuka atau mengunjungi website yang sedang diperiksa.
3. Hasil klasifikasi bergantung pada pola yang dipelajari dari dataset pelatihan.
4. URL yang diklasifikasikan sebagai Benign tidak otomatis menjamin bahwa website sepenuhnya aman.
5. Skor prediksi merupakan keluaran probabilitas model, bukan jaminan tingkat keamanan sebenarnya.
6. Karakteristik dan sumber dataset dapat memengaruhi kemampuan model dalam mengklasifikasikan URL di luar dataset yang digunakan.

---

## 11. Tujuan Proyek

Proyek ini bertujuan menerapkan pendekatan Defensive AI untuk membantu mengidentifikasi URL yang berpotensi phishing menggunakan Machine Learning.

Melalui proses preprocessing data, ekstraksi fitur, klasifikasi menggunakan Random Forest, evaluasi performa, dan analisis kesalahan, proyek ini menunjukkan penerapan Machine Learning sebagai salah satu pendekatan dalam bidang keamanan informasi.

---

## 12. Identitas Kelompok

**Mata Kuliah:** Keamanan Informasi  
**Program Studi:** Informatika  
**Universitas:** Universitas Siliwangi

**Anggota Kelompok:**

1. Jamal Abdul Nasir 
2. Muhammad Fadhil Nurwahid
3. Farid Dhiya Fairuz

---

## Disclaimer

Aplikasi ini dikembangkan untuk keperluan pendidikan dan penelitian dalam bidang keamanan informasi.

Hasil prediksi aplikasi tidak boleh dijadikan satu-satunya dasar untuk menentukan apakah suatu website aman atau berbahaya.