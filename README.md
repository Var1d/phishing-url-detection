# 🛡️ Phishing URL Detection System

Sistem deteksi URL phishing berbasis Machine Learning menggunakan algoritma **Random Forest Classifier**.

Proyek ini dikembangkan untuk mata kuliah **Keamanan Informasi** sebagai implementasi Defensive AI. Sistem menganalisis karakteristik URL tanpa harus mengunjungi atau membuka situs tujuan, kemudian mengklasifikasikannya menjadi:

- **Benign**: URL diklasifikasikan sebagai URL normal.
- **Phishing**: URL diklasifikasikan sebagai URL phishing.

## 1. Tujuan Proyek

Tujuan proyek ini adalah membangun aplikasi yang dapat membantu mengidentifikasi URL yang berpotensi phishing menggunakan pendekatan Machine Learning.

Sistem menggunakan fitur numerik yang diekstraksi dari URL, kemudian diproses oleh model Random Forest untuk menghasilkan prediksi.

## 2. Teknologi yang Digunakan

| Teknologi | Kegunaan |
|---|---|
| Python | Bahasa pemrograman |
| Pandas | Pengolahan dataset |
| NumPy | Operasi numerik |
| Scikit-learn | Pelatihan dan evaluasi model |
| Random Forest | Algoritma klasifikasi |
| TLDExtract | Ekstraksi informasi domain |
| Streamlit | Antarmuka aplikasi |
| Matplotlib & Seaborn | Visualisasi data |
| Joblib | Penyimpanan model |

## 3. Dataset

Proyek ini menggunakan dataset **URL-Phish Version 2** dari Mendeley Data.

Dataset berisi 116.600 data URL dengan dua kelas:

| Label | Keterangan | Jumlah awal |
|---|---|---:|
| 0 | Benign | 100.000 |
| 1 | Phishing | 16.600 |

Setelah preprocessing dan penghapusan URL duplikat, dataset berisi **115.231 data**.

Rincian data setelah preprocessing:

- Benign: 98.641
- Phishing: 16.590
- URL duplikat yang dihapus: 1.369

**Catatan:** File dataset tidak disimpan di repository GitHub. Anggota kelompok perlu mendapatkan versi dataset yang sama dan meletakkannya secara lokal di folder `dataset/`.

Nama file yang diharapkan:

`dataset/Dataset.csv`

## 4. Struktur Folder

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
└── src/
    ├── data_preprocessing.py
    ├── model_training.py
    ├── feature_extraction.py
    ├── prediction.py
    ├── test_feature_extraction.py
    └── validate_features.py
```

Keterangan:

| File | Fungsi |
|---|---|
| `app.py` | Antarmuka aplikasi Streamlit |
| `data_preprocessing.py` | Membersihkan dan mempersiapkan dataset |
| `model_training.py` | Melatih dan mengevaluasi model Random Forest |
| `feature_extraction.py` | Mengekstraksi 22 fitur dari URL |
| `prediction.py` | Memuat model dan melakukan prediksi URL |
| `test_feature_extraction.py` | Menguji kesesuaian ekstraksi fitur pada sampel |
| `validate_features.py` | Memvalidasi ekstraksi fitur menggunakan 500 URL |
| `Dataset.csv` | Dataset asli |
| `cleaned_dataset.csv` | Dataset setelah preprocessing |
| `random_forest.pkl` | Model hasil pelatihan |

## 5. Persiapan Lingkungan

Pastikan Python dan Git sudah terpasang.

Clone repository:

```bash
git clone <URL_REPOSITORY_GITHUB>
```

Masuk ke folder proyek:

```bash
cd Phishing-URL-Detection
```

Buat virtual environment:

```bash
python -m venv .venv
```

Aktifkan virtual environment.

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

Instal seluruh dependensi:

```bash
pip install -r requirements.txt
```

## 6. Persiapan Dataset dan Model

Karena dataset dan file model tidak disimpan di repository, anggota kelompok perlu menyiapkannya terlebih dahulu.

### A. Menyiapkan Dataset

Letakkan dataset asli dengan nama:

```text
dataset/Dataset.csv
```

Pastikan struktur folder `dataset` tersedia.

### B. Menjalankan Preprocessing

Dari folder utama proyek, jalankan:

```bash
python src/data_preprocessing.py
```

Program akan melakukan pemeriksaan dan pembersihan dataset, kemudian menghasilkan:

```text
dataset/cleaned_dataset.csv
```

### C. Melatih Model

Jalankan:

```bash
python src/model_training.py
```

Model akan dilatih menggunakan algoritma Random Forest dan disimpan ke:

```text
models/random_forest.pkl
```

File model tersebut diperlukan agar aplikasi dapat melakukan prediksi.

## 7. Menjalankan Aplikasi

Setelah model berhasil dibuat, jalankan:

```bash
streamlit run app.py
```

Aplikasi akan berjalan secara lokal dan dapat diakses melalui browser.

Fitur aplikasi yang direncanakan:

1. Input URL untuk dianalisis.
2. Prediksi klasifikasi Benign atau Phishing.
3. Tampilan skor prediksi model.
4. Detail 22 fitur hasil ekstraksi URL.
5. Riwayat analisis selama sesi aplikasi berjalan.
6. Informasi evaluasi performa model.

## 8. Evaluasi Model

Model menggunakan Random Forest dengan konfigurasi:

- `n_estimators = 200`
- `random_state = 42`
- `class_weight = balanced`
- `n_jobs = -1`

Dataset dibagi menjadi:

- 80% data pelatihan.
- 20% data pengujian.

Pembagian dilakukan menggunakan `train_test_split` dengan `stratify=y` dan `random_state=42`.

Hasil evaluasi pada data pengujian:

| Metrik | Hasil |
|---|---:|
| Accuracy | 97,60% |
| Precision (Phishing) | 90,25% |
| Recall (Phishing) | 93,46% |
| F1-Score (Phishing) | 91,83% |

Confusion Matrix:

| | Predicted Benign | Predicted Phishing |
|---|---:|---:|
| Actual Benign | 19.394 | 335 |
| Actual Phishing | 217 | 3.101 |

Interpretasi:

- True Negative (TN): 19.394 URL benign diklasifikasikan dengan benar.
- False Positive (FP): 335 URL benign salah diklasifikasikan sebagai phishing.
- False Negative (FN): 217 URL phishing salah diklasifikasikan sebagai benign.
- True Positive (TP): 3.101 URL phishing diklasifikasikan dengan benar.

## 9. Validasi Ekstraksi Fitur

Sistem menggunakan 22 fitur numerik yang dihitung dari karakteristik URL.

Validasi dilakukan dengan membandingkan hasil ekstraksi fitur dari program dengan nilai fitur asli pada dataset.

Hasil pengujian terhadap 500 URL:

| Pemeriksaan | Hasil |
|---|---:|
| Jumlah sampel | 500 |
| Berhasil diperiksa | 500 |
| Gagal diproses | 0 |
| Ketidaksesuaian fitur | 0 |

Seluruh 22 fitur cocok pada 500 sampel yang diuji.

Untuk menjalankan validasi:

```bash
python src/validate_features.py
```

## 10. Pengujian

Pengujian ekstraksi fitur:

```bash
python src/test_feature_extraction.py
```

Pengujian validasi 500 URL:

```bash
python src/validate_features.py
```

Pengujian prediksi:

```bash
python src/prediction.py
```

## 11. Alur Kerja Sistem

```text
Dataset URL
     |
     v
Data Preprocessing
     |
     v
Cleaned Dataset
     |
     v
Random Forest Training
     |
     v
Trained Model
     |
     v
User Input URL
     |
     v
Feature Extraction (22 Features)
     |
     v
Random Forest Prediction
     |
     v
Benign / Phishing
```

## 12. Catatan dan Batasan Sistem

- Sistem menganalisis karakteristik teks URL, bukan isi halaman web.
- Sistem tidak mengunjungi situs tujuan atau melakukan pemindaian langsung terhadap website.
- Hasil prediksi bukan jaminan bahwa suatu URL aman atau berbahaya.
- Skor probabilitas model bukan probabilitas keamanan dunia nyata yang telah dijamin terkalibrasi.
- Performa model dapat dipengaruhi oleh karakteristik dan sumber dataset.
- Hasil evaluasi merupakan hasil pengujian pada pembagian dataset tertentu dan belum tentu mencerminkan performa pada seluruh URL di internet.

## 13. Panduan untuk Anggota Kelompok

Jika ingin melanjutkan pengembangan proyek:

1. Clone repository GitHub.
2. Buat dan aktifkan virtual environment.
3. Instal dependensi dari `requirements.txt`.
4. Siapkan dataset `Dataset.csv` di folder `dataset/`.
5. Jalankan preprocessing.
6. Latih ulang model.
7. Jalankan aplikasi Streamlit.
8. Lakukan pengujian sebelum mengubah atau menambahkan fitur.

Jika melakukan perubahan kode, pastikan fitur ekstraksi tetap konsisten dengan fitur yang digunakan ketika model dilatih.

## 14. Pengembangan Selanjutnya

Beberapa pengembangan yang dapat dilakukan:

- Memperbaiki tampilan antarmuka aplikasi.
- Menambahkan visualisasi hasil prediksi.
- Menambahkan analisis feature importance.
- Melakukan cross-validation.
- Menguji model menggunakan dataset eksternal.
- Menganalisis false positive dan false negative lebih lanjut.

---

**Project:** Phishing URL Detection System  
**Category:** Defensive AI  
**Course:** Information Security
