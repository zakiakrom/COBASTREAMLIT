import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Risk Analysis Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# STYLE
# ─────────────────────────────────────────────
# st.markdown("""
# <style>
#     [data-testid="stAppViewContainer"] {
#         background-color: #0f172a;
#         color: #e2e8f0;
#     }
#     [data-testid="stSidebar"] {
#         background-color: #1e293b;
#     }
#     .metric-card {
#         background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
#         border: 1px solid #334155;
#         border-radius: 12px;
#         padding: 20px;
#         text-align: center;
#     }
#     .section-title {
#         font-size: 1.2rem;
#         font-weight: 700;
#         color: #94a3b8;
#         letter-spacing: 0.05em;
#         text-transform: uppercase;
#         margin-bottom: 0.5rem;
#     }
#     div[data-testid="stMetricValue"] {
#         font-size: 2rem;
#         font-weight: 800;
#     }
#     div[data-testid="stMetricLabel"] {
#         font-size: 0.85rem;
#         color: #64748b;
#     }
#     .stDataFrame {
#         border-radius: 10px;
#     }
#     h1, h2, h3 {
#         color: #f1f5f9 !important;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ─────────────────────────────────────────────
# # GENERATE DATA SINTETIS
# # ─────────────────────────────────────────────
@st.cache_data
def generate_data(n_samples=5000, seed=42):
    np.random.seed(seed)
    regions   = ["West", "East", "Central", "South"]
    categories = ["Technology", "Furniture", "Office Supplies"]
    sub_cats  = {
        "Technology":      ["Phones", "Computers", "Accessories"],
        "Furniture":       ["Chairs", "Tables", "Bookcases"],
        "Office Supplies": ["Paper", "Binders", "Art"]
    }
    region_arr   = np.random.choice(regions,   n_samples)
    category_arr = np.random.choice(categories, n_samples)
    sub_cat_arr  = [np.random.choice(sub_cats[c]) for c in category_arr]
    unit_price   = np.random.uniform(5, 500, n_samples)
    quantity     = np.random.randint(1, 15, n_samples)
    discount     = np.random.choice([0.0, 0.1, 0.2, 0.3, 0.4, 0.5], n_samples,
                                    p=[0.40, 0.25, 0.15, 0.10, 0.07, 0.03])
    sales        = unit_price * quantity * (1 - discount)
    base_margin  = np.random.uniform(0.05, 0.45, n_samples)
    profit       = sales * base_margin - (discount * sales * 0.8)
    df = pd.DataFrame({
        "Region":     region_arr,
        "Category":   category_arr,
        "Sub_Category": sub_cat_arr,
        "Unit price": unit_price,
        "Quantity":   quantity,
        "Discount":   discount,
        "Sales":      np.round(sales, 2),
        "Profit":     np.round(profit, 2),
    })
    return df

# # ─────────────────────────────────────────────
# # PIPELINE UTAMA
# # ─────────────────────────────────────────────
@st.cache_resource
def run_pipeline(threshold_pct, n_samples):
    df = generate_data(n_samples)
    # Labeling
    df["Margin_Pct"] = (df["Profit"] / df["Sales"]) * 100
    threshold = df["Margin_Pct"].quantile(threshold_pct / 100)
    df["Is_Risk"] = (df["Margin_Pct"] < threshold).astype(int)
    # Encoding
    features = ["Region", "Category", "Discount", "Quantity", "Unit price"]
    X = df[features]
    y = df["Is_Risk"]
    X_encoded = pd.get_dummies(X, columns=["Region", "Category"], drop_first=True)
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42, stratify=y
    )
    # Train
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    report = classification_report(y_test, y_pred, output_dict=True)
    cm     = confusion_matrix(y_test, y_pred)
    importances = pd.Series(model.feature_importances_, index=X_encoded.columns)
    return df, model, X_encoded, X_train, X_test, y_train, y_test, y_pred, y_prob, report, cm, importances, threshold

# # ─────────────────────────────────────────────
# # SIDEBAR
# # ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/combo-chart--v1.png", width=100)
    st.title("⚙️ Konfigurasi")
    st.divider()

    n_samples = st.slider("Jumlah Data", min_value=100, max_value=5000,
                          value=5000, step=500,
                          help="Jumlah baris data sintetis yang di-generate")

    threshold_pct = st.slider("Threshold Risiko (%)", min_value=5, max_value=40,
                              value=15, step=5,
                              help="Persentil margin terendah yang dikategorikan 'Berisiko Tinggi'")

    st.divider()
    st.markdown("**📊 Tentang Model**")
    st.caption("""
    - **Algoritma:** Random Forest  
    - **Target:** Is_Risk (biner)  
    - **Fitur:** Region, Category, Discount, Quantity, Unit Price  
    - **Split:** 80% train / 20% test  
    """)
    st.divider()
    st.caption("E-Commerce Risk Analysis • 2024")

# # ─────────────────────────────────────────────
# # RUN PIPELINE
# # ─────────────────────────────────────────────
(df, model, X_encoded, X_train, X_test,
 y_train, y_test, y_pred, y_prob,
 report, cm, importances, threshold_val) = run_pipeline(threshold_pct, n_samples)

# # ─────────────────────────────────────────────
# # HEADER
# # ─────────────────────────────────────────────
st.markdown("## 🔍 E-Commerce Risk Analysis Dashboard")
st.caption(f"Dataset: **{len(df):,}** transaksi  •  Threshold margin risiko: **{threshold_val:.2f}%**")
st.divider()

# # ─────────────────────────────────────────────
# # SECTION 1 : METRIK UTAMA
# # ─────────────────────────────────────────────
st.markdown('<p class="section-title">📈 Ringkasan Model & Data</p>', unsafe_allow_html=True)

total_risk     = int(df["Is_Risk"].sum())
total_safe     = int((df["Is_Risk"] == 0).sum())
acc_val        = report["accuracy"]
precision_risk = report["1"]["precision"]
recall_risk    = report["1"]["recall"]
f1_risk        = report["1"]["f1-score"]

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Transaksi", f"{len(df):,}")
col2.metric("Transaksi Berisiko", f"{total_risk:,}", f"{total_risk/len(df)*100:.1f}%")
col3.metric("Akurasi Model", f"{acc_val*100:.1f}%")
col4.metric("Precision (Risk)", f"{precision_risk*100:.1f}%")
col5.metric("Recall (Risk)", f"{recall_risk*100:.1f}%")

st.divider()

# # ─────────────────────────────────────────────
# # SECTION 2 : DISTRIBUSI DATA & RISIKO
# # ─────────────────────────────────────────────
st.markdown('<p class="section-title">📊 Distribusi Data</p>', unsafe_allow_html=True)

row2a, row2b, row2c = st.columns(3)

# ── Pie: Risk vs Safe
with row2a:
    st.markdown("**Proporsi Risiko**")
    fig, ax = plt.subplots(figsize=(4, 4), facecolor="#0f172a")
    colors  = ["#22c55e", "#ef4444"]
    labels  = ["Aman", "Berisiko"]
    sizes   = [total_safe, total_risk]
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct="%1.1f%%",
        colors=colors, startangle=90,
        wedgeprops=dict(linewidth=2, edgecolor="#0f172a")
    )
    for t in texts + autotexts:
        t.set_color("white")
        t.set_fontsize(12)
    ax.set_facecolor("#0f172a")
    fig.patch.set_facecolor("#0f172a")
    st.pyplot(fig, use_container_width=True)
    plt.close()

# ── Bar: Risiko per Kategori
with row2b:
    st.markdown("**Risiko per Kategori**")
    cat_risk = df.groupby("Category")["Is_Risk"].mean().sort_values(ascending=True) * 100
    fig, ax  = plt.subplots(figsize=(5, 4), facecolor="#0f172a")
    bars = ax.barh(cat_risk.index, cat_risk.values,
                   color=["#ef4444" if v == cat_risk.max() else "#3b82f6"
                          for v in cat_risk.values], height=0.5)
    ax.set_xlabel("% Berisiko", color="#94a3b8", fontsize=10)
    ax.set_facecolor("#0f172a")
    fig.patch.set_facecolor("#0f172a")
    ax.tick_params(colors="#94a3b8")
    ax.spines[:].set_color("#334155")
    for bar in bars:
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f"{bar.get_width():.1f}%", va="center", color="white", fontsize=9)
    st.pyplot(fig, use_container_width=True)
    plt.close()

# ── Bar: Risiko per Region
with row2c:
    st.markdown("**Risiko per Region**")
    reg_risk = df.groupby("Region")["Is_Risk"].mean().sort_values(ascending=True) * 100
    fig, ax  = plt.subplots(figsize=(5, 4), facecolor="#0f172a")
    bars = ax.barh(reg_risk.index, reg_risk.values,
                   color=["#f59e0b" if v == reg_risk.max() else "#6366f1"
                          for v in reg_risk.values], height=0.5)
    ax.set_xlabel("% Berisiko", color="#94a3b8", fontsize=10)
    ax.set_facecolor("#0f172a")
    fig.patch.set_facecolor("#0f172a")
    ax.tick_params(colors="#94a3b8")
    ax.spines[:].set_color("#334155")
    for bar in bars:
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f"{bar.get_width():.1f}%", va="center", color="white", fontsize=9)
    st.pyplot(fig, use_container_width=True)
    plt.close()

# st.divider()

# # ─────────────────────────────────────────────
# # SECTION 3 : DISTRIBUSI MARGIN
# # ─────────────────────────────────────────────
# st.markdown('<p class="section-title">📉 Distribusi Margin Profit</p>', unsafe_allow_html=True)

# col_hist1, col_hist2 = st.columns(2)

# with col_hist1:
#     st.markdown("**Histogram Margin Profit (keseluruhan)**")
#     fig, ax = plt.subplots(figsize=(6, 3.5), facecolor="#0f172a")
#     safe_data = df[df["Is_Risk"] == 0]["Margin_Pct"]
#     risk_data = df[df["Is_Risk"] == 1]["Margin_Pct"]
#     ax.hist(safe_data, bins=50, color="#22c55e", alpha=0.7, label="Aman")
#     ax.hist(risk_data, bins=50, color="#ef4444", alpha=0.7, label="Berisiko")
#     ax.axvline(threshold_val, color="#facc15", linestyle="--", linewidth=1.5,
#                label=f"Threshold {threshold_val:.1f}%")
#     ax.set_xlabel("Margin (%)", color="#94a3b8")
#     ax.set_ylabel("Frekuensi",  color="#94a3b8")
#     ax.set_facecolor("#0f172a")
#     fig.patch.set_facecolor("#0f172a")
#     ax.tick_params(colors="#94a3b8")
#     ax.spines[:].set_color("#334155")
#     ax.legend(facecolor="#1e293b", labelcolor="white", fontsize=9)
#     st.pyplot(fig, use_container_width=True)
#     plt.close()

# with col_hist2:
#     st.markdown("**Margin per Diskon**")
#     df["Discount_Pct"] = (df["Discount"] * 100).astype(int).astype(str) + "%"
#     discount_margin = df.groupby("Discount_Pct")["Margin_Pct"].median().reset_index()
#     fig, ax = plt.subplots(figsize=(6, 3.5), facecolor="#0f172a")
#     bars = ax.bar(discount_margin["Discount_Pct"], discount_margin["Margin_Pct"],
#                   color=["#ef4444" if v < threshold_val else "#3b82f6"
#                          for v in discount_margin["Margin_Pct"]])
#     ax.axhline(threshold_val, color="#facc15", linestyle="--", linewidth=1.5,
#                label=f"Threshold {threshold_val:.1f}%")
#     ax.set_xlabel("Tingkat Diskon", color="#94a3b8")
#     ax.set_ylabel("Median Margin (%)", color="#94a3b8")
#     ax.set_facecolor("#0f172a")
#     fig.patch.set_facecolor("#0f172a")
#     ax.tick_params(colors="#94a3b8")
#     ax.spines[:].set_color("#334155")
#     ax.legend(facecolor="#1e293b", labelcolor="white", fontsize=9)
#     st.pyplot(fig, use_container_width=True)
#     plt.close()

# st.divider()

# # ─────────────────────────────────────────────
# # SECTION 4 : EVALUASI MODEL
# # ─────────────────────────────────────────────
# st.markdown('<p class="section-title">🤖 Evaluasi Model Random Forest</p>', unsafe_allow_html=True)

# col_cm, col_feat = st.columns(2)

# # ── Confusion Matrix
# with col_cm:
#     st.markdown("**Confusion Matrix**")
#     fig, ax = plt.subplots(figsize=(5, 4), facecolor="#0f172a")
#     cmap = sns.color_palette("Reds", as_cmap=True)
#     sns.heatmap(cm, annot=True, fmt="d", cmap=cmap,
#                 linewidths=2, linecolor="#0f172a",
#                 xticklabels=["Aman (0)", "Berisiko (1)"],
#                 yticklabels=["Aman (0)", "Berisiko (1)"],
#                 annot_kws={"size": 16, "weight": "bold", "color": "white"},
#                 ax=ax)
#     ax.set_xlabel("Prediksi", color="#94a3b8", fontsize=11)
#     ax.set_ylabel("Aktual",   color="#94a3b8", fontsize=11)
#     ax.tick_params(colors="#94a3b8")
#     fig.patch.set_facecolor("#0f172a")
#     ax.set_facecolor("#0f172a")
#     st.pyplot(fig, use_container_width=True)
#     plt.close()
#     # keterangan
#     tn, fp, fn, tp = cm.ravel()
#     st.caption(f"TP={tp:,}  |  FP={fp:,}  |  FN={fn:,}  |  TN={tn:,}")

# # ── Feature Importance
# with col_feat:
#     st.markdown("**Faktor Pemicu Risiko (Top 10)**")
#     top10 = importances.nlargest(10).sort_values(ascending=True)
#     palette = ["#ef4444" if i >= len(top10) - 3 else "#3b82f6"
#                for i in range(len(top10))]
#     fig, ax = plt.subplots(figsize=(5, 4), facecolor="#0f172a")
#     bars = ax.barh(top10.index, top10.values, color=palette, height=0.6)
#     ax.set_xlabel("Importance Score", color="#94a3b8", fontsize=10)
#     ax.set_facecolor("#0f172a")
#     fig.patch.set_facecolor("#0f172a")
#     ax.tick_params(colors="#94a3b8", labelsize=9)
#     ax.spines[:].set_color("#334155")
#     for bar in bars:
#         ax.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height()/2,
#                 f"{bar.get_width():.3f}", va="center", color="white", fontsize=8)
#     red_patch  = mpatches.Patch(color="#ef4444", label="Top 3 Faktor")
#     blue_patch = mpatches.Patch(color="#3b82f6", label="Faktor Lain")
#     ax.legend(handles=[red_patch, blue_patch],
#               facecolor="#1e293b", labelcolor="white", fontsize=8)
#     st.pyplot(fig, use_container_width=True)
#     plt.close()

# st.divider()

# # ─────────────────────────────────────────────
# # SECTION 5 : CLASSIFICATION REPORT
# # ─────────────────────────────────────────────
# st.markdown('<p class="section-title">📋 Classification Report</p>', unsafe_allow_html=True)

# report_df = pd.DataFrame(report).transpose().drop(["accuracy", "macro avg", "weighted avg"], errors="ignore")
# report_df = report_df[["precision", "recall", "f1-score", "support"]].rename(
#     index={"0": "Aman (0)", "1": "Berisiko (1)"}
# )
# report_df[["precision", "recall", "f1-score"]] = report_df[["precision", "recall", "f1-score"]].applymap(
#     lambda x: f"{x:.3f}"
# )
# report_df["support"] = report_df["support"].apply(lambda x: f"{int(x):,}")

# # Styling tabel
# def style_report(val):
#     try:
#         v = float(val.replace(",", ""))
#         if v >= 0.9:
#             return "background-color:#166534; color:white"
#         elif v >= 0.7:
#             return "background-color:#1e3a5f; color:white"
#         else:
#             return "background-color:#7f1d1d; color:white"
#     except:
#         return ""

# colr1, colr2 = st.columns([1, 2])
# with colr1:
#     st.dataframe(
#         report_df.style.applymap(style_report,
#                                  subset=["precision", "recall", "f1-score"]),
#         use_container_width=True
#     )

# with colr2:
#     # Bar chart precision/recall/f1 per kelas
#     metrics = ["precision", "recall", "f1-score"]
#     vals0 = [float(report["0"][m]) for m in metrics]
#     vals1 = [float(report["1"][m]) for m in metrics]
#     x = np.arange(len(metrics))
#     width = 0.3
#     fig, ax = plt.subplots(figsize=(6, 3), facecolor="#0f172a")
#     ax.bar(x - width/2, vals0, width, label="Aman (0)",    color="#22c55e", alpha=0.9)
#     ax.bar(x + width/2, vals1, width, label="Berisiko (1)", color="#ef4444", alpha=0.9)
#     ax.set_xticks(x)
#     ax.set_xticklabels(["Precision", "Recall", "F1-Score"], color="#94a3b8")
#     ax.set_ylim(0, 1.1)
#     ax.set_facecolor("#0f172a")
#     fig.patch.set_facecolor("#0f172a")
#     ax.tick_params(colors="#94a3b8")
#     ax.spines[:].set_color("#334155")
#     ax.legend(facecolor="#1e293b", labelcolor="white", fontsize=9)
#     ax.axhline(1.0, color="#334155", linestyle="--", linewidth=0.8)
#     for bars_set in [ax.containers[0], ax.containers[1]]:
#         ax.bar_label(bars_set, fmt="%.2f", color="white", fontsize=8, padding=2)
#     st.pyplot(fig, use_container_width=True)
#     plt.close()

# st.divider()

# # ─────────────────────────────────────────────
# # SECTION 6 : PREDIKSI MANUAL
# # ─────────────────────────────────────────────
st.markdown('<p class="section-title">🎯 Prediksi Transaksi Baru</p>', unsafe_allow_html=True)
st.caption("Masukkan data transaksi baru untuk memprediksi apakah berisiko tinggi atau tidak.")

with st.form("predict_form"):
    p1, p2, p3 = st.columns(3)
    with p1:
        inp_region   = st.selectbox("Region",   ["West", "East", "Central", "South"])
        inp_category = st.selectbox("Kategori", ["Technology", "Furniture", "Office Supplies"])
    with p2:
        inp_discount = st.slider("Diskon (%)", 0, 50, 10, step=5) / 100
        inp_qty      = st.number_input("Quantity", min_value=1, max_value=20, value=3)
    with p3:
        inp_price = st.number_input("Unit Price (Rp)", min_value=1.0, value=150.0, step=10.0)
        submitted = st.form_submit_button("🔍 Prediksi", use_container_width=True)

if submitted:
    inp_df = pd.DataFrame([{
        "Region":     inp_region,
        "Category":   inp_category,
        "Discount":   inp_discount,
        "Quantity":   inp_qty,
        "Unit price": inp_price,
    }])
    inp_enc = pd.get_dummies(inp_df, columns=["Region", "Category"], drop_first=True)
    # Sejajarkan kolom
    for col in X_encoded.columns:
        if col not in inp_enc.columns:
            inp_enc[col] = 0
    inp_enc = inp_enc[X_encoded.columns]

    pred  = model.predict(inp_enc)[0]
    prob  = model.predict_proba(inp_enc)[0][1] * 100
    sales = inp_price * inp_qty * (1 - inp_discount)

    rc1, rc2, rc3 = st.columns(3)
    rc1.metric("Estimasi Sales", f"Rp {sales:,.0f}")
    rc2.metric("Probabilitas Risiko", f"{prob:.1f}%")
    if pred == 1:
        rc3.markdown("### 🔴 **BERISIKO TINGGI**")
        st.error(f"⚠️ Transaksi ini diprediksi **BERISIKO** dengan probabilitas {prob:.1f}%. "
                  f"Pertimbangkan untuk mengurangi diskon atau meninjau harga produk.")
    else:
        rc3.markdown("### 🟢 **AMAN**")
        st.success(f"✅ Transaksi ini diprediksi **AMAN** dengan probabilitas risiko hanya {prob:.1f}%.")

# # ─────────────────────────────────────────────
# # SECTION 7 : TABEL DATA SAMPEL
# # ─────────────────────────────────────────────
with st.expander("📄 Lihat Sampel Data (50 baris pertama)", expanded=False):
    display_df = df[["Region", "Category", "Unit price", "Quantity",
                      "Discount", "Sales", "Profit", "Margin_Pct", "Is_Risk"]].head(50)
    display_df["Is_Risk"] = display_df["Is_Risk"].map({0: "✅ Aman", 1: "🔴 Risiko"})
    display_df["Margin_Pct"] = display_df["Margin_Pct"].round(2)
    st.dataframe(display_df, use_container_width=True, height=300)