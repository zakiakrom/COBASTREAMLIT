import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(
    page_title="DataSense Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for Styling (Emulating Tailwind/Dark Theme)
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #101319;
        color: #e1e2eb;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #18181b !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(38, 39, 48, 0.4);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin-bottom: 1rem;
    }
    
    /* Custom Headers */
    .main-title {
        font-size: 2.25rem;
        font-weight: 700;
        color: #e1e2eb;
        margin-bottom: 0.5rem;
    }
    
    .sub-text {
        color: #c6c5d1;
        margin-bottom: 2rem;
    }

    .metric-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #c6c5d1;
        margin-bottom: 0.5rem;
    }

    .metric-value-primary {
        font-size: 2rem;
        font-weight: 700;
        color: #ffb3ae;
    }
    
    .metric-value-normal {
        font-size: 2rem;
        font-weight: 700;
        color: #e1e2eb;
    }

    /* Target specific Streamlit elements to match theme */
    div[data-testid="stMetricValue"] {
        color: #ffb3ae !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Component
with st.sidebar:
    st.markdown("## Analytics Pro")
    st.markdown("<p style='color: #71717a; font-size: 10px; margin-top: -15px;'>ENTERPRISE SUITE</p>", unsafe_allow_html=True)
    st.write("---")
    
    st.button("🏠 Dashboard", use_container_width=True)
    st.button("📈 Trending Products", use_container_width=True)
    st.button("🌐 Region Analysis", use_container_width=True)
    st.button("⚠️ Risk Prediction", use_container_width=True)
    
    st.write("---")
    # Profile section at bottom
    st.markdown("""
        <div style='display: flex; align-items: center; gap: 10px; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 8px;'>
            <div style='width: 32px; height: 32px; background: #3f3f46; border-radius: 50%;'></div>
            <div>
                <p style='margin: 0; font-size: 12px; font-weight: bold;'>Alex Rivers</p>
                <p style='margin: 0; font-size: 10px; color: #71717a;'>Lead Analyst</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 4. Header Section
col_title, col_actions = st.columns([2, 1])

with col_title:
    st.markdown('<h1 class="main-title">Market Overview</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-text">Real-time performance metrics across global regions.</p>', unsafe_allow_html=True)

with col_actions:
    st.write("##") # Spacer
    c1, c2 = st.columns(2)
    c1.button("📥 Export Report", type="primary", use_container_width=True)
    c2.button("🔍 Filters", use_container_width=True)

# 5. Key Metrics Row (Bento Style)
m1, m2, m3 = st.columns(3)

with m1:
    st.markdown("""
        <div class="glass-card">
            <p class="metric-label">Trending Product</p>
            <p class="metric-value-primary">UltraLink Pro</p>
            <p style="color: #4ade80; font-size: 14px;">↗ +24.8% this week</p>
        </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
        <div class="glass-card">
            <p class="metric-label">Total Analyzed</p>
            <p class="metric-value-normal">1.42M</p>
            <p style="color: #71717a; font-size: 14px;">📊 99.9% integrity</p>
        </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
        <div class="glass-card">
            <p class="metric-label">Top Region</p>
            <p style="color: #3cd7ff; font-size: 2rem; font-weight: 700;">North America</p>
            <p style="color: #3cd7ff; font-size: 14px;">🌐 38% revenue share</p>
        </div>
    """, unsafe_allow_html=True)

# 6. Charts Section
chart_col, region_col = st.columns([2, 1])

with chart_col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Product Sales Trends")
    
    # Generate dummy data for chart
    chart_data = pd.DataFrame(
        np.random.randn(20, 2) * [10, 5] + [100, 50],
        columns=['UltraLink', 'Legacy']
    )
    
    st.line_chart(chart_data, color=["#ff4b4b", "#71717a"])
    st.markdown('</div>', unsafe_allow_html=True)

with region_col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Top Regions")
    
    regions = {
        "North America": 85,
        "Europe": 65,
        "Asia Pacific": 58,
        "South America": 25
    }
    
    for region, val in regions.items():
        st.write(f"{region} - ${val*5}k")
        st.progress(val/100)
    
    st.write("##")
    st.button("View detailed report →", key="reg_btn")
    st.markdown('</div>', unsafe_allow_html=True)

# 7. Bottom Status Grid
st.markdown("### System Status")
s1, s2, s3, s4 = st.columns(4)

status_data = [
    ("Node Status", "98 Active", "🔴"),
    ("Sync Speed", "42ms avg", "🟢"),
    ("Storage", "12.4 TB", "🔵"),
    ("Threat Level", "Low Risk", "🟠")
]

for col, (label, val, icon) in zip([s1, s2, s3, s4], status_data):
    with col:
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);">
                <p style="font-size: 10px; color: #71717a; margin: 0;">{label}</p>
                <p style="font-size: 16px; font-weight: bold; margin: 0;">{icon} {val}</p>
            </div>
        """, unsafe_allow_html=True)

# Footer/FAB for Mobile (Simulated)
st.markdown("""
    <div style="position: fixed; bottom: 20px; right: 20px; z-index: 99;">
        <button style="background: #ff5351; color: white; border: none; width: 50px; height: 50px; border-radius: 50%; font-size: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); cursor: pointer;">
            +
        </button>
    </div>
""", unsafe_allow_html=True)