import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

def show():
       # SETELAN LEBAR HALAMAN DAN IKON
    st.set_page_config(
        page_title="Sales Dashboard",
        page_icon="📊",
        layout="wide")

    st.title("Trending Analysis")

    # 1. Konfigurasi Halaman
    st.set_page_config(
        page_title="Trending Products - DataSense",
        page_icon="📈",
        layout="wide"
    )
    
    # 4. Top Insights (Bento Grid Style)
    row1_col1, row1_col2 = st.columns([2, 1])

    with row1_col1:
        with st.container(border=True):
            inner_h1, inner_h2 = st.columns([2, 1])
            inner_h1.subheader("Market Forecast")
            inner_h1.caption("Aggregated 12-month predictive modeling")
            
            # Metrics di dalam chart area
            with inner_h2:
                m_col1, m_col2 = st.columns(2)
                m_col1.metric("Volatility", "0.42%")
                m_col2.metric("Confidence", "89.4%")
            
            # Forecast Chart menggunakan data dummy
            chart_data = pd.DataFrame(
                np.random.randn(20, 1),
                columns=['Trend Index']
            )
            st.area_chart(chart_data, color="#ff4b4b", height=200)
            
            st.caption("JAN 24 — DEC 24 (Projected)")

    with row1_col2:
        with st.container(border=True):
            st.caption("HIGH VELOCITY")
            st.subheader("Growth Index")
            
            st.write("##")
            st.metric("Quarterly Growth", "+24.8%", delta="Momentum High")
            
            st.write("Category average outperformed by 12 points this quarter.")
            st.write("##")
            st.button("View Full Index", use_container_width=True)

    # 5. Product Leaderboard (List/Table Style)
    st.write("##")
    st.subheader("Product Leaderboard")

    # Menyiapkan data untuk leaderboard
    products = [
        {
            "Product": "NeuralLink Pro",
            "Category": "Audio Tech",
            "Growth": 42.5,
            "Market Share": 0.85,
            "Status": "Exceptional"
        },
        {
            "Product": "BioWatch Series 9",
            "Category": "Wearables",
            "Growth": 18.2,
            "Market Share": 0.62,
            "Status": "Performing"
        },
        {
            "Product": "EcoStream 500",
            "Category": "Green Energy",
            "Growth": 54.9,
            "Market Share": 0.41,
            "Status": "Exceptional"
        }
    ]

    df_products = pd.DataFrame(products)

    # Menampilkan menggunakan st.dataframe dengan Column Config yang canggih
    st.dataframe(
        df_products,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Product": st.column_config.TextColumn("Product Name", help="The name of the trending item"),
            "Growth": st.column_config.NumberColumn("Growth WoW", format="+%.1f%%"),
            "Market Share": st.column_config.ProgressColumn("Market Share", min_value=0, max_value=1, format="%.0f%%"),
            "Category": st.column_config.TextColumn("Category"),
            "Status": st.column_config.SelectboxColumn(
                "Performance Status",
                options=["Exceptional", "Performing", "At Risk"]
            )
        }
    )
