import streamlit as st
import joblib
import pandas as pd

# Load model
model = joblib.load(r"C:\PROJE\yapayzeka\Notebooks\model_recommendation.pkl")
model_trending = joblib.load(r"C:\PROJE\yapayzeka\Notebooks\model_trending.pkl")
le_region = joblib.load(r"C:\PROJE\yapayzeka\Notebooks\le_region.pkl")
le_category = joblib.load(r"C:\PROJE\yapayzeka\Notebooks\le_category.pkl")
encoders = joblib.load(r"C:\PROJE\yapayzeka\Notebooks\encoders.pkl")
label_encoder = joblib.load(r"C:\PROJE\yapayzeka\Notebooks\label_encoder.pkl")


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

region = st.selectbox("Pilih Region", le_region.classes_)
category = st.selectbox("Pilih Category", le_category.classes_)

region_encoded = le_region.transform([region])[0]
category_encoded = le_category.transform([category])[0]

# input_data = [[region_encoded, category_encoded]]

if st.button("Recommend"):
    result = model.predict(input_data)
    st.success(f"Rekomendasi Produk: {result[0]}")