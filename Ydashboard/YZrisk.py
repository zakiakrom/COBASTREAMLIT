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
    st.title("RISK PREDICTION")

    # 1. Konfigurasi Halaman
    st.set_page_config(
        page_title="DataSense Pro",
        page_icon="🛡️",
        layout="wide"
    )

    # 3. Header
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:

        st.write("Real-time predictive modeling for enterprise-level vulnerabilities.")

    with col_h2:
        st.write("##") # Spacer
        inner_col1, inner_col2 = st.columns(2)
        inner_col1.button("Export", use_container_width=True)
        inner_col2.button("Simulate", type="primary", use_container_width=True)

    # 4. Row 1: Metrics & Gauges
    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)

    with row1_col1:
        st.metric("Aggregate Risk Index", "74.2", delta="12%", delta_color="inverse")

    with row1_col2:
        # Menggunakan Plotly untuk visualisasi yang lebih 'pro' tanpa HTML
        fig_fail = px.pie(values=[14, 86], hole=0.7, color_discrete_sequence=['#ff4b4b', '#262730'])
        fig_fail.update_layout(showlegend=False, height=140, margin=dict(t=0, b=0, l=0, r=0))
        st.write("System Failure Prob.")
        st.plotly_chart(fig_fail, use_container_width=True, config={'displayModeBar': False})

    with row1_col3:
        fig_vol = px.pie(values=[54, 46], hole=0.7, color_discrete_sequence=['#facc15', '#262730'])
        fig_vol.update_layout(showlegend=False, height=140, margin=dict(t=0, b=0, l=0, r=0))
        st.write("Market Volatility")
        st.plotly_chart(fig_vol, use_container_width=True, config={'displayModeBar': False})

    with row1_col4:
        fig_def = px.pie(values=[82, 18], hole=0.7, color_discrete_sequence=['#ef4444', '#262730'])
        fig_def.update_layout(showlegend=False, height=140, margin=dict(t=0, b=0, l=0, r=0))
        st.write("Credit Default Risk")
        st.plotly_chart(fig_def, use_container_width=True, config={'displayModeBar': False})

    # 5. Row 2: Chart & Sidebar Info
    st.divider()
    row2_col1, row2_col2 = st.columns([2, 1])

    with row2_col1:
        st.subheader("Forecast Projection")
        chart_data = pd.DataFrame(
            np.random.randn(20, 2),
            columns=['Predicted', 'Baseline']
        )
        st.area_chart(chart_data)
        
        # Sub-metrics di bawah chart
        sm1, sm2, sm3 = st.columns(3)
        sm1.metric("Lower Bound", "62.1")
        sm2.metric("Mean Target", "74.2")
        sm3.metric("Confidence", "92.4%")

    with row2_col2:
        st.subheader("Top Risk Drivers")
        # Menggunakan container untuk grouping
        with st.container(border=True):
            st.write("🔴 Currency Devaluation (+4.2%)")
            st.write("🟡 Supply Chain Lag (+1.8%)")
            st.write("🔵 Cybersecurity Mesh (-0.4%)")
            st.write("🔴 Political Instability (+2.9%)")
        
        st.write("##")
        st.subheader("Simulation")
        sim_data = np.random.exponential(size=50)
        st.bar_chart(sim_data)

    # 6. Row 3: Table
    st.divider()
    st.subheader("Incidence Log")

    log_data = pd.DataFrame([
        {"Timestamp": "2023-10-24 14:22:01", "Entity": "EU_MARKET_NODE_04", "Severity": "CRITICAL", "Shift": "+24.2%"},
        {"Timestamp": "2023-10-24 13:58:45", "Entity": "LOGISTICS_CN_SHANGHAI", "Severity": "WARNING", "Shift": "+8.5%"},
        {"Timestamp": "2023-10-24 11:15:30", "Entity": "SEC_PROTOCOL_DELTA", "Severity": "LOW", "Shift": "-1.2%"},
    ])

    st.dataframe(log_data, use_container_width=True)