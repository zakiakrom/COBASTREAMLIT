import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import joblib
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ML Sales Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Dark Blue Futuristic Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ── Root Variables ── */
:root {
    --bg-primary:    #050d1a;
    --bg-card:       #0a1628;
    --bg-card2:      #0d1f3c;
    --accent-blue:   #2979ff;
    --accent-cyan:   #00e5ff;
    --accent-green:  #00e676;
    --accent-orange: #ff6d00;
    --text-primary:  #e8f0fe;
    --text-muted:    #7a8fb0;
    --border:        rgba(41, 121, 255, 0.18);
    --glow:          0 0 24px rgba(41, 121, 255, 0.25);
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

.stApp {
    background: linear-gradient(135deg, #050d1a 0%, #07152a 50%, #050d1a 100%);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07152a 0%, #050d1a 100%) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stDateInput label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: var(--text-primary) !important;
}

/* ── Sidebar Logo/Title ── */
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0 24px 0;
    font-family: 'Rajdhani', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: 1px;
}

.sidebar-logo .dot {
    width: 32px; height: 32px;
    border-radius: 50%;
    background: conic-gradient(var(--accent-blue), var(--accent-cyan), var(--accent-blue));
    box-shadow: 0 0 16px var(--accent-blue);
    animation: spin 4s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ── Sidebar nav items ── */
.nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 10px;
    font-size: 14px;
    color: var(--text-muted);
    cursor: pointer;
    transition: all 0.2s;
    margin-bottom: 4px;
}
.nav-item:hover, .nav-item.active {
    background: rgba(41, 121, 255, 0.15);
    color: var(--text-primary);
    border-left: 3px solid var(--accent-blue);
}

/* ── Metric Cards ── */
.metric-card {
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card2) 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--glow);
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-2px); }
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan));
}
.metric-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 6px;
}
.metric-value {
    font-family: 'Rajdhani', sans-serif;
    font-size: 36px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1;
}
.metric-sub {
    font-size: 12px;
    color: var(--accent-green);
    margin-top: 6px;
}
.metric-icon {
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 40px;
    opacity: 0.15;
}

/* ── Section Headers ── */
.section-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: 0.5px;
    margin-bottom: 2px;
}

/* ── Trending List ── */
.trend-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.trend-rank {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 14px;
    color: var(--accent-blue);
    width: 20px;
}
.trend-name { font-size: 14px; color: var(--text-primary); flex: 1; margin-left: 10px; }
.trend-pct  { font-size: 13px; font-weight: 600; color: var(--accent-green); }

/* ── Region List ── */
.region-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.region-bar-wrap { flex: 1; background: rgba(255,255,255,0.06); border-radius: 4px; height: 8px; }
.region-bar {
    height: 8px;
    border-radius: 4px;
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan));
}

/* ── Plotly chart container ── */
.chart-card {
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card2) 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    box-shadow: var(--glow);
}

/* ── ML Prediction section ── */
.predict-card {
    background: linear-gradient(135deg, #0d1f3c, #07152a);
    border: 1px solid rgba(0,229,255,0.2);
    border-radius: 16px;
    padding: 20px 24px;
    box-shadow: 0 0 24px rgba(0,229,255,0.1);
}
.predict-result {
    font-family: 'Rajdhani', sans-serif;
    font-size: 48px;
    font-weight: 700;
    color: var(--accent-cyan);
    text-shadow: 0 0 20px rgba(0,229,255,0.5);
}

/* ── Streamlit overrides ── */
div[data-testid="stMetricValue"] { color: var(--accent-cyan) !important; }
.stSelectbox > div > div { background: var(--bg-card2) !important; border-color: var(--border) !important; }
.stSlider .st-ey { background: var(--accent-blue) !important; }
button[kind="primary"] {
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan)) !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
}
hr { border-color: var(--border) !important; }
.stTabs [data-baseweb="tab"] {
    color: var(--text-muted);
    font-family: 'Rajdhani', sans-serif;
    font-size: 15px;
    font-weight: 600;
}
.stTabs [aria-selected="true"] { color: var(--accent-cyan) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HELPER: load model (ganti path sesuai model kamu)
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    path = "model.pkl"
    if os.path.exists(path):
        return joblib.load(path)
    return None

model = load_model()

# ─────────────────────────────────────────────
# DUMMY DATA (ganti dengan data asli kamu)
# ─────────────────────────────────────────────
@st.cache_data
def generate_sales_data(period="1M"):
    days = {"1W": 7, "1M": 30, "3M": 90, "1Y": 365}[period]
    dates = pd.date_range(end=datetime.today(), periods=days, freq="D")
    np.random.seed(42)
    base = np.linspace(5000, 23000, days)
    noise = np.random.normal(0, 1500, days)
    sales = (base + noise).clip(0)
    return pd.DataFrame({"date": dates, "sales": sales.astype(int)})

trending_products = [
    {"rank": 1, "name": "Smart Fitness Band",   "pct": "+72%"},
    {"rank": 2, "name": "Wireless Earbuds",      "pct": "+58%"},
    {"rank": 3, "name": "Home Security Camera",  "pct": "+45%"},
    {"rank": 4, "name": "Gaming Laptop",         "pct": "+39%"},
    {"rank": 5, "name": "Kitchen Blender",       "pct": "+31%"},
]

regions = [
    {"name": "West Coast",  "value": 54200, "pct": 54.2},
    {"name": "Northeast",   "value": 38700, "pct": 38.7},
    {"name": "Midwest",     "value": 32100, "pct": 32.1},
    {"name": "Southeast",   "value": 28500, "pct": 28.5},
    {"name": "Southwest",   "value": 21300, "pct": 21.3},
]

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="dot"></div>
        Dashboard
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="nav-item active">📊 &nbsp; Dashboard Overview</div>
    <div class="nav-item">🔥 &nbsp; Trending Products</div>
    <div class="nav-item">🗺️ &nbsp; Regional Sales</div>
    <div class="nav-item">🤖 &nbsp; ML Predictions</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**⚙️ Controls**")

    period = st.selectbox("Time Period", ["1W", "1M", "3M", "1Y"], index=1)

    st.markdown("---")
    st.markdown("**🤖 ML Input**")
    feature1 = st.slider("Feature 1 (e.g. Price)", 0, 1000, 250)
    feature2 = st.slider("Feature 2 (e.g. Rating)", 1.0, 5.0, 4.2, step=0.1)
    feature3 = st.selectbox("Category", ["Electronics", "Fashion", "Home", "Sports"])

    predict_btn = st.button("🔮 Run Prediction", use_container_width=True, type="primary")

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("""
    <p style="font-family:'Rajdhani',sans-serif;font-size:28px;font-weight:700;
              color:#e8f0fe;margin:0;letter-spacing:1px;">
        📡 ML Sales Intelligence Dashboard
    </p>
    <p style="font-size:13px;color:#7a8fb0;margin:4px 0 20px 0;">
        Real-time analytics · Machine Learning Insights · Jan 2024
    </p>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# METRIC CARDS
# ─────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Trending Product</div>
        <div class="metric-value" style="font-size:22px;">Smart Fitness Band</div>
        <div class="metric-sub">↑ +72% this month</div>
        <div class="metric-icon">⌚</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Total Products Analyzed</div>
        <div class="metric-value">8,450</div>
        <div class="metric-sub">↑ +12.4% vs last period</div>
        <div class="metric-icon">📦</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Top Region</div>
        <div class="metric-value" style="font-size:22px;">West Coast USA</div>
        <div class="metric-sub">54.2K units · 54% share</div>
        <div class="metric-icon">🌎</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN CHARTS ROW
# ─────────────────────────────────────────────
col_chart, col_trend = st.columns([2, 1])

with col_chart:
    df = generate_sales_data(period)

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df["date"], y=df["sales"],
        mode="lines+markers",
        line=dict(color="#2979ff", width=3, shape="spline"),
        marker=dict(color="#ffffff", size=7, line=dict(color="#2979ff", width=2)),
        fill="tozeroy",
        fillcolor="rgba(41,121,255,0.08)",
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Sales: %{y:,}<extra></extra>"
    ))

    fig_line.update_layout(
        title=dict(text="Product Sales Trends", font=dict(family="Rajdhani", size=18, color="#e8f0fe")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#7a8fb0", family="Inter"),
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", showline=False, tickfont=dict(size=11)),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", showline=False, tickfont=dict(size=11)),
        hovermode="x unified",
        height=320,
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col_trend:
    st.markdown("""
    <div class="metric-card" style="height:100%;">
        <div class="section-title">🔥 Trending Products</div>
        <br>
    """, unsafe_allow_html=True)

    for p in trending_products:
        st.markdown(f"""
        <div class="trend-item">
            <span class="trend-rank">{p['rank']}.</span>
            <span class="trend-name">{p['name']}</span>
            <span class="trend-pct">{p['pct']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAP + REGIONS
# ─────────────────────────────────────────────
col_map, col_regions = st.columns([3, 2])

with col_map:
    # USA Choropleth Map
    state_sales = {
        "CA": 32000, "WA": 22000, "OR": 18000,
        "NY": 25000, "NJ": 18000, "MA": 15000,
        "TX": 20000, "FL": 16000, "IL": 14000,
        "AZ": 12000, "CO": 11000, "NV": 10000,
        "GA": 9000,  "NC": 8500,  "VA": 8000,
        "OH": 7500,  "MI": 7000,  "PA": 9500,
        "MN": 6500,  "WI": 6000,
    }
    map_df = pd.DataFrame({"state": list(state_sales.keys()),
                            "sales": list(state_sales.values())})

    fig_map = go.Figure(go.Choropleth(
        locations=map_df["state"],
        z=map_df["sales"],
        locationmode="USA-states",
        colorscale=[
            [0.0,  "#050d1a"],
            [0.3,  "#0d2957"],
            [0.6,  "#1a4fb5"],
            [0.85, "#ff6d00"],
            [1.0,  "#ff1744"],
        ],
        colorbar=dict(
            title=dict(text="Sales", font=dict(color="#7a8fb0", size=11)),
            tickfont=dict(color="#7a8fb0", size=10),
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(255,255,255,0.1)",
            len=0.7,
        ),
        hovertemplate="<b>%{location}</b><br>Sales: %{z:,}<extra></extra>",
    ))
    fig_map.update_layout(
        title=dict(text="Sales by Region", font=dict(family="Rajdhani", size=18, color="#e8f0fe")),
        geo=dict(
            scope="usa",
            bgcolor="rgba(0,0,0,0)",
            lakecolor="rgba(0,0,0,0)",
            landcolor="#0a1628",
            subunitcolor="rgba(41,121,255,0.2)",
            showlakes=True,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=50, b=0),
        height=360,
        font=dict(color="#7a8fb0"),
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col_regions:
    st.markdown("""
    <div class="metric-card">
        <div class="section-title">🏆 Top Regions</div><br>
    """, unsafe_allow_html=True)

    max_val = max(r["value"] for r in regions)
    for i, r in enumerate(regions):
        bar_width = int(r["pct"] / max(r["pct"] for r in regions) * 100)
        st.markdown(f"""
        <div class="region-item">
            <span style="color:#7a8fb0;font-size:13px;width:14px;">{i+1}.</span>
            <span style="font-size:13px;color:#e8f0fe;width:90px;">{r['name']}</span>
            <div class="region-bar-wrap">
                <div class="region-bar" style="width:{bar_width}%;"></div>
            </div>
            <span style="font-size:13px;font-weight:600;color:#e8f0fe;margin-left:8px;width:46px;">
                {r['value']//1000:.1f}K
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ML PREDICTION SECTION
# ─────────────────────────────────────────────
st.markdown("""
<div style="font-family:'Rajdhani',sans-serif;font-size:20px;font-weight:700;
            color:#00e5ff;margin-bottom:12px;letter-spacing:1px;">
    🤖 Machine Learning Prediction Engine
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔮 Prediction", "📈 Model Performance", "📊 Feature Importance"])

with tab1:
    pred_col1, pred_col2 = st.columns([1, 2])

    with pred_col1:
        st.markdown("""
        <div class="predict-card">
            <div class="metric-label">Input Summary</div><br>
        </div>
        """, unsafe_allow_html=True)
        st.write(f"**Feature 1 (Price):** {feature1}")
        st.write(f"**Feature 2 (Rating):** {feature2}")
        st.write(f"**Category:** {feature3}")

    with pred_col2:
        if predict_btn:
            cat_enc = {"Electronics": 0, "Fashion": 1, "Home": 2, "Sports": 3}[feature3]
            input_arr = np.array([[feature1, feature2, cat_enc]])

            if model is not None:
                prediction = model.predict(input_arr)[0]
                try:
                    proba = model.predict_proba(input_arr)[0]
                    confidence = max(proba) * 100
                except:
                    confidence = 87.4
            else:
                # Demo mode: simple formula
                prediction = int(feature1 * feature2 * 12 + cat_enc * 500)
                confidence = 87.4

            st.markdown(f"""
            <div class="predict-card" style="text-align:center;padding:30px;">
                <div class="metric-label">Predicted Sales Volume</div>
                <div class="predict-result">{prediction:,}</div>
                <div style="color:#7a8fb0;font-size:13px;margin-top:8px;">
                    Confidence: <span style="color:#00e676;font-weight:600;">{confidence:.1f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Confidence bar
            conf_fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=confidence,
                domain={"x": [0, 1], "y": [0, 1]},
                gauge=dict(
                    axis=dict(range=[0, 100], tickcolor="#7a8fb0"),
                    bar=dict(color="#2979ff"),
                    bgcolor="rgba(255,255,255,0.05)",
                    bordercolor="rgba(255,255,255,0.1)",
                    steps=[
                        dict(range=[0, 50],  color="rgba(255,109,0,0.15)"),
                        dict(range=[50, 80], color="rgba(41,121,255,0.15)"),
                        dict(range=[80, 100],color="rgba(0,230,118,0.15)"),
                    ],
                ),
                number=dict(suffix="%", font=dict(color="#00e5ff", size=28)),
                title=dict(text="Model Confidence", font=dict(color="#7a8fb0", size=13)),
            ))
            conf_fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                height=220,
                margin=dict(l=20, r=20, t=20, b=0),
                font=dict(color="#7a8fb0"),
            )
            st.plotly_chart(conf_fig, use_container_width=True)
        else:
            st.markdown("""
            <div class="predict-card" style="text-align:center;padding:40px;">
                <div style="font-size:48px;margin-bottom:12px;opacity:0.4;">🤖</div>
                <div style="color:#7a8fb0;font-size:14px;">
                    Adjust parameters on the sidebar<br>and click <b style="color:#00e5ff;">Run Prediction</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    # Dummy model metrics
    m1, m2, m3, m4 = st.columns(4)
    metrics = [
        ("Accuracy",  "94.2%", "↑ +1.3%"),
        ("Precision", "91.8%", "↑ +0.8%"),
        ("Recall",    "93.1%", "↑ +1.1%"),
        ("F1 Score",  "92.4%", "↑ +0.9%"),
    ]
    for col, (label, val, delta) in zip([m1, m2, m3, m4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="text-align:center;">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="font-size:28px;">{val}</div>
                <div class="metric-sub">{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Confusion matrix heatmap
    cm = np.array([[420, 30, 12], [25, 380, 18], [8, 15, 392]])
    fig_cm = go.Figure(go.Heatmap(
        z=cm,
        x=["Predicted Low", "Predicted Mid", "Predicted High"],
        y=["Actual Low", "Actual Mid", "Actual High"],
        colorscale=[[0, "#050d1a"], [0.5, "#1a4fb5"], [1, "#00e5ff"]],
        text=cm, texttemplate="%{text}",
        hovertemplate="<b>%{y} → %{x}</b><br>Count: %{z}<extra></extra>",
        showscale=True,
    ))
    fig_cm.update_layout(
        title=dict(text="Confusion Matrix", font=dict(family="Rajdhani", size=16, color="#e8f0fe")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#7a8fb0"),
        margin=dict(l=10, r=10, t=50, b=10),
        height=300,
    )
    st.plotly_chart(fig_cm, use_container_width=True)

with tab3:
    features = ["Price", "Rating", "Category", "Stock Level", "Promo Active",
                "Day of Week", "Season", "Competitor Price"]
    importances = [0.31, 0.22, 0.18, 0.11, 0.08, 0.05, 0.03, 0.02]
    colors = ["#2979ff" if v > 0.15 else "#1a4fb5" if v > 0.08 else "#0d2957"
              for v in importances]

    fig_fi = go.Figure(go.Bar(
        x=importances[::-1],
        y=features[::-1],
        orientation="h",
        marker_color=colors[::-1],
        hovertemplate="<b>%{y}</b><br>Importance: %{x:.2%}<extra></extra>",
    ))
    fig_fi.update_layout(
        title=dict(text="Feature Importance", font=dict(family="Rajdhani", size=16, color="#e8f0fe")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#7a8fb0"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickformat=".0%"),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=50, b=10),
        height=340,
    )
    st.plotly_chart(fig_fi, use_container_width=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<p style="text-align:center;color:#3a4f6e;font-size:12px;">
    ML Sales Dashboard · Built with Streamlit + Plotly · Model: <code style="color:#2979ff;">model.pkl</code>
</p>
""", unsafe_allow_html=True)