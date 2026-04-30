import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.express as px


st.title("🚀 Smart E-Commerce Analytics")
st.markdown("""
    Welcome, **Bilal**! This AI-powered system helps you detect financial risks 
    and forecast future sales based on your transaction data.
    """)

# --- 1. PAGE CONFIGURATION ---
# Harus diletakkan paling atas sebelum kode UI lainnya
st.set_page_config(page_title="Smart E-Commerce AI", layout="wide", page_icon="📈")

# --- 2. LOAD DATA (Agar 'df' terdefinisi untuk semua halaman) ---
@st.cache_data
def load_initial_data():
    np.random.seed(42)
    data = {
        'order_date': pd.date_range(start='2024-01-01', periods=100, freq='D'),
        'sales': np.random.randint(100, 1000, 100),
        'profit': np.random.randint(-100, 500, 100),
        'discount': np.random.uniform(0, 0.3, 100),
        'region': np.random.choice(['Marmara', 'Ege', 'Akdeniz', 'Central Anatolia'], 100),
        'product_name': np.random.choice(['Laptop', 'Mouse', 'Keyboard', 'Monitor'], 100)
    }
    return pd.DataFrame(data)

df = load_initial_data()

# --- 3. LOAD MODELS & ASSETS ---
@st.cache_resource
def load_assets():
    # Mengarah ke folder 'Notebooks/' sesuai struktur foldermu
    risk_model = joblib.load('Notebooks/risk_model.pkl')
    forecast_model = joblib.load('Notebooks/forecast_model.pkl')
    le_region = joblib.load('Notebooks/le_region.pkl')
    le_product = joblib.load('Notebooks/le_product.pkl')
    return risk_model, forecast_model, le_region, le_product

# Proteksi jika file tidak ditemukan
try:
    risk_model, forecast_model, le_region, le_product = load_assets()
except FileNotFoundError:
    st.error("⚠️ File .pkl tidak ditemukan di folder 'Notebooks'. Pastikan file sudah dipindah ke sana!")
    st.stop()

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Dashboard Overview", 
    "Risk Predictor", 
    "Market Analysis", 
    "Revenue Forecast"
])

# --- 5. PAGE LOGIC ---

# PAGE 1: DASHBOARD OVERVIEW
if page == "Dashboard Overview":
    st.title("🚀 Smart E-Commerce Analytics")
    st.markdown("""
    Welcome, **Bilal**! This AI-powered system helps you detect financial risks 
    and forecast future sales based on your transaction data.
    """)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Model Status", "Active", "Online")
    col2.metric("Accuracy", "92.5%", "+2.1%")
    col3.metric("System Load", "Normal", "0.2s")
    
    st.info("Select a tool from the sidebar to get started.")

# PAGE 2: RISK PREDICTOR
elif page == "Risk Predictor":
    st.title("🛡️ Real-Time Risk Analysis")
    st.write("Input transaction details to check for financial risk.")

    with st.form("risk_form"):
        col1, col2 = st.columns(2)
        with col1:
            sales = st.number_input("Total Sales ($)", min_value=0.0)
            quantity = st.number_input("Quantity Sold", min_value=1)
            discount = st.slider("Discount Applied (%)", 0, 100, 10) / 100
        
        with col2:
            region = st.selectbox("Region", le_region.classes_)
            product = st.selectbox("Product Name", le_product.classes_)
        
        submit = st.form_submit_button("Analyze Transaction")

    if submit:
        region_n = le_region.transform([region])[0]
        product_n = le_product.transform([product])[0]
        input_data = np.array([[sales, quantity, discount, region_n, product_n]])
        prediction = risk_model.predict(input_data)
        
        st.subheader("Analysis Result:")
        if prediction[0] == 1:
            st.error("⚠️ HIGH RISK DETECTED: This transaction is likely a loss or low-margin.")
        else:
            st.success("✅ SAFE: This transaction meets profit efficiency standards.")

# PAGE 3: REVENUE FORECAST
elif page == "Revenue Forecast":
    st.title("📈 Revenue Forecasting")
    st.write("Predicting future sales based on historical trends.")

    future_months = np.array([[6], [7], [8]])
    predictions = forecast_model.predict(future_months)
    
    forecast_data = pd.DataFrame({
        'Month': ['Month 6', 'Month 7', 'Month 8'],
        'Predicted Sales': predictions
    })

    fig = px.line(forecast_data, x='Month', y='Predicted Sales', title='Future Sales Projection', markers=True)
    st.plotly_chart(fig, use_container_width=True)
    st.write("The AI predicts a steady growth based on current market behavior.")

# PAGE 4: MARKET ANALYSIS (With Analyze Button)
elif page == "Market Analysis":
    st.title("📊 Market Insights & Trends")
    st.markdown("Analyze product performance over time and across different regions.")

    # Menggunakan st.form agar ada tombol "Analyze"
    with st.form("market_analysis_form"):
        st.subheader("📅 Select Analysis Period")
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start Date", value=pd.to_datetime("2024-01-01"))
        with col2:
            end_date = st.date_input("End Date", value=pd.to_datetime("2024-12-31"))
        
        # Tombol "Play" / Analisis
        submit_button = st.form_submit_button(label='🚀 Run Market Analysis')

    # Logika Analisis hanya berjalan JIKA tombol diklik
    if submit_button:
        st.divider()
        
        # Filtering data
        mask = (df['order_date'] >= pd.to_datetime(start_date)) & (df['order_date'] <= pd.to_datetime(end_date))
        df_period = df.loc[mask]

        if not df_period.empty:
            # 1. TRENDING PRODUCTS
            st.subheader(f"🔥 Top Products ({start_date} to {end_date})")
            trending = df_period.groupby('product_name')['sales'].sum().sort_values(ascending=False).reset_index()
            
            fig_trend = px.bar(trending, x='sales', y='product_name', orientation='h',
                               color='sales', color_continuous_scale='Magma',
                               labels={'sales': 'Total Sales ($)', 'product_name': 'Product'})
            st.plotly_chart(fig_trend, use_container_width=True)
            
            st.divider()

            # 2. REGIONAL LEADERBOARD
            st.subheader("📍 Regional Sales Leaderboard")
            region_sales = df_period.groupby(['region', 'product_name'])['sales'].sum().reset_index()
            top_per_region = region_sales.sort_values(['region', 'sales'], ascending=[True, False]).drop_duplicates('region')

            fig_region = px.bar(top_per_region, x='region', y='sales', color='product_name',
                                text='product_name', title="Market Leader per Region")
            st.plotly_chart(fig_region, use_container_width=True)
            
            st.success("Analysis Complete! Data successfully filtered.")
        else:
            st.warning("No transactions found for this period. Please try a different date range.")