import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
import os
import plotly.express as px

st.set_page_config(
    page_title="E-Commerce ML Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

CSV_PATH  = r"C:\PROJE\zeka\Data\Processed\cleaned_ecommerce_data.csv"
MODEL_DIR = r"C:\PROJE\zeka\Notebooks"

@st.cache_data
def load_data(path):
    # Tambahkan sep=';' agar Pandas tahu pemisahnya adalah titik koma
    df = pd.read_csv(path, sep=';')
    
    # Sekarang kolom "order_date" pasti terbaca
    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")


    if "quantity" in df.columns:
        median_qty = df["quantity"].median()
        df["is_trending"] = (df["quantity"] > median_qty).astype(int)
    
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

# ── Sidebar: navigasi saja ──
with st.sidebar:
    st.title("🛒 ML Dashboard")
    st.markdown("---")
    page = st.radio("📌 Halaman", [
        "📊 EDA Overview",
        "📈 Trending Analysis",
        "⚠️ Risk Prediction",
        "🎯 Recommendation",
        "🗺️ Region Analysis",
    ])
    st.markdown("---")
    st.caption(f"Total data: {len(df):,} baris")

# ─────────────────────────────────────────────
# HALAMAN 1: EDA OVERVIEW
# ─────────────────────────────────────────────
if page == "📊 EDA Overview":
    st.title("📊 EDA Overview")
    st.caption(f"Total {len(df):,} transaksi")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Penjualan",  f"Rp {df['sales'].sum():,.0f}")
    col2.metric("Total Profit",     f"Rp {df['profit'].sum():,.0f}")
    col3.metric("Jumlah Transaksi", f"{len(df):,}")
    avg_disc = df["discount"].mean() * 100 if "discount" in df.columns else 0
    col4.metric("Rata-rata Diskon", f"{avg_disc:.1f}%")

    st.markdown("---")

    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Tren Penjualan Bulanan")
        daily = df.groupby(df["order_date"].dt.to_period("M"))["sales"].sum().reset_index()
        daily["order_date"] = daily["order_date"].astype(str)
        fig = px.line(daily, x="order_date", y="sales",
                      labels={"order_date": "Bulan", "sales": "Total Penjualan"},
                      color_discrete_sequence=["#636EFA"])
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.subheader("Penjualan per Kategori")
        cat_s = df.groupby("product_name")["sales"].sum().sort_values(ascending=False).reset_index()
        fig2 = px.bar(cat_s, x="product_name", y="sales",
                      color="sales", color_continuous_scale="Blues",
                      labels={"product_name": "Produk", "sales": "Penjualan"})
        fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    col3a, col3b = st.columns(2)
    with col3a:
        st.subheader("Distribusi Profit")
        fig3 = px.histogram(df, x="profit", nbins=40,
                            color_discrete_sequence=["#00CC96"])
        fig3.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig3, use_container_width=True)

    with col3b:
        st.subheader("Top 10 Produk")
        top_p = df.groupby("product_name")["sales"].sum().nlargest(10).reset_index()
        fig4 = px.bar(top_p.sort_values("sales"), x="sales", y="product_name",
                      orientation="h", color_discrete_sequence=["#AB63FA"])
        fig4.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig4, use_container_width=True)

    with st.expander("📋 Lihat Data Mentah"):
        st.dataframe(df.head(100), use_container_width=True)

# ─────────────────────────────────────────────
# HALAMAN 2: TRENDING ANALYSIS
# ─────────────────────────────────────────────
elif page == "📈 Trending Analysis":
    st.title("📈 Trending Analysis")

    st.markdown("---")
    if "is_trending" in df.columns:
        col1, col2 = st.columns([1, 2])
        with col1:
            tc = df["is_trending"].value_counts()
            fig = go.Figure(data=[go.Pie(
                labels=["Tidak Trending", "Trending"],
                values=[tc.get(0, 0), tc.get(1, 0)],
                hole=0.45, marker_colors=["#EF553B", "#00CC96"]
            )])
            fig.update_layout(title="Proporsi Trending", margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Top Produk Trending")
            tc2 = (
                df[df["is_trending"] == 1]
                .groupby("product_name", as_index=False)   # ← as_index=False agar kolom tidak hilang
                .agg(jumlah_trending=("is_trending", "count"))  # ← nama kolom baru langsung di sini
                .sort_values("jumlah_trending", ascending=False)
                .head(15)
             )
            fig2 = px.bar(
                    tc2,
                    x="jumlah_trending",
                    y="product_name",
                    orientation="h",
                    color="jumlah_trending",
                    color_continuous_scale="Viridis",
                    labels={"product_name": "Produk", "jumlah_trending": "Jumlah Trending"}
                )
            fig2.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig2, use_container_width=True)

    else:
        st.info("Kolom `is_trending` tidak ditemukan di data.")



    st.subheader("🔮 Prediksi Trending Produk Baru")
    st.write("Model trending:", models.get("trending"))
    if models.get("trending") is not None:
        # Cek 1: apakah model terbaca?
            st.write("Model:", models.get("trending"))

    # Cek 2: fitur apa yang dipakai saat training?
    if models.get("trending") is not None:
        try:
            st.write("Fitur:", models["trending"].feature_names_in_.tolist())
        except:
            st.write("n_features:", models["trending"].n_features_in_)
    # else:
    #     st.info("Model trending tidak ditemukan.")

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
    

#     # --- 1. LOGIKA PEMBUATAN KOLOM (Tambahkan ini) ---
#     # Misal: Produk dianggap trending jika penjualan > rata-rata
#     if "is_trending" not in df.columns and "sales" in df.columns:
#         threshold = df["sales"].mean()
#     df["is_trending"] = (df["sales"] > threshold).astype(int)

# # --- 2. VISUALISASI (Kode kamu yang sudah diperbaiki) ---
#     if "is_trending" in df.columns:
#         col1, col2 = st.columns([1, 2])
    
#         with col1:
#         # Menggunakan .get() agar tidak error jika salah satu kategori (0 atau 1) tidak ada
#             tc = df["is_trending"].value_counts()
#             val_0 = tc.get(0, 0)
#             val_1 = tc.get(1, 0)
            
#             fig = go.Figure(data=[go.Pie(
#                 labels=["Tidak Trending", "Trending"],
#                 values=[val_0, val_1],
#                 hole=0.45, 
#                 marker_colors=["#EF553B", "#00CC96"]
#             )])
#             fig.update_layout(title="Proporsi Trending", margin=dict(l=0, r=0, t=40, b=0))
#             st.plotly_chart(fig, use_container_width=True)

#         with col2:
#             st.subheader("Produk Trending Teratas")
#             # Memperbaiki filter dan grouping
#             tc2 = (df[df["is_trending"] == 1]
#                 .groupby("product_name")
#                 .size()
#                 .reset_index(name="jumlah_trending")
#                 .sort_values("jumlah_trending", ascending=False)
#                 .head(10)) # Ambil top 10 agar chart tidak penuh
                
#             if not tc2.empty:
#                 fig2 = px.bar(tc2, x="product_name", y="jumlah_trending",
#                             color="jumlah_trending", color_continuous_scale="Viridis",
#                             labels={"product_name": "Nama Produk", "jumlah_trending": "Total Terjual"})
#                 st.plotly_chart(fig2, use_container_width=True)
#             else:
#                 st.warning("Tidak ada data produk yang memenuhi kriteria trending.")
        
#     else:
#         st.info("Kolom `is_trending` tidak ditemukan. Pastikan data memiliki kolom 'sales' untuk menghitung tren.")

#_________________________________________________________________________________________________
    
    # if models.get("trending") is not None:
    #     with st.form("trending_form"):
    #         ca, cb, cc = st.columns(3)
    #         with ca:
    #             qty = st.number_input("Quantity", min_value=1, value=10)
    #             price = st.number_input("Unit Price", min_value=0.0, value=50000.0)
    #         with cb:
    #             # Pastikan perhitungan diskon sesuai dengan input saat training
    #             discount_val = st.slider("Diskon (%)", 0, 50, 10) / 100 
    #             sales_val = st.number_input("Sales", min_value=0.0, value=500000.0)
    #         with cc:
    #             profit_val = st.number_input("Profit", value=50000.0)
            
    #         submitted = st.form_submit_button("Prediksi Trending ▶")

    #     if submitted:
    #         try:
    #             # Gunakan DataFrame agar nama fitur terbaca jika model menggunakan scikit-learn
    #             import pandas as pd
    #             input_data = pd.DataFrame([[qty, price, discount_val, sales_val, profit_val]], 
    #                                     columns=['quantity', 'unit_price', 'discount', 'sales', 'profit'])
                
    #             pred = models["trending"].predict(input_data)[0]
                
    #             # Cek apakah model mendukung predict_proba
    #             if hasattr(models["trending"], "predict_proba"):
    #                 prob = models["trending"].predict_proba(input_data)[0]
    #                 prob_val = f"{prob[1]*100:.1f}%"
    #             else:
    #                 prob_val = "N/A"

    #             if pred == 1:
    #                 st.success(f"✅ Produk ini **TRENDING** — Probabilitas: {prob_val}")
    #             else:
    #                 st.warning(f"⚠️ Produk ini **TIDAK trending** — Probabilitas: {prob_val}")
    #         except Exception as e:
    #             st.error(f"Prediksi gagal: {e}")
    # else:
    #     st.info("Model trending tidak ditemukan. Pastikan file model sudah di-load ke dictionary `models`.")



    # if models.get("trending") is not None:
    #     # Cek 1: apakah model terbaca?
    #     st.write("Model:", models.get("trending"))

    # # Cek 2: fitur apa yang dipakai saat training?
    # if models.get("trending") is not None:
    #     try:
    #         st.write("Fitur:", models["trending"].feature_names_in_.tolist())
    #     except:
    #         st.write("n_features:", models["trending"].n_features_in_)


    #     st.write("Model trending:", models.get("trending"))
    #     with st.form("trending_form"):
    #         ca, cb, cc = st.columns(3)
    #         with ca:
    #             qty       = st.number_input("Quantity", min_value=1, value=10)
    #             price     = st.number_input("Unit Price", min_value=0.0, value=50000.0)
    #         with cb:
    #             discount  = st.slider("Diskon (%)", 0, 50, 10) / 100
    #             sales_val = st.number_input("Sales", min_value=0.0, value=500000.0)
    #         with cc:
    #             profit_val = st.number_input("Profit", value=50000.0)
    #         submitted = st.form_submit_button("Prediksi Trending ▶")

    #     if submitted:
    #         try:
    #             pred = models["trending"].predict([[qty, price, discount, sales_val, profit_val]])[0]
    #             prob = models["trending"].predict_proba([[qty, price, discount, sales_val, profit_val]])[0]
    #             if pred == 1:
    #                 st.success(f"✅ Produk ini **TRENDING** — Probabilitas: {prob[1]*100:.1f}%")
    #             else:
    #                 st.warning(f"⚠️ Produk ini **TIDAK trending** — Probabilitas trending: {prob[1]*100:.1f}%")
    #         except Exception as e:
    #             st.error(f"Prediksi gagal: {e}")
    #  else:
    #      st.info("Model trending tidak ditemukan.")

##################################################################################################

# ─────────────────────────────────────────────
# HALAMAN 3: RISK PREDICTION
# ─────────────────────────────────────────────
elif page == "⚠️ Risk Prediction":
    st.title("⚠️ Risk Prediction")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribusi Profit per Region")
        fig = px.box(df, x="region", y="profit", color="region")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Profit vs Diskon")
        fig2 = px.scatter(df.sample(min(1000, len(df))),
                          x="discount", y="profit", color="product_name", opacity=0.6)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("🔮 Prediksi Risiko Transaksi")

    if models.get("risk") is not None:
        with st.form("risk_form"):
            ra, rb = st.columns(2)
            with ra:
                r_qty      = st.number_input("Quantity", min_value=1, value=5, key="risk_qty")
                r_price    = st.number_input("Unit Price", min_value=0.0, value=100000.0, key="risk_price")
                r_discount = st.slider("Diskon (%)", 0, 80, 20, key="risk_disc") / 100
            with rb:
                r_sales  = st.number_input("Sales", min_value=0.0, value=500000.0, key="risk_sales")
                r_profit = st.number_input("Profit (bisa negatif)", value=-10000.0, key="risk_profit")
            r_sub = st.form_submit_button("Cek Risiko ▶")

        # LOGIKA EKSEKUSI
        if r_sub:
            try:
                # Pastikan urutan [r_qty, r_price, r_discount, r_sales, r_profit] 
                # sama dengan saat training model
                input_risk = [[r_qty, r_price, r_discount, r_sales, r_profit]]
                res_risk = models["risk"].predict(input_risk)[0]
                
                if res_risk == 1:
                    st.error("🚨 Transaksi ini terdeteksi BERISIKO TINGGI!")
                else:
                    st.success("✅ Transaksi ini tergolong Aman.")
            except Exception as e:
                st.error(f"Gagal melakukan cek risiko: {e}")
    else:
        st.info("Model analisis risiko belum tersedia.")

    # if models.get("risk") is not None:
    #     with st.form("risk_form"):
    #         ra, rb = st.columns(2)
    #         with ra:
    #             r_qty      = st.number_input("Quantity", min_value=1, value=5)
    #             r_price    = st.number_input("Unit Price", min_value=0.0, value=100000.0)
    #             r_discount = st.slider("Diskon (%)", 0, 80, 20) / 100
    #         with rb:
    #             r_sales  = st.number_input("Sales", min_value=0.0, value=500000.0)
    #             r_profit = st.number_input("Profit (bisa negatif)", value=-10000.0)
    #         r_sub = st.form_submit_button("Cek Risiko ▶")

    #     if r_sub:
    #         try:
    #             r_pred = models["risk"].predict([[r_qty, r_price, r_discount, r_sales, r_profit]])[0]
    #             r_prob = models["risk"].predict_proba([[r_qty, r_price, r_discount, r_sales, r_profit]])[0]
    #             label_map = {0: "Rendah 🟢", 1: "Sedang 🟡", 2: "Tinggi 🔴"}
    #             st.metric("Level Risiko", label_map.get(r_pred, str(r_pred)))
    #             st.bar_chart(pd.DataFrame({"Probabilitas": r_prob}, index=["Rendah", "Sedang", "Tinggi"]))
    #         except Exception as e:
    #             st.error(f"Prediksi gagal: {e}")
    # else:
        # st.info("Model risk tidak ditemukan.")

# ─────────────────────────────────────────────
# HALAMAN 4: RECOMMENDATION
# ─────────────────────────────────────────────
elif page == "🎯 Recommendation":
    st.title("🎯 Product Recommendation")

    rec_region = st.selectbox("Region", sorted(df["region"].unique().tolist()))

    # col1, col2 = st.columns(2)
    # with col1:
    #     rec_region = st.selectbox("Region", sorted(df["region"].unique().tolist()))
    # with col2:
    #     rec_product = st.selectbox("Produk", sorted(df["product_name"].unique().tolist()))
    # st.markdown("---")

    agg_dict = {
        "total_sales": ("sales", "sum"),
        "total_qty":   ("quantity", "sum"),
        "avg_profit":  ("profit", "mean"),
    }
    # if "is_trending" in df.columns:
    #     agg_dict["trending_rate"] = ("is_trending", "mean")

    # Tampilkan top 10 produk terlaris di region yang dipilih
    mask = df["region"] == rec_region

    top_rec = (df[mask]
            .groupby("product_name")
            .agg(**agg_dict)
            .sort_values("total_sales", ascending=False)
            .head(10)
            .reset_index())

    if len(top_rec) > 0:
        fig = px.bar(
            top_rec, x="total_sales", y="product_name",
            orientation="h", color="avg_profit",
            color_continuous_scale="RdYlGn",
            labels={"total_sales": "Total Penjualan",
                    "product_name": "Produk",
                    "avg_profit": "Rata-rata Profit"},
            title=f"Top 10 Produk di {rec_region}"
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(top_rec, use_container_width=True)
    else:
        st.warning("Tidak ada data untuk region ini.")

    # mask = (df["region"] == rec_region) & (df["product_name"] == rec_product)
    # top_rec = (df[mask]
    #            .agg(**agg_dict)
    #            .to_frame("value")
    #            .reset_index()
    #            .rename(columns={"index": "metrik"}))

    # if len(top_rec) > 0:
    #     st.subheader(f"Ringkasan — {rec_product} di {rec_region}")
    #     st.dataframe(top_rec, use_container_width=True)
    # else:
    #     st.warning("Tidak ada data untuk kombinasi ini.")

# elif page == "🎯 Recommendation":
#     st.title("🎯 Product Recommendation")

#     col1, col2 = st.columns(2)
#     with col1:
#         rec_region = st.selectbox("Region", sorted(df["region"].unique().tolist()))
#     with col2:
#         rec_category = st.selectbox("Kategori", sorted(df["product_name"].unique().tolist()))
#     st.markdown("---")



#     agg_dict = {
#         "total_sales": ("sales", "sum"),
#         "total_qty":   ("quantity", "sum"),
#         "avg_profit":  ("profit", "mean"),
#     }

#     if "is_trending" in df.columns:
#         agg_dict["trending_rate"] = ("is_trending", "mean")

#     mask = (df["region"] == rec_region) & (df["categorp"] == rec_category)
#     top_rec = (df[mask].groupby("product_name")
#                .agg(**agg_dict)
#                .sort_values("total_sales", ascending=False)
#                .head(10).reset_index())

#     if len(top_rec) > 0:
#         fig = px.bar(top_rec, x="total_sales", y="product_name",
#                      orientation="h", color="avg_profit",
#                      color_continuous_scale="RdYlGn",
#                      labels={"total_sales": "Total Penjualan",
#                              "product_name": "Produk",
#                              "avg_profit": "Rata-rata Profit"},
#                      title=f"Top 10 Produk — {rec_category} di {rec_region}")
#         fig.update_layout(yaxis=dict(autorange="reversed"))
#         st.plotly_chart(fig, use_container_width=True)
#         st.dataframe(top_rec, use_container_width=True)
#     else:
#         st.warning("Tidak ada data untuk kombinasi ini.")

# ─────────────────────────────────────────────
# HALAMAN 5: REGION ANALYSIS
# ─────────────────────────────────────────────
elif page == "🗺️ Region Analysis":
    st.title("🗺️ Region Analysis")

    # Normalisasi nama kolom
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Cek kolom wajib
    kolom_wajib = ["region", "sales", "profit", "discount", "product_name",]
    kolom_hilang = [k for k in kolom_wajib if k not in df.columns]
    if kolom_hilang:
        st.error(f"Kolom berikut tidak ditemukan di data: {kolom_hilang}")
        st.stop()

    if df.empty:
        st.warning("Data kosong!")
        st.stop()

    # Buat ringkasan per region
    region_summary = (df.groupby("region")
                        .agg(total_sales=("sales", "sum"),
                             total_profit=("profit", "sum"),
                            #  total_orders=("order_id", "count"),
                             avg_discount=("discount", "mean"))
                        .reset_index())

    # Chart
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
    pivot = df.groupby(["region", "product_name"])["sales"].sum().unstack(fill_value=0)
    fig3 = px.imshow(pivot, aspect="auto", color_continuous_scale="Blues",
                     labels=dict(x="Kategori", y="Region", color="Total Penjualan"))
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Tabel Ringkasan Region")
    tbl = region_summary.copy()
    tbl["avg_discount"] = (tbl["avg_discount"] * 100).round(1).astype(str) + "%"
    tbl.columns = ["Region", "Total Penjualan", "Total Profit", "Total Order", "Rata-rata Diskon"]
    st.dataframe(tbl, use_container_width=True)

#     st.title("🗺️ Region Analysis")

#     df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

#     #   # Cek kolom yang tersedia dulu
#     # agg_region = {"total_sales": ("sales", "sum"), "total_profit": ("profit", "sum")}
    
#     # if "order_id" in df.columns:
#     #     agg_region["total_orders"] = ("order_id", "count")
#     # else:
#     #     agg_region["total_orders"] = ("sales", "count")  # pakai kolom lain untuk hitung baris

#     # if "discount" in df.columns:
#     #     agg_region["avg_discount"] = ("discount", "mean")


#     # Cek apakah kolom region ada dan tidak kosong
#     print("region" in df.columns)
#     print(df["region"].isna().sum())  # Berapa banyak nilai kosong



#     print(df.columns.tolist())
#     print(df.dtypes)

#     region_summary = (df.groupby("region")
#                       .agg(total_sales=("sales", "sum"),
#                            total_profit=("profit", "sum"),
#                            total_orders=("order_id", "count"),
#                            avg_discount=("discount", "mean"))
#                       .reset_index())
    
#     # Definisi HARUS ada sebelum dipakai
#     agg_region = {
#         "total_sales": ("sales", "sum"),
#         "total_profit": ("profit", "sum"),
#         "total_orders": ("order_id", "count"),
#         "avg_discount": ("discount", "mean"),
#     }

#     region_summary = (df.groupby("region")
#                         .agg(**agg_region)
#                         .reset_index())
    
#         # ✅ Dict yang benar pakai string sebagai key
#     agg_region = {
#         "sales": "sum",
#         "profit": "sum",
#         "order_id": "count",
#         "discount": "mean"
#     }

#     region_summary = (df.groupby("region")
#                         .agg(agg_region)  # Tanpa **
#                         .reset_index())

#     # Rename kolom setelahnya
#     region_summary.columns = ["region", "total_sales", "total_profit", "total_orders", "avg_discount"]

#     col1, col2 = st.columns(2)
#     with col1:
#         st.subheader("Total Penjualan per Region")
#         fig = px.pie(region_summary, values="total_sales", names="region",
#                      hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
#         fig.update_layout(margin=dict(l=0, r=0, t=10, b=0))
#         st.plotly_chart(fig, use_container_width=True)

#     with col2:
#         st.subheader("Profit vs Penjualan per Region")
#         fig2 = px.scatter(region_summary, x="total_sales", y="total_profit",
#                           size="total_orders", color="region", text="region", size_max=50)
#         fig2.update_traces(textposition="top center")
#         fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0))
#         st.plotly_chart(fig2, use_container_width=True)

#     st.subheader("Heatmap: Penjualan Region × Kategori")
#     pivot = df.groupby(["region", "category"])["sales"].sum().unstack(fill_value=0)
#     fig3 = px.imshow(pivot, aspect="auto", color_continuous_scale="Blues",
#                      labels=dict(x="Kategori", y="Region", color="Total Penjualan"))
#     st.plotly_chart(fig3, use_container_width=True)

#     st.subheader("Tabel Ringkasan Region")
#     tbl = region_summary.copy()
#     tbl["avg_discount"] = (tbl["avg_discount"] * 100).round(1).astype(str) + "%"
#     tbl.columns = ["Region", "Total Penjualan", "Total Profit", "Total Order", "Rata-rata Diskon"]
#     st.dataframe(tbl, use_container_width=True)