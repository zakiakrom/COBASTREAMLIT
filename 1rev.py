import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

# # 1. Buat DataFrame dari feature importances
# df_importance = pd.DataFrame({
#     'feature': X.columns,
#     'importance': model.feature_importances_
# }).sort_values(by='importance', ascending=False)

# # 2. Plot menggunakan nama kolom yang sudah didefinisikan
# fig = px.bar(
#     df_importance, 
#     x='importance', 
#     y='feature', 
#     orientation='h',
#     title='Feature Importances XGBoost'
# )
# st.plotly_chart(fig)

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Revenue Prediction Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom Styling ───────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1e2a3a, #243447);
    border: 1px solid #2d4060;
    border-radius: 12px;
    padding: 16px;
}
[data-testid="stMetricValue"] { color: #00d4aa; font-size: 1.5rem !important; }
[data-testid="stMetricDelta"] { color: #82d3f0; }
[data-testid="stMetricLabel"] { color: #9fb3c8; }
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    padding: 8px 20px;
}
</style>
""", unsafe_allow_html=True)

# ─── Data Generator ───────────────────────────────────────────────────────────
@st.cache_data
def generate_data(n=3000, seed=42):
    rng = np.random.default_rng(seed)
    regions     = ['North', 'South', 'East', 'West']
    cities      = ['Mumbai', 'Delhi', 'Chennai', 'Kolkata', 'Hyderabad', 'Bengaluru']
    categories  = ['Electronics', 'Clothing', 'Furniture', 'Books', 'Sports']
    sub_cats    = ['Smartphones', 'Laptops', 'Shirts', 'Sofas', 'Novels', 'Cricket', 'Cameras']
    payments    = ['Card', 'UPI', 'NetBanking', 'COD']

    region   = rng.choice(regions,   n)
    city     = rng.choice(cities,    n)
    cat      = rng.choice(categories, n)
    sub_cat  = rng.choice(sub_cats,  n)
    payment  = rng.choice(payments,  n)

    quantity   = rng.integers(1, 15, n)
    unit_price = rng.uniform(200, 8000, n)
    discount   = rng.uniform(0, 0.5, n)
    is_trend   = rng.integers(0, 2, n)
    month      = rng.integers(1, 13, n)
    year       = rng.choice([2023, 2024, 2025], n)

    # Base sales with realistic noise
    base      = unit_price * quantity * (1 - discount * 0.6)
    trend_mul = np.where(is_trend == 1, rng.uniform(1.1, 1.5, n), rng.uniform(0.8, 1.1, n))
    cat_mul   = {'Electronics': 1.3, 'Furniture': 1.2, 'Sports': 1.0, 'Clothing': 0.9, 'Books': 0.7}
    c_mul     = np.array([cat_mul[c] for c in cat])
    noise     = rng.normal(1, 0.1, n)
    sales     = base * trend_mul * c_mul * noise
    profit    = sales * rng.uniform(0.05, 0.35, n)

    df = pd.DataFrame({
        'region': region, 'city': city, 'category': cat,
        'sub_category': sub_cat, 'payment_mode': payment,
        'quantity': quantity, 'unit_price': unit_price.round(2),
        'discount': discount.round(3), 'is_trending': is_trend,
        'month': month, 'year': year,
        'sales': sales.round(2), 'profit': profit.round(2)
    })
    df['profit_margin']    = (df['profit'] / df['sales']).round(4)
    df['revenue_per_unit'] = (df['sales']  / df['quantity']).round(2)
    df['log_sales']        = np.log1p(df['sales'])
    return df

# ─── Model Training ───────────────────────────────────────────────────────────
@st.cache_resource
def train_models(df):
    le_dict = {}
    df_enc = df.copy()
    for col in ['region', 'city', 'category', 'sub_category', 'payment_mode']:
        le = LabelEncoder()
        df_enc[col + '_enc'] = le.fit_transform(df_enc[col])
        le_dict[col] = le

    FEATURES = [
        'quantity', 'unit_price', 'discount', 'month', 'year',
        'is_trending', 'profit_margin', 'revenue_per_unit',
        'region_enc', 'city_enc', 'category_enc', 'sub_category_enc', 'payment_mode_enc'
    ]
    X = df_enc[FEATURES]
    y = df_enc['log_sales']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models_def = {
        'Random Forest':     RandomForestRegressor(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
        'Ridge Regression':  Ridge(alpha=1.0)
    }
    results = {}
    for name, model in models_def.items():
        model.fit(X_train, y_train)
        y_pred = np.expm1(model.predict(X_test))
        y_true = np.expm1(y_test)
        results[name] = {
            'model': model,
            'mae':  mean_absolute_error(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'r2':   r2_score(y_true, y_pred),
            'y_pred': y_pred,
            'y_true': y_true.values
        }

    best_name = max(results, key=lambda x: results[x]['r2'])
    return results, best_name, le_dict, FEATURES, X_test, y_test

# ─── Simulation ───────────────────────────────────────────────────────────────
@st.cache_data
def run_simulation(_best_model, _le_dict, df, FEATURES):
    def safe_enc(le, val):
        try:    return int(le.transform([val])[0])
        except: return 0

    rows = []
    for region in df['region'].unique():
        for cat in df['category'].unique():
            for trending in [0, 1]:
                sub = df[(df['region'] == region) & (df['category'] == cat)]
                if len(sub) == 0: continue
                row = {
                    'quantity':         sub['quantity'].mean(),
                    'unit_price':       sub['unit_price'].mean(),
                    'discount':         sub['discount'].mean(),
                    'month':            6, 'year': 2025,
                    'is_trending':      trending,
                    'profit_margin':    (sub['profit'] / sub['sales']).mean(),
                    'revenue_per_unit': (sub['sales'] / sub['quantity']).mean(),
                    'region_enc':       safe_enc(_le_dict['region'],   region),
                    'city_enc':         0,
                    'category_enc':     safe_enc(_le_dict['category'], cat),
                    'sub_category_enc': 0,
                    'payment_mode_enc': 0
                }
                pred = np.expm1(_best_model.predict(pd.DataFrame([row])[FEATURES])[0])
                rows.append({
                    'Region': region, 'Category': cat,
                    'Status': 'Trending' if trending else 'Non-Trending',
                    'Predicted Sales (₹)': round(pred, 2)
                })
    return pd.DataFrame(rows)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════════════════════════
df = generate_data()
results, best_name, le_dict, FEATURES, X_test, y_test = train_models(df)
best_model = results[best_name]['model']
df_sim = run_simulation(best_model, le_dict, df, FEATURES)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.divider()
    st.markdown("**Dataset**")
    st.info(f"🗂  {df.shape[0]:,} records\n\n📊 {df.shape[1]} features")

    st.markdown("**Best Model**")
    st.success(f"🏆 {best_name}")
    st.metric("R²", f"{results[best_name]['r2']:.4f}")
    st.metric("MAE", f"₹ {results[best_name]['mae']:,.0f}")
    st.metric("RMSE", f"₹ {results[best_name]['rmse']:,.0f}")

    st.divider()
    st.markdown("**Filter Data**")
    sel_region = st.selectbox("Region", df['region'].unique().tolist(),
                                default=df['region'].unique().tolist())
    sel_cat    = st.multiselect("Category", df['category'].unique().tolist(),
                                default=df['category'].unique().tolist())

df_f = df[(df['region'].isin([sel_region])) & (df['category'].isin(sel_cat))]

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("# 💰 Revenue Prediction Dashboard")
st.markdown("E-Commerce Sales Forecasting · ML Regression Pipeline")
st.divider()

# ─── KPI Row ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Revenue",   f"₹ {df_f['sales'].sum()/1e6:.2f}M",   f"+{len(df_f):,} records")
k2.metric("Avg Sale Value",  f"₹ {df_f['sales'].mean():,.0f}",       f"σ {df_f['sales'].std():,.0f}")
k3.metric("Avg Discount",    f"{df_f['discount'].mean()*100:.1f}%",   None)
k4.metric("Trending Share",  f"{df_f['is_trending'].mean()*100:.1f}%", None)
k5.metric("Avg Profit Margin",f"{df_f['profit_margin'].mean()*100:.1f}%", None)

st.divider()

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 EDA & Distributions",
    "🤖 Model Comparison",
    "🎯 Best Model Analysis",
    "🗺️ Simulation & Forecast",
    "🔮 Live Predictor"
])

# ══════════════════════════════════════════════════════
# TAB 1 ─ EDA
# ══════════════════════════════════════════════════════
with tab1:
    st.subheader("Exploratory Data Analysis")

    c1, c2 = st.columns(2)

    with c1:
        # Sales distribution
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Sales Distribution", "Log(Sales) Distribution"))
        fig.add_trace(go.Histogram(x=df_f['sales'], nbinsx=40, marker_color='#00d4aa',
                                   opacity=0.8, name='Sales'), row=1, col=1)
        fig.add_trace(go.Histogram(x=df_f['log_sales'], nbinsx=40, marker_color='#82d3f0',
                                   opacity=0.8, name='Log Sales'), row=1, col=2)
        fig.update_layout(title="Target Variable: Sales", showlegend=False,
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font_color='white', height=300, margin=dict(t=50, b=20))
        fig.update_xaxes(gridcolor='#2d4060'); fig.update_yaxes(gridcolor='#2d4060')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Sales by trending
        fig = px.box(df_f, x='is_trending', y='sales', color='is_trending',
                     color_discrete_map={0: '#95a5a6', 1: '#e74c3c'},
                     labels={'is_trending': 'Trending (1=Yes)', 'sales': 'Sales (₹)'},
                     title="Sales by Trending Status")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font_color='white', height=300, showlegend=False, margin=dict(t=50, b=20))
        fig.update_xaxes(gridcolor='#2d4060'); fig.update_yaxes(gridcolor='#2d4060')
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        cat_sales = df_f.groupby('category')['sales'].mean().sort_values().reset_index()
        fig = px.bar(cat_sales, x='sales', y='category', orientation='h',
                     color='sales', color_continuous_scale='teal',
                     labels={'sales': 'Avg Sales (₹)', 'category': ''},
                     title="Avg Sales per Category")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font_color='white', height=320, margin=dict(t=50, b=20),
                          coloraxis_showscale=False)
        fig.update_xaxes(gridcolor='#2d4060'); fig.update_yaxes(gridcolor='#2d4060')
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        reg_trend = df_f.groupby(['region', 'is_trending'])['sales'].mean().reset_index()
        reg_trend['Trending'] = reg_trend['is_trending'].map({0: 'Non-Trending', 1: 'Trending'})
        fig = px.bar(reg_trend, x='region', y='sales', color='Trending', barmode='group',
                     color_discrete_map={'Non-Trending': '#95a5a6', 'Trending': '#e74c3c'},
                     labels={'sales': 'Avg Sales (₹)', 'region': 'Region'},
                     title="Sales per Region: Trending vs Non-Trending")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font_color='white', height=320, margin=dict(t=50, b=20))
        fig.update_xaxes(gridcolor='#2d4060'); fig.update_yaxes(gridcolor='#2d4060')
        st.plotly_chart(fig, use_container_width=True)

    # Correlation heatmap
    num_cols = ['quantity', 'unit_price', 'discount', 'sales', 'profit_margin', 'is_trending']
    corr = df_f[num_cols].corr().round(3)
    fig = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r',
                    title="Feature Correlation Matrix", zmin=-1, zmax=1, aspect='auto')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white',
                      height=400, margin=dict(t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)

    # Monthly trend
    monthly = df_f.groupby('month')['sales'].sum().reset_index()
    fig = px.area(monthly, x='month', y='sales',
                  labels={'month': 'Month', 'sales': 'Total Sales (₹)'},
                  title="Monthly Total Revenue Trend",
                  color_discrete_sequence=['#00d4aa'])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      font_color='white', height=300, margin=dict(t=50, b=20))
    fig.update_xaxes(gridcolor='#2d4060', tickvals=list(range(1, 13)),
                     ticktext=['Jan','Feb','Mar','Apr','May','Jun',
                               'Jul','Aug','Sep','Oct','Nov','Dec'])
    fig.update_yaxes(gridcolor='#2d4060')
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════
# TAB 2 ─ Model Comparison
# ══════════════════════════════════════════════════════
with tab2:
    st.subheader("Model Comparison — Random Forest vs Gradient Boosting vs Ridge")

    metrics_df = pd.DataFrame({
        'Model': list(results.keys()),
        'R²': [results[m]['r2'] for m in results],
        'MAE (₹)': [results[m]['mae'] for m in results],
        'RMSE (₹)': [results[m]['rmse'] for m in results],
    })

    # Styled metrics table
    c1, c2, c3 = st.columns(3)
    cols = [c1, c2, c3]
    for i, (name, res) in enumerate(results.items()):
        trophy = "🏆 " if name == best_name else ""
        cols[i].metric(f"{trophy}{name}", f"R² = {res['r2']:.4f}",
                       f"MAE ₹{res['mae']:,.0f} · RMSE ₹{res['rmse']:,.0f}")

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        fig = px.bar(metrics_df, x='Model', y='R²', color='Model',
                     title="R² Score (Higher = Better)",
                     color_discrete_sequence=['#00d4aa', '#82d3f0', '#f5a623'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font_color='white', height=350, showlegend=False, margin=dict(t=50))
        fig.update_yaxes(range=[0, 1.05], gridcolor='#2d4060')
        fig.update_xaxes(gridcolor='#2d4060')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.bar(metrics_df, x='Model', y='MAE (₹)', color='Model',
                     title="MAE — Mean Absolute Error (Lower = Better)",
                     color_discrete_sequence=['#00d4aa', '#82d3f0', '#f5a623'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font_color='white', height=350, showlegend=False, margin=dict(t=50))
        fig.update_yaxes(gridcolor='#2d4060'); fig.update_xaxes(gridcolor='#2d4060')
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        fig = px.bar(metrics_df, x='Model', y='RMSE (₹)', color='Model',
                     title="RMSE — Root Mean Squared Error (Lower = Better)",
                     color_discrete_sequence=['#00d4aa', '#82d3f0', '#f5a623'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font_color='white', height=350, showlegend=False, margin=dict(t=50))
        fig.update_yaxes(gridcolor='#2d4060'); fig.update_xaxes(gridcolor='#2d4060')
        st.plotly_chart(fig, use_container_width=True)

    # Radar chart comparison
    cats  = ['R²', 'MAE Inv', 'RMSE Inv']
    max_mae  = max(r['mae']  for r in results.values())
    max_rmse = max(r['rmse'] for r in results.values())
    fig = go.Figure()
    colors = ['#00d4aa', '#82d3f0', '#f5a623']
    for (name, res), color in zip(results.items(), colors):
        vals = [
            res['r2'],
            1 - res['mae']  / max_mae,
            1 - res['rmse'] / max_rmse
        ]
        fig.add_trace(go.Scatterpolar(r=vals + [vals[0]], theta=cats + [cats[0]],
                                      fill='toself', name=name, line_color=color,
                                      fillcolor=color, opacity=0.25))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1],
                                   gridcolor='#2d4060', color='white'),
                   angularaxis=dict(color='white', gridcolor='#2d4060'),
                   bgcolor='rgba(0,0,0,0)'),
        paper_bgcolor='rgba(0,0,0,0)', font_color='white',
        title="Radar: Normalized Model Performance",
        height=420, margin=dict(t=60)
    )
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════
# TAB 3 ─ Best Model Analysis
# ══════════════════════════════════════════════════════
with tab3:
    st.subheader(f"Best Model Analysis — 🏆 {best_name}")

    y_pred = results[best_name]['y_pred']
    y_true = results[best_name]['y_true']
    residuals = y_true - y_pred

    c1, c2 = st.columns(2)

    with c1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=y_true, y=y_pred, mode='markers',
                                 marker=dict(color='#00d4aa', size=4, opacity=0.5),
                                 name='Predictions'))
        lim = max(y_true.max(), y_pred.max())
        fig.add_trace(go.Scatter(x=[0, lim], y=[0, lim], mode='lines',
                                 line=dict(color='red', dash='dash', width=2),
                                 name='Perfect Fit'))
        fig.update_layout(title="Actual vs Predicted Sales",
                          xaxis_title="Actual (₹)", yaxis_title="Predicted (₹)",
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font_color='white', height=400,
                          xaxis=dict(gridcolor='#2d4060'),
                          yaxis=dict(gridcolor='#2d4060'))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=y_pred, y=residuals, mode='markers',
                                 marker=dict(color='#f5a623', size=4, opacity=0.5),
                                 name='Residuals'))
        fig.add_hline(y=0, line_dash='dash', line_color='white', line_width=1.5)
        fig.update_layout(title="Residual Plot",
                          xaxis_title="Predicted (₹)", yaxis_title="Residual (₹)",
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font_color='white', height=400,
                          xaxis=dict(gridcolor='#2d4060'),
                          yaxis=dict(gridcolor='#2d4060'))
        st.plotly_chart(fig, use_container_width=True)

    # Feature importance
    if hasattr(best_model, 'feature_importances_'):
        fi = pd.Series(best_model.feature_importances_, index=FEATURES).sort_values()
        fig = px.bar(fi.reset_index(), x='feature_importances_', y='index',
                     orientation='h', color='feature_importances_',
                     color_continuous_scale='teal',
                     title=f"Feature Importance — {best_name}",
                     labels={'feature_importances_': 'Importance Score', 'index': 'Feature'})
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font_color='white', height=430, coloraxis_showscale=False,
                          margin=dict(t=50, b=20))
        fig.update_xaxes(gridcolor='#2d4060'); fig.update_yaxes(gridcolor='#2d4060')
        st.plotly_chart(fig, use_container_width=True)

    # Residual distribution
    fig = px.histogram(x=residuals, nbins=50, title="Residual Distribution",
                       labels={'x': 'Residual (₹)', 'y': 'Count'},
                       color_discrete_sequence=['#82d3f0'])
    fig.add_vline(x=0, line_dash='dash', line_color='red', line_width=2)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      font_color='white', height=300, margin=dict(t=50))
    fig.update_xaxes(gridcolor='#2d4060'); fig.update_yaxes(gridcolor='#2d4060')
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════
# TAB 4 ─ Simulation & Forecast
# ══════════════════════════════════════════════════════
with tab4:
    st.subheader("Prediction Simulation — Region × Category × Trending Status")

    top10 = (df_sim[df_sim['Status'] == 'Trending']
             .sort_values('Predicted Sales (₹)', ascending=False)
             .head(10))

    st.markdown("#### 🏆 Top 10 Highest Revenue Opportunities (Trending)")
    fig = px.bar(top10, x='Predicted Sales (₹)', y=top10['Region'] + ' · ' + top10['Category'],
                 orientation='h', color='Predicted Sales (₹)',
                 color_continuous_scale='teal',
                 labels={'y': 'Region · Category'},
                 title="Top 10 Predicted Sales — Trending Products")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      font_color='white', height=400, coloraxis_showscale=False,
                      margin=dict(t=50, b=20))
    fig.update_xaxes(gridcolor='#2d4060'); fig.update_yaxes(gridcolor='#2d4060')
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap: Region vs Category (Trending)
    pivot = df_sim[df_sim['Status'] == 'Trending'].pivot(
        index='Category', columns='Region', values='Predicted Sales (₹)')
    fig = px.imshow(pivot, text_auto='.0f', color_continuous_scale='teal',
                    title="Heatmap: Predicted Sales (₹) — Trending Products",
                    aspect='auto')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white',
                      height=380, margin=dict(t=50))
    st.plotly_chart(fig, use_container_width=True)

    # Trending vs Non-Trending comparison
    comp = df_sim.groupby(['Category', 'Status'])['Predicted Sales (₹)'].mean().reset_index()
    fig = px.bar(comp, x='Category', y='Predicted Sales (₹)', color='Status', barmode='group',
                 color_discrete_map={'Non-Trending': '#95a5a6', 'Trending': '#e74c3c'},
                 title="Avg Predicted Sales: Trending vs Non-Trending per Category")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      font_color='white', height=380, margin=dict(t=50))
    fig.update_xaxes(gridcolor='#2d4060'); fig.update_yaxes(gridcolor='#2d4060')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 📋 Full Simulation Table")
    st.dataframe(
        df_sim.sort_values('Predicted Sales (₹)', ascending=False)
              .reset_index(drop=True)
              .style.background_gradient(subset=['Predicted Sales (₹)'], cmap='YlGn'),
        use_container_width=True, height=400
    )


# ══════════════════════════════════════════════════════
# TAB 5 ─ Live Predictor
# ══════════════════════════════════════════════════════
with tab5:
    st.subheader("🔮 Live Revenue Predictor")
    st.markdown("Masukkan parameter produk untuk mendapatkan prediksi revenue secara real-time.")

    with st.form("prediction_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            region   = st.selectbox("Region", df['region'].unique())
            category = st.selectbox("Category", df['category'].unique())
            sub_cat  = st.selectbox("Sub Category", df['sub_category'].unique())
        with c2:
            quantity   = st.number_input("Quantity", min_value=1, max_value=50, value=5)
            unit_price = st.number_input("Unit Price (₹)", min_value=100.0, max_value=15000.0, value=2000.0, step=100.0)
            discount   = st.slider("Discount", 0.0, 0.5, 0.1, 0.01, format="%.2f")
        with c3:
            is_trending  = st.radio("Is Trending?", [0, 1], format_func=lambda x: "✅ Yes" if x else "❌ No")
            month        = st.selectbox("Month", list(range(1, 13)),
                                        format_func=lambda m: ['Jan','Feb','Mar','Apr','May','Jun',
                                                               'Jul','Aug','Sep','Oct','Nov','Dec'][m-1])
            year         = st.selectbox("Year", [2023, 2024, 2025])

        submitted = st.form_submit_button("🔮 Predict Revenue", use_container_width=True)

    if submitted:
        def safe_enc(le, val):
            try:    return int(le.transform([val])[0])
            except: return 0

        sub = df[(df['region'] == region) & (df['category'] == category)]
        profit_margin = (sub['profit'] / sub['sales']).mean() if len(sub) > 0 else 0.2
        rev_per_unit  = (sub['sales'] / sub['quantity']).mean() if len(sub) > 0 else unit_price

        row = {
            'quantity':         quantity,
            'unit_price':       unit_price,
            'discount':         discount,
            'month':            month,
            'year':             year,
            'is_trending':      is_trending,
            'profit_margin':    profit_margin,
            'revenue_per_unit': rev_per_unit,
            'region_enc':       safe_enc(le_dict['region'],       region),
            'city_enc':         0,
            'category_enc':     safe_enc(le_dict['category'],     category),
            'sub_category_enc': safe_enc(le_dict['sub_category'], sub_cat),
            'payment_mode_enc': 0
        }
        pred_val = np.expm1(best_model.predict(pd.DataFrame([row])[FEATURES])[0])

        st.divider()
        rc1, rc2, rc3, rc4 = st.columns(4)
        rc1.metric("💰 Predicted Revenue",   f"₹ {pred_val:,.2f}")
        rc2.metric("📦 Est. Profit",          f"₹ {pred_val * profit_margin:,.2f}")
        rc3.metric("📊 Model Used",           best_name)
        rc4.metric("🎯 Model R²",             f"{results[best_name]['r2']:.4f}")

        # Gauge chart
        max_sales = df['sales'].quantile(0.95)
        pct       = min(pred_val / max_sales, 1.0) * 100
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=pred_val,
            number={'prefix': '₹ ', 'valueformat': ',.0f'},
            title={'text': "Predicted Sales", 'font': {'color': 'white'}},
            delta={'reference': df['sales'].mean(), 'valueformat': ',.0f', 'prefix': '₹ '},
            gauge={
                'axis': {'range': [0, max_sales], 'tickcolor': 'white', 'tickfont': {'color': 'white'}},
                'bar': {'color': '#00d4aa'},
                'steps': [
                    {'range': [0, max_sales * 0.33], 'color': '#1e2a3a'},
                    {'range': [max_sales * 0.33, max_sales * 0.66], 'color': '#243447'},
                    {'range': [max_sales * 0.66, max_sales], 'color': '#2d4060'}
                ],
                'threshold': {
                    'line': {'color': 'red', 'width': 3},
                    'thickness': 0.75,
                    'value': df['sales'].mean()
                }
            }
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white',
                          height=320, margin=dict(t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)

        # Scenario comparison (no-trend vs trend)
        for t_val in [1 - is_trending]:
            row2 = {**row, 'is_trending': t_val}
            alt_pred = np.expm1(best_model.predict(pd.DataFrame([row2])[FEATURES])[0])

        labels = ['Current Prediction', 'Alternative (flip trending)']
        vals   = [pred_val, alt_pred]
        colors = ['#00d4aa', '#f5a623']
        fig = go.Figure([go.Bar(x=labels, y=vals, marker_color=colors,
                                text=[f"₹{v:,.0f}" for v in vals],
                                textposition='outside')])
        fig.update_layout(title="Scenario: Current vs Alternative Trending Status",
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font_color='white', height=320, margin=dict(t=50))
        fig.update_yaxes(gridcolor='#2d4060')
        st.plotly_chart(fig, use_container_width=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<div style='text-align:center; color:#9fb3c8; font-size:0.85rem;'>"
    "Revenue Prediction Dashboard · Built with Streamlit & Scikit-learn · "
    f"Model: {best_name} · R² = {results[best_name]['r2']:.4f}"
    "</div>",
    unsafe_allow_html=True
)