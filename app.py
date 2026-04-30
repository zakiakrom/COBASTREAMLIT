import streamlit as st
import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="E-Commerce Trend Dashboard", layout="wide")

# Custom CSS agar tampilan metrik lebih mirip dengan referensi gambar (kotak putih berbayang)
# Custom CSS untuk mengubah warna teks metrik menjadi Hitam
st.markdown("""
    <style>
    /* Mengubah warna angka/nilai metrik menjadi hitam */
    [data-testid="stMetricValue"] {
        color: #000000 !important;
        font-weight: bold;
    }
    
    /* Mengubah warna label (judul kecil) metrik menjadi hitam */
    [data-testid="stMetricLabel"] {
        color: #000000 !important;
    }

    /* Card styling tetap seperti referensi gambar */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e1e4e8;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOAD ASSETS ---
@st.cache_resource
def load_data():
    try:
        # Load model dan encoders
        model = joblib.load('Notebooks/model_trending.pkl')
        encoders = joblib.load('Notebooks/encoders.pkl')
        # Load dataset untuk visualisasi
        df = pd.read_csv('Data/Processed/ecommerce_clean.csv')
        return model, encoders, df
    except Exception as e:
        st.error(f"Gagal memuat file: {e}. Pastikan file .pkl dan .csv ada di folder yang sama.")
        st.stop()

model, encoders, df = load_data()

# --- 3. SIDEBAR (Kontrol & Prediksi) ---
# Bagian sidebar di sebelah kiri, seperti pada gambar referensi
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=120)
st.sidebar.title("Analyze Product Trend")
st.sidebar.write("Input product details to get an instant AI prediction.")
st.sidebar.markdown("---")

# Form input untuk prediksi di sidebar
with st.sidebar.form("input_form"):
    selected_cat = st.selectbox("Category", encoders['category'].classes_)
    selected_reg = st.selectbox("Region", encoders['region'].classes_)
    qty = st.number_input("Quantity", min_value=1, value=10)
    price = st.number_input("Unit Price ($)", min_value=0.1, value=49.99)
    discount = st.slider("Discount (%)", 0.0, 1.0, 0.1)
    
    submit_btn = st.form_submit_button("Start Analysis")

# Logika Prediksi AI
if submit_btn:
    # Transform input teks menjadi angka
    cat_n = encoders['category'].transform([selected_cat])[0]
    reg_n = encoders['region'].transform([selected_reg])[0]
    
    # Masukkan ke DataFrame (urutan kolom harus sama dengan saat latihan X)
    input_features = pd.DataFrame([[cat_n, qty, price, discount, reg_n]], 
                                    columns=['category_n', 'quantity', 'unit_price', 'discount', 'region_n'])
    
    res = model.predict(input_features)[0]
    
    # Tampilkan hasil prediksi di sidebar
    if res == 1:
        st.sidebar.success(f"🔥 Prediction: **TRENDING!**")
        st.sidebar.write(f"Product is likely to be a hot item in {selected_reg}.")
    else:
        st.sidebar.warning(f"📉 Prediction: **NORMAL**")
        st.sidebar.write(f"Product is expected to have standard sales volume in {selected_reg}.")

# --- 4. KONTEN UTAMA (Dashboard Analytics) ---
st.title("🚀 E-Commerce Analytics Dashboard")
st.write(f"A comprehensive view of trends across **{len(df):,}** transaction records.")
st.markdown("---")

# Row 1: Key Performance Metrics (Kotak-kotak di atas pada gambar)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"${df['sales'].sum():,.0f}")
c2.metric("Total Profit", f"${df['profit'].sum():,.0f}")
c3.metric("Avg Profit Margin", f"{(df['profit'].sum() / df['sales'].sum())*100:.1f}%")
c4.metric("Trending Items", len(df[df['is_trending'] == 1]), delta_color="normal")

st.markdown("---")

# Row 2: Regional Sales Analysis (Grafik di tengah pada gambar)
st.subheader("📍 Regional Sales Performance by Category")
# Mirip dengan persebaran region yang kamu buat sebelumnya
region_sales = df.groupby(['region', 'category'])['sales'].sum().reset_index()

plt.figure(figsize=(12, 6))
# Menggunakan palet warna yang bersih agar mirip dengan referensi
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=region_sales, x='region', y='sales', hue='category', palette="muted", ax=ax)
plt.title("Total Sales Revenue Distribution")
plt.ylabel("Sales ($)")
st.pyplot(fig)

# Row 3: Data Table (Tabel di bawah pada gambar)
st.subheader("📋 Top 10 High-Volume Transactions")
# Menampilkan kolom kunci saja agar rapi
display_cols = ['order_date', 'region', 'category', 'product_name', 'sales', 'quantity', 'is_trending']
st.dataframe(df[display_cols].sort_values(by='sales', ascending=False).head(10), use_container_width=True)

# Footer
st.caption(f"Dashboard generated for Yapay Zeka Project | Bartın, Türkiye | {df['order_date'].max()}")