import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
import os

# ─────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce ML Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# PATH — sesuaikan jika perlu
# ─────────────────────────────────────────────
# ── GANTI PATH INI sesuai lokasi file CSV kamu ──
CSV_PATH  = r"C:\PROJE\zeka\Data\Processed\cleaned_ecommerce_data.csv"
MODEL_DIR = r"C:\PROJE\zeka\Notebooks"

@st.cache_data
def load_data(path):
    # Tambahkan sep=';' agar Pandas tahu pemisahnya adalah titik koma
    df = pd.read_csv(path, sep=';')
    
    # Sekarang kolom "order_date" pasti terbaca
    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    
    return df

@st.cache_resource
def load_model(path):
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception:
        return None

#── Load data ──
if not os.path.exists(CSV_PATH):
    st.error(f"❌ File tidak ditemukan:\n`{CSV_PATH}`")
else:
    df = load_data(CSV_PATH)


# ── Load models ──
models = {
    "trending":       load_model(os.path.join(MODEL_DIR, "model_trending.pkl")),
    "risk":           load_model(os.path.join(MODEL_DIR, "risk_model.pkl")),
    "recommendation": load_model(os.path.join(MODEL_DIR, "model_recommendation.pkl")),
    "forecast":       load_model(os.path.join(MODEL_DIR, "forecast_model.pkl")),
    "le_category":    load_model(os.path.join(MODEL_DIR, "le_category.pkl")),
    "le_product":     load_model(os.path.join(MODEL_DIR, "le_product.pkl")),
    "le_region":      load_model(os.path.join(MODEL_DIR, "le_region.pkl")),
    "encoders":       load_model(os.path.join(MODEL_DIR, "encoders.pkl")),
}

# CSV_PATH  = r"C:\PROJE\zeka\Data\Processed\cleaned_ecommerce_data.csv"
# MODEL_DIR = r"C:\PROJE\zeka\Notebooks"

# @st.cache_data
# def load_data(path):
#     df = pd.read_csv(path)
#     df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
#     return df

# @st.cache_resource
# def load_model(path):
#     try:
#         with open(path, "rb") as f:
#             return pickle.load(f)
#     except Exception:
#         return None

# # ── Load data ──
# if not os.path.exists(CSV_PATH):
#     st.error(f"❌ File tidak ditemukan: `{CSV_PATH}`")
#     uploaded = st.file_uploader("Upload cleaned_ecommerce_data.csv", type="csv")
#     if uploaded:
#         df = pd.read_csv(uploaded)
#         df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
#         st.success(f"✅ Data dimuat: {len(df):,} baris")
#     else:
#         st.stop()
# else:
#     df = load_data(CSV_PATH)

# # ── Load models ──
# models = {
#     "trending":       load_model(os.path.join(MODEL_DIR, "model_trending.pkl")),
#     "risk":           load_model(os.path.join(MODEL_DIR, "risk_model.pkl")),
#     "recommendation": load_model(os.path.join(MODEL_DIR, "model_recommendation.pkl")),
#     "forecast":       load_model(os.path.join(MODEL_DIR, "forecast_model.pkl")),
#     "le_category":    load_model(os.path.join(MODEL_DIR, "le_category.pkl")),
#     "le_product":     load_model(os.path.join(MODEL_DIR, "le_product.pkl")),
#     "le_region":      load_model(os.path.join(MODEL_DIR, "le_region.pkl")),
#     "encoders":       load_model(os.path.join(MODEL_DIR, "encoders.pkl")),
# }

# ─────────────────────────────────────────────
# SIDEBAR — hanya navigasi
# ─────────────────────────────────────────────
with st.sidebar:
    st.title("🛒 ML Dashboard")
    st.markdown("---")
    page = st.radio ("📌 Halaman", [
        "📊 EDA Overview",
        "📈 Trending Analysis",
        "⚠️ Risk Prediction",
        "🎯 Recommendation",
        "🗺️ Region Analysis",
    ])
    st.caption(f"Total data: {len(df):,} baris")

# ─────────────────────────────────────────────
# HELPER — widget filter per halaman
# ─────────────────────────────────────────────
def filter_bar(key, show_date=True, show_region=True, show_category=True):
    fdf = df.copy()
    n_cols = (2 if show_date else 0) + (1 if show_region else 0) + (1 if show_category else 0)
    cols = st.columns(n_cols)
    idx = 0

    if show_date:
        min_d = df["order_date"].min().date()
        max_d = df["order_date"].max().date()
        with cols[idx]:
            start = st.date_input("Dari", value=min_d, min_value=min_d, max_value=max_d, key=f"{key}_start")
        with cols[idx + 1]:
            end = st.date_input("Sampai", value=max_d, min_value=min_d, max_value=max_d, key=f"{key}_end")
        fdf = fdf[(fdf["order_date"].dt.date >= start) & (fdf["order_date"].dt.date <= end)]
        idx += 2

    if show_region:
        with cols[idx]:
            sel_region = st.selectbox("Region", ["Semua"] + sorted(df["region"].unique().tolist()), key=f"{key}_region")
        if sel_region != "Semua":
            fdf = fdf[fdf["region"] == sel_region]
        idx += 1

    if show_category:
        with cols[idx]:
            sel_cat = st.selectbox("Kategori", ["Semua"] + sorted(df["category"].unique().tolist()), key=f"{key}_cat")
        if sel_cat != "Semua":
            fdf = fdf[fdf["category"] == sel_cat]

    st.caption(f"Menampilkan **{len(fdf):,}** dari {len(df):,} transaksi")
    st.markdown("---")
    return fdf

# ─────────────────────────────────────────────
# HALAMAN 1: EDA OVERVIEW
# ─────────────────────────────────────────────
if page == "📊 EDA Overview":
    st.title("📊 EDA Overview")
    fdf = filter_bar("eda", show_date=True, show_region=True, show_category=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Penjualan",  f"Rp {fdf['sales'].sum():,.0f}")
    col2.metric("Total Profit",     f"Rp {fdf['profit'].sum():,.0f}")
    col3.metric("Jumlah Transaksi", f"{len(fdf):,}")
    avg_disc = fdf["discount"].mean() * 100 if "discount" in fdf.columns else 0
    col4.metric("Rata-rata Diskon", f"{avg_disc:.1f}%")

    st.markdown("---")

    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Tren Penjualan Bulanan")
        daily = fdf.groupby(fdf["order_date"].dt.to_period("M"))["sales"].sum().reset_index()
        daily["order_date"] = daily["order_date"].astype(str)
        fig = px.line(daily, x="order_date", y="sales",
                      labels={"order_date": "Bulan", "sales": "Total Penjualan"},
                      color_discrete_sequence=["#636EFA"])
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.subheader("Penjualan per Kategori")
        cat_s = fdf.groupby("category")["sales"].sum().sort_values(ascending=False).reset_index()
        fig2 = px.bar(cat_s, x="category", y="sales",
                      color="sales", color_continuous_scale="Blues",
                      labels={"category": "Kategori", "sales": "Penjualan"})
        fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    col3a, col3b = st.columns(2)
    with col3a:
        st.subheader("Distribusi Profit")
        fig3 = px.histogram(fdf, x="profit", nbins=40,
                            color_discrete_sequence=["#00CC96"])
        fig3.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig3, use_container_width=True)

    with col3b:
        st.subheader("Top 10 Produk")
        top_p = fdf.groupby("product_name")["sales"].sum().nlargest(10).reset_index()
        fig4 = px.bar(top_p.sort_values("sales"), x="sales", y="product_name",
                      orientation="h", color_discrete_sequence=["#AB63FA"])
        fig4.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig4, use_container_width=True)

    with st.expander("📋 Lihat Data Mentah"):
        st.dataframe(fdf.head(100), use_container_width=True)

# ─────────────────────────────────────────────
# HALAMAN 2: TRENDING ANALYSIS
# ─────────────────────────────────────────────
elif page == "📈 Trending Analysis":
    st.title("📈 Trending Analysis")
    fdf = filter_bar("trend", show_date=True, show_region=False, show_category=True)

    if "is_trending" in fdf.columns:
        col1, col2 = st.columns([1, 2])
        with col1:
            tc = fdf["is_trending"].value_counts()
            fig = go.Figure(data=[go.Pie(
                labels=["Tidak Trending", "Trending"],
                values=[tc.get(0, 0), tc.get(1, 0)],
                hole=0.45, marker_colors=["#EF553B", "#00CC96"]
            )])
            fig.update_layout(title="Proporsi Trending", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Produk Trending per Kategori")
            tc2 = (fdf[fdf["is_trending"] == 1]
                   .groupby("category")["product_name"].count()
                   .reset_index()
                   .rename(columns={"product_name": "jumlah_trending"})
                   .sort_values("jumlah_trending", ascending=False))
            fig2 = px.bar(tc2, x="category", y="jumlah_trending",
                          color="jumlah_trending", color_continuous_scale="Viridis")
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Kolom `is_trending` tidak ditemukan di data.")

    st.markdown("---")
    st.subheader("🔮 Prediksi Trending Produk Baru")
    if models.get("trending") is not None:
        with st.form("trending_form"):
            ca, cb, cc = st.columns(3)
            with ca:
                qty       = st.number_input("Quantity", min_value=1, value=10)
                price     = st.number_input("Unit Price", min_value=0.0, value=50000.0)
            with cb:
                discount  = st.slider("Diskon (%)", 0, 50, 10) / 100
                sales_val = st.number_input("Sales", min_value=0.0, value=500000.0)
            with cc:
                profit_val = st.number_input("Profit", value=50000.0)
            submitted = st.form_submit_button("Prediksi Trending ▶")
        if submitted:
            try:
                pred = models["trending"].predict([[qty, price, discount, sales_val, profit_val]])[0]
                prob = models["trending"].predict_proba([[qty, price, discount, sales_val, profit_val]])[0]
                if pred == 1:
                    st.success(f"✅ Produk ini **TRENDING** — Probabilitas: {prob[1]*100:.1f}%")
                else:
                    st.warning(f"⚠️ Produk ini **TIDAK trending** — Probabilitas trending: {prob[1]*100:.1f}%")
            except Exception as e:
                st.error(f"Prediksi gagal: {e}")
    else:
        st.info("Model trending tidak ditemukan.")

# ─────────────────────────────────────────────
# HALAMAN 3: RISK PREDICTION
# ─────────────────────────────────────────────
elif page == "⚠️ Risk Prediction":
    st.title("⚠️ Risk Prediction")
    fdf = filter_bar("risk", show_date=True, show_region=True, show_category=False)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribusi Profit per Region")
        fig = px.box(fdf, x="region", y="profit", color="region")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Profit vs Diskon")
        fig2 = px.scatter(fdf.sample(min(1000, len(fdf))),
                          x="discount", y="profit", color="category", opacity=0.6)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("🔮 Prediksi Risiko Transaksi")
    if models.get("risk") is not None:
        with st.form("risk_form"):
            ra, rb = st.columns(2)
            with ra:
                r_qty      = st.number_input("Quantity", min_value=1, value=5)
                r_price    = st.number_input("Unit Price", min_value=0.0, value=100000.0)
                r_discount = st.slider("Diskon (%)", 0, 80, 20) / 100
            with rb:
                r_sales  = st.number_input("Sales", min_value=0.0, value=500000.0)
                r_profit = st.number_input("Profit (bisa negatif)", value=-10000.0)
            r_sub = st.form_submit_button("Cek Risiko ▶")
        if r_sub:
            try:
                r_pred = models["risk"].predict([[r_qty, r_price, r_discount, r_sales, r_profit]])[0]
                r_prob = models["risk"].predict_proba([[r_qty, r_price, r_discount, r_sales, r_profit]])[0]
                label_map = {0: "Rendah 🟢", 1: "Sedang 🟡", 2: "Tinggi 🔴"}
                st.metric("Level Risiko", label_map.get(r_pred, str(r_pred)))
                st.bar_chart(pd.DataFrame({"Probabilitas": r_prob}, index=["Rendah", "Sedang", "Tinggi"]))
            except Exception as e:
                st.error(f"Prediksi gagal: {e}")
    else:
        st.info("Model risk tidak ditemukan.")

# ─────────────────────────────────────────────
# HALAMAN 4: RECOMMENDATION
# ─────────────────────────────────────────────
elif page == "🎯 Recommendation":
    st.title("🎯 Product Recommendation")

    st.markdown("#### Filter Rekomendasi")
    col1, col2 = st.columns(2)
    with col1:
        rec_region = st.selectbox("Region", sorted(df["region"].unique().tolist()))
    with col2:
        rec_category = st.selectbox("Kategori", sorted(df["category"].unique().tolist()))
    st.markdown("---")

    agg_dict = {
        "total_sales": ("sales", "sum"),
        "total_qty":   ("quantity", "sum"),
        "avg_profit":  ("profit", "mean"),
    }
    if "is_trending" in df.columns:
        agg_dict["trending_rate"] = ("is_trending", "mean")

    mask = (df["region"] == rec_region) & (df["category"] == rec_category)
    top_rec = (df[mask].groupby("product_name")
               .agg(**agg_dict)
               .sort_values("total_sales", ascending=False)
               .head(10).reset_index())

    if len(top_rec) > 0:
        fig = px.bar(top_rec, x="total_sales", y="product_name",
                     orientation="h", color="avg_profit",
                     color_continuous_scale="RdYlGn",
                     labels={"total_sales": "Total Penjualan",
                             "product_name": "Produk",
                             "avg_profit": "Rata-rata Profit"},
                     title=f"Top 10 Produk — {rec_category} di {rec_region}")
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(top_rec, use_container_width=True)
    else:
        st.warning("Tidak ada data untuk kombinasi filter ini.")

# ─────────────────────────────────────────────
# HALAMAN 5: REGION ANALYSIS
# ─────────────────────────────────────────────
elif page == "🗺️ Region Analysis":
    st.title("🗺️ Region Analysis")
    fdf = filter_bar("region_page", show_date=True, show_region=False, show_category=True)

    region_summary = (fdf.groupby("region")
                      .agg(total_sales=("sales","sum"),
                           total_profit=("profit","sum"),
                           total_orders=("order_id","count"),
                           avg_discount=("discount","mean"))
                      .reset_index())

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Total Penjualan per Region")
        fig = px.pie(region_summary, values="total_sales", names="region",
                     hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Profit vs Penjualan per Region")
        fig2 = px.scatter(region_summary, x="total_sales", y="total_profit",
                          size="total_orders", color="region", text="region", size_max=50)
        fig2.update_traces(textposition="top center")
        fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Heatmap: Penjualan Region × Kategori")
    pivot = fdf.groupby(["region", "category"])["sales"].sum().unstack(fill_value=0)
    fig3 = px.imshow(pivot, aspect="auto", color_continuous_scale="Blues",
                     labels=dict(x="Kategori", y="Region", color="Total Penjualan"))
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Tabel Ringkasan Region")
    tbl = region_summary.copy()
    tbl["avg_discount"] = (tbl["avg_discount"] * 100).round(1).astype(str) + "%"
    tbl.columns = ["Region", "Total Penjualan", "Total Profit", "Total Order", "Rata-rata Diskon"]
    st.dataframe(tbl, use_container_width=True)