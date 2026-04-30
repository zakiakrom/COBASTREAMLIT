import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

def show():
    # st.title("region analysis")

    # # 2. Custom CSS (Meniru Tema Dark & Glassmorphism Tailwind)
    # # st.markdown("""
    # #     <style>
    # #     /* Background Utama */
    # #     .stApp {
    # #         background-color: #101319;
    # #         color: #e1e2eb;
    # #     }
        
    # #     /* Sidebar */
    # #     section[data-testid="stSidebar"] {
    # #         background-color: #18181b !important;
    # #         border-right: 1px solid rgba(255, 255, 255, 0.05);
    # #     }

    # #     /* Container Glassmorphism */
    # #     .glass-card {
    # #         background: rgba(39, 42, 49, 0.4);
    # #         backdrop-filter: blur(8px);
    # #         border: 1px solid rgba(255, 255, 255, 0.1);
    # #         padding: 1.5rem;
    # #         border-radius: 0.75rem;
    # #         margin-bottom: 1rem;
    # #     }

    # #     /* Styling Teks & Header */
    # #     .metric-title {
    # #         color: #9ca3af;
    # #         font-size: 0.75rem;
    # #         text-transform: uppercase;
    # #         font-weight: bold;
    # #         margin-bottom: 5px;
    # #     }
        
    # #     .metric-value {
    # #         font-size: 1.8rem;
    # #         font-weight: 700;
    # #         letter-spacing: -0.02em;
    # #     }

    # #     .status-performing { color: #10b981; font-size: 0.7rem; font-weight: bold; }
    # #     .status-atrisk { color: #ef4444; font-size: 0.7rem; font-weight: bold; }

    # #     /* Override Streamlit Progress Bar */
    # #     div[st-testid="stMarkdownContainer"] p { margin-bottom: 0; }
    # #     .stProgress > div > div > div > div { background-color: #ff4b4b; }
    # #     </style>
    # #     """, unsafe_allow_html=True)


        
    # st.write("---")
    # st.markdown("""
    #         <div style='background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);'>
    #             <p style='font-size: 10px; color: #6b7280; margin:0;'>SYSTEM STATUS</p>
    #             <div style='display: flex; align-items: center; gap: 8px; margin-top: 5px;'>
    #                 <div style='width: 8px; height: 8px; background: #10b981; border-radius: 50%;'></div>
    #                 <span style='font-size: 12px;'>Live Server Syncing</span>
    #             </div>
    #         </div>
    #     """, unsafe_allow_html=True)

    # # 4. Header Section
    # head_col1, head_col2 = st.columns([3, 1])
    # with head_col1:
    #     st.markdown("<h1 style='margin-bottom:0;'>Global Sales Distribution</h1>", unsafe_allow_html=True)
    #     st.markdown("<p style='color: #6b7280;'>Visualizing regional performance metrics and market penetration across top-tier economic zones.</p>", unsafe_allow_html=True)

    # with head_col2:
    #     st.write("##") # Spacer
    #     c1, c2 = st.columns(2)
    #     c1.button("Filter", icon="🔍")
    #     c2.button("Export CSV", type="primary")

    # # 5. Metrics Grid (Bento Style)
    # m1, m2, m3, m4 = st.columns(4)

    # with m1:
    #     st.markdown("""<div class='glass-card'><p class='metric-title'>Total Regional Sales</p><p class='metric-value'>$4.28M</p><p class='status-performing'>▲ +12.4% vs LY</p></div>""", unsafe_allow_html=True)
    # with m2:
    #     st.markdown("""<div class='glass-card'><p class='metric-title'>Active Markets</p><p class='metric-value'>142</p><p class='status-performing'>✓ 98.2% Reach</p></div>""", unsafe_allow_html=True)
    # with m3:
    #     st.markdown("""<div class='glass-card'><p class='metric-title'>Avg Margin</p><p class='metric-value'>31.8%</p><p class='status-atrisk'>▼ -1.2% MoM</p></div>""", unsafe_allow_html=True)
    # with m4:
    #     st.markdown("""<div class='glass-card'><p class='metric-title'>Growth Forecast</p><p class='metric-value'>18.5%</p><p style='color:#3cd7ff; font-size:0.7rem; font-weight:bold;'>⚡ High Potential</p></div>""", unsafe_allow_html=True)

    # # 6. Interactive Map & Analytics Panel
    # col_map, col_stats = st.columns([2, 1])

    # with col_map:
    #     st.markdown("<div class='glass-card' style='height: 520px;'>", unsafe_allow_html=True)
    #     st.subheader("Live Distribution Hub")
        
    #     # Dummy data untuk peta (koordinat kota besar)
    #     map_data = pd.DataFrame({
    #         'lat': [40.7128, 51.5074, 1.3521, -6.2088],
    #         'lon': [-74.0060, -0.1278, 103.8198, 106.8456],
    #         'name': ['New York', 'London', 'Singapore', 'Jakarta']
    #     })
    #     st.map(map_data, color="#ff4b4b", size=200, use_container_width=True)
    #     st.markdown("</div>", unsafe_allow_html=True)

    # with col_stats:
    #     st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    #     st.markdown("<p class='metric-title'>Regional Breakdown</p>", unsafe_allow_html=True)
        
    #     regions = [
    #         ("ASIA-PACIFIC", 42, "$2.1M Revenue"),
    #         ("NORTH AMERICA", 31, "$1.5M Revenue"),
    #         ("EUROPEAN UNION", 18, "$0.9M Revenue"),
    #         ("LATAM & OTHER", 9, "$0.4M Revenue")
    #     ]
        
    #     for name, val, rev in regions:
    #         st.write(f"**{name}**")
    #         st.progress(val / 100)
    #         st.caption(f"{rev} | {val}% Contribution")
    #         st.write("")
        
    #     st.markdown("""
    #         <div style='background: #1f2937; border: 1px solid #374151; padding: 15px; border-radius: 10px; margin-top: 10px;'>
    #             <p style='color: white; font-weight: bold; font-size: 13px;'>Analysis Insight</p>
    #             <p style='color: #9ca3af; font-size: 11px;'>Asian markets are outpacing forecasts due to rapid fintech adoption. Recommend shifting 15% more budget to Singapore.</p>
    #         </div>
    #     """, unsafe_allow_html=True)
    #     st.markdown("</div>", unsafe_allow_html=True)

    # # 7. Granular Sales Ledger (Table)
    # st.markdown("### Granular Sales Ledger")
    # data = {
    #     "Region / Hub": ["North America East", "Western Europe Hub", "South East Asia"],
    #     "Location": ["New Jersey, US", "Berlin, DE", "Singapore City, SG"],
    #     "Transaction Vol": ["2,481", "1,920", "4,209"],
    #     "Gross Revenue": ["$842,000", "$654,100", "$2,104,500"],
    #     "Net Profit": ["$210,500", "$142,000", "$590,000"],
    #     "Status": ["PERFORMING", "AT RISK", "EXCEPTIONAL"]
    # }

    # df = pd.DataFrame(data)

    # # Custom table display using dataframe
    # st.dataframe(
    #     df, 
    #     use_container_width=True, 
    #     hide_index=True,
    #     column_config={
    #         "Status": st.column_config.TextColumn(
    #             "Status",
    #             help="Regional status based on KPIs",
    #             width="medium"
    #         )
    #     }
    # )

    # SETELAN LEBAR HALAMAN DAN IKON
    st.set_page_config(
        page_title="Sales Dashboard",
        page_icon="📊",
        layout="wide"
    )


    # 1. Konfigurasi Halaman
    st.set_page_config(
        page_title="Region Analysis | DataSense",
        page_icon="🌐",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 3. Header Section
    head_col1, head_col2 = st.columns([3, 1])
    with head_col1:
        st.title("Global Sales Distribution")
        st.write("Visualizing regional performance metrics and market penetration across top-tier economic zones.")

    with head_col2:
        st.write("##") # Spacer
        c1, c2 = st.columns(2)
        c1.button("Filter", icon="🔍", use_container_width=True)
        c2.button("Export", type="primary", icon="📄", use_container_width=True)

    # 4. Metrics Grid (Menggunakan st.metric bawaan)
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        with st.container(border=True):
            st.metric("Total Regional Sales", "$4.28M", delta="12.4% vs LY")
    with m2:
        with st.container(border=True):
            st.metric("Active Markets", "142", delta="98.2% Reach", delta_color="normal")
    with m3:
        with st.container(border=True):
            st.metric("Avg Margin", "31.8%", delta="-1.2% MoM", delta_color="inverse")
    with m4:
        with st.container(border=True):
            st.metric("Growth Forecast", "18.5%", delta="High Potential", delta_color="off")

    # 5. Interactive Map & Analytics Panel
    col_map, col_stats = st.columns([2, 1])

    with col_map:
        with st.container(border=True):
            st.subheader("Live Distribution Hub")
            
            # Data untuk peta
            map_data = pd.DataFrame({
                'lat': [40.7128, 51.5074, 1.3521, -6.2088],
                'lon': [-74.0060, -0.1278, 103.8198, 106.8456],
            })
            st.map(map_data, color="#ff4b4b", size=200)

    with col_stats:
        with st.container(border=True):
            st.subheader("Regional Breakdown")
            
            regions = [
                ("ASIA-PACIFIC", 42, "$2.1M Revenue"),
                ("NORTH AMERICA", 31, "$1.5M Revenue"),
                ("EUROPEAN UNION", 18, "$0.9M Revenue"),
                ("LATAM & OTHER", 9, "$0.4M Revenue")
            ]
            
            for name, val, rev in regions:
                st.write(f"**{name}**")
                st.progress(val / 100)
                st.caption(f"{rev} | {val}% Contribution")
            
            st.info("**Analysis Insight**: Asian markets are outpacing forecasts. Recommend shifting 15% more budget to Singapore.", icon="💡")

    # 6. Granular Sales Ledger (Menggunakan st.dataframe dengan Column Config)
    st.divider()
    st.subheader("Granular Sales Ledger")

    data = pd.DataFrame([
        {"Region": "North America East", "Location": "New Jersey, US", "Vol": 2481, "Revenue": 842000, "Status": "PERFORMING"},
        {"Region": "Western Europe Hub", "Location": "Berlin, DE", "Vol": 1920, "Revenue": 654100, "Status": "AT RISK"},
        {"Region": "South East Asia", "Location": "Singapore City, SG", "Vol": 4209, "Revenue": 2104500, "Status": "EXCEPTIONAL"},
    ])

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Revenue": st.column_config.NumberColumn("Gross Revenue", format="$%d"),
            "Vol": st.column_config.NumberColumn("Transaction Vol", format="%d 📦"),
            "Status": st.column_config.SelectboxColumn(
                "Status",
                options=["PERFORMING", "AT RISK", "EXCEPTIONAL"],
                required=True,
            ),
        }
    )