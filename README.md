# 📊 E-Commerce Risk Analysis & Trend Discovery System

## 📌 Deskripsi Proyek
Proyek ini bertujuan untuk meningkatkan keberlanjutan finansial bisnis e-commerce dengan meminimalkan risiko operasional melalui pendekatan **Data Science** dan **Machine Learning**. Sistem ini fokus pada dua solusi utama:
1. **Trend Discovery:** Mendeteksi produk yang akan populer dalam rentang waktu tertentu untuk menghindari *opportunity loss*.
2. **Regional Mapping:** Memetakan persebaran produk terlaris per wilayah untuk optimalisasi stok dan logistik.

---

## 🚀 Fitur Utama

### 1. Trend Forecasting (ML-Powered)
Menggunakan **Facebook Prophet** untuk menganalisis data historis penjualan dan memprediksi tren permintaan di masa depan. Membantu bisnis menentukan kapan harus menambah stok sebelum permintaan melonjak.

### 2. Geospatial Sales Analysis
Visualisasi peta interaktif yang menunjukkan produk terlaris berdasarkan region. Fitur ini menjawab risiko kesalahan alokasi barang antar gudang di berbagai wilayah.

---

## 🛠️ Tech Stack
- **Language:** Python
- **Data Wrangling:** Pandas, NumPy
- **Machine Learning:** Facebook Prophet (Time-Series)
- **Dashboard:** Streamlit
- **Visualization:** Plotly & Pydeck (Peta 3D)
- **Design:** Figma

---

## 📂 Struktur Proyek
```text
E-Commerce Risk Analysis & Trend Discovery System/
├── assets/                 # Aset Visual
│   ├── figma-design.png    # Screenshot desain High-Fi dari Figma
│   ├── demo.gif            # Animasi dashboard saat dijalankan
│   └── logo.png            # Logo proyek (opsional)
├── data/                   # Data Management
│   ├── raw/                # Dataset asli (contoh: olist_ecommerce.csv)
│   └── processed/          # Data setelah di-wrangling (siap untuk ML)
├── notebooks/              # Dokumentasi Eksperimen (Jupyter Notebook)
│   ├── 01_wrangling_eda.ipynb   # Proses pembersihan & eksplorasi
│   ├── 02_trend_forecasting.ipynb # Eksperimen model Prophet
│   └── 03_regional_analysis.ipynb # Eksperimen pemetaan wilayah
├── src/                    # Source Code Utama
│   ├── __init__.py
│   ├── processor.py        # Script untuk pemrosesan data otomatis
│   └── ml_engine.py        # Script logika Prophet & Ranking
├── app.py                  # Entry point aplikasi Streamlit
├── requirements.txt        # Daftar library (Pandas, Prophet, Streamlit, dll.)
├── .gitignore              # File yang tidak boleh di-upload (seperti folder venv/)
└── README.md               # Dokumentasi utama proyek
