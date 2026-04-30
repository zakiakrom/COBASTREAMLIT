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
        layout="wide"
    )

    # 1. Konfigurasi Halaman
    st.set_page_config(
        page_title="DataHero | Smart Inventory",
        page_icon="🛡️",
        layout="wide"
    )

    # 4. Hero Section
    st.title("Smart Inventory Actions")
    st.write("AI-driven insights based on last 30 days of sales data and market trends.")

    # 5. Bento Grid Stats
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        with st.container(border=True):
            st.metric("Total Recommendations", "42", delta="+12% vs LW")
    with m2:
        with st.container(border=True):
            st.metric("Stock Risk Level", "Medium", delta="Stable trend", delta_color="off")
    with m3:
        with st.container(border=True):
            st.metric("Projected Revenue", "$14.2k", delta="Potential uplift")
    with m4:
        with st.container(border=True):
            st.metric("Processing Priority", "High", delta="3 critical pending", delta_color="inverse")

  