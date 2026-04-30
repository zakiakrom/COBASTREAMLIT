# import streamlit as st
# import pandas as pd
# import numpy as np
# import pickle
# import plotly.express as px
# import plotly.graph_objects as go
# import os
# import sys
# import joblib 

# st.set_page_config(
#     page_title="E-Commerce ML Dashboard",
#     page_icon="🛒",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ── GANTI PATH INI sesuai lokasi file CSV kamu ──
# CSV_PATH  = r"C:\PROJE\zeka\Data\Processed\cleaned_ecommerce_data.csv"
# MODEL_DIR = r"C:\PROJE\zeka\Notebooks"
# # ────────────────────────────────────────────────


# @st.cache_data
# def load_data(path):
#     # Tambahkan sep=';' agar Pandas tahu pemisahnya adalah titik koma
#     df = pd.read_csv(path, sep=';')
    
#     # Sekarang kolom "order_date" pasti terbaca
#     if "order_date" in df.columns:
#         df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    
#     return df

# @st.cache_resource
# def load_model(path):
#     try:
#         with open(path, "rb") as f:
#             return pickle.load(f)
#     except Exception:
#         return None

# #── Load data ──
# if not os.path.exists(CSV_PATH):
#     st.error(f"❌ File tidak ditemukan:\n`{CSV_PATH}`")
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

# def show():
#         with st.sidebar:
#             st.title("🛒 ML Dashboard")
#         st.markdown("---")

#         page = st.radio("📌 Halaman", [
#             "📊 EDA Overview",
#             "📈 Trending Analysis",
#             "⚠️ Risk Prediction",
#             "🎯 Recommendation",
#             "🗺️ Region Analysis",
#         ])

#         st.markdown("---")
#         st.subheader("🔧 Filter Global")

#         # Filter tanggal
#         min_date = df["order_date"].min().date()
#         max_date = df["order_date"].max().date()
#         date_range = st.date_input(
#             "Rentang Tanggal",
#             value=(min_date, max_date),
#             min_value=min_date,
#             max_value=max_date
#         )

#         # Filter region
#         regions = ["Semua"] + sorted(df["region"].unique().tolist())
#         selected_region = st.selectbox("Region", regions)

#         # Filter products
#         products = ["Semua"] + sorted(df["product_name"].unique().tolist())
#         selected_product = st.selectbox("Pilih Produk", products)

#         st.markdown("---")
#         st.caption(f"Total data: {len(df):,} baris")

#     # Terapkan filter
#     filtered_df = df.copy()
#     if len(pd.date_range) == 2:
#         filtered_df = filtered_df[
#             (filtered_df["order_date"].dt.date >= pd.date_range[0]) &
#             (filtered_df["order_date"].dt.date <= pd.date_range[1])
#         ]
#     if selected_region != "Semua":
#         filtered_df = filtered_df[filtered_df["region"] == selected_region]
#     if selected_product != "Semua":
#         filtered_df = filtered_df[filtered_df["product_name"] == selected_product]
#         st.title("📊 Sales Dashboard")

#     col_left, col_right = st.columns(2)

#     # Grafik penjualan harian
#     with col_left:
#         st.subheader("Tren Penjualan Harian")
#         sales_daily = (
#             filtered_df.groupby(filtered_df["order_date"].dt.to_period("M"))["sales"]
#             .sum()
#             .reset_index()
#         )
#         sales_daily["order_date"] = sales_daily["order_date"].astype(str)
#         fig = px.line(
#             sales_daily, x="order_date", y="sales",
#             labels={"order_date": "Bulan", "sales": "Total Penjualan"},
#             color_discrete_sequence=["#636EFA"]
#         )
#         fig.update_layout(margin=dict(l=0, r=0, t=10, b=0))
#         st.plotly_chart(fig, use_container_width=True)

#     # Penjualan per kategori
#     with col_right:
#         st.subheader("Penjualan per produk")
#         cat_sales = (
#             filtered_df.groupby("product_name")["sales"].sum()
#             .sort_values(ascending=False)
#             .reset_index()
#         )
#         fig2 = px.bar(
#             cat_sales, x="product_name", y="sales",
#             color="sales", color_continuous_scale="Blues",
#             labels={"product_name": "Produk", "sales": "Total Penjualan"}
#         )
#         fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0), showlegend=False)
#         st.plotly_chart(fig2, use_container_width=True)

#     # Distribusi profit
#     col3a, col3b = st.columns(2)
#     with col3a:
#         st.subheader("Distribusi Profit")
#         fig3 = px.histogram(
#             filtered_df, x="profit", nbins=40,
#             color_discrete_sequence=["#00CC96"],
#             labels={"profit": "Profit"}
#         )
#         fig3.update_layout(margin=dict(l=0, r=0, t=10, b=0))
#         st.plotly_chart(fig3, use_container_width=True)

#     with col3b:
#         st.subheader("Top 10 Produk")
#         top_products = (
#             filtered_df.groupby("product_name")["sales"].sum()
#             .nlargest(10)
#             .reset_index()
#         )
#         fig4 = px.bar(
#             top_products.sort_values("sales"), x="sales", y="product_name",
#             orientation="h", color_discrete_sequence=["#AB63FA"],
#             labels={"product_name": "Produk", "sales": "Penjualan"}
#         )
#         fig4.update_layout(margin=dict(l=0, r=0, t=10, b=0))
#         st.plotly_chart(fig4, use_container_width=True)

#     # Tabel data mentah
#     with st.expander("📋 Lihat Data Mentah"):
#         st.dataframe(filtered_df.head(100), use_container_width=True)

#     #######################################



   
#     #############################
#     st.markdown("""
#     <style>
#     /* Main background */
#     .stApp {
#         background-color: #101319;
#         color: #e1e2eb;
#     }
    
#     /* Sidebar styling */
#     section[data-testid="stSidebar"] {
#         background-color: #18181b !important;
#         border-right: 1px solid rgba(255, 255, 255, 0.05);
#     }
    
#     /* Glassmorphism Cards */
#     .glass-card {
#         background: rgba(38, 39, 48, 0.4);
#         backdrop-filter: blur(8px);
#         border: 1px solid rgba(255, 255, 255, 0.05);
#         padding: 1.5rem;
#         border-radius: 0.75rem;
#         margin-bottom: 1rem;
#     }
    
#     /* Custom Headers */
#     .main-title {
#         font-size: 2.25rem;
#         font-weight: 700;
#         color: #e1e2eb;
#         margin-bottom: 0.5rem;
#     }
    
#     .sub-text {
#         color: #c6c5d1;
#         margin-bottom: 2rem;
#     }

#     .metric-label {
#         font-size: 0.75rem;
#         text-transform: uppercase;
#         letter-spacing: 0.1em;
#         color: #c6c5d1;
#         margin-bottom: 0.5rem;
#     }

#     .metric-value-primary {
#         font-size: 2rem;
#         font-weight: 700;
#         color: #ffb3ae;
#     }
    
#     .metric-value-normal {
#         font-size: 2rem;
#         font-weight: 700;
#         color: #e1e2eb;
#     }

#     /* Target specific Streamlit elements to match theme */
#     div[data-testid="stMetricValue"] {
#         color: #ffb3ae !important;
#     }
#     </style>
#     """, unsafe_allow_html=True)


#     # 4. Header Section
#     col_title, col_actions = st.columns([2, 1])

#     with col_title:
#         st.markdown('<h1 class="main-title">Market Overview</h1>', unsafe_allow_html=True)
#         st.markdown('<p class="sub-text">Real-time performance metrics across global regions.</p>', unsafe_allow_html=True)

#     with col_actions:
#         st.write("##") # Spacer
#         c1, c2 = st.columns(2)
#         c1.button("📥 Export Report", type="primary", use_container_width=True)
#         c2.button("🔍 Filters", use_container_width=True)

#     # 5. Key Metrics Row (Bento Style)
#     m1, m2, m3 = st.columns(3)

#     with m1:
#         st.markdown("""
#             <div class="glass-card">
#                 <p class="metric-label">Trending Product</p>
#                 <p class="metric-value-primary">UltraLink Pro</p>
#                 <p style="color: #4ade80; font-size: 14px;">↗ +24.8% this week</p>
#             </div>
#         """, unsafe_allow_html=True)

#     with m2:
#         st.markdown("""
#             <div class="glass-card">
#                 <p class="metric-label">Total Analyzed</p>
#                 <p class="metric-value-normal">1.42M</p>
#                 <p style="color: #71717a; font-size: 14px;">📊 99.9% integrity</p>
#             </div>
#         """, unsafe_allow_html=True)

#     with m3:
#         st.markdown("""
#             <div class="glass-card">
#                 <p class="metric-label">Top Region</p>
#                 <p style="color: #3cd7ff; font-size: 2rem; font-weight: 700;">North America</p>
#                 <p style="color: #3cd7ff; font-size: 14px;">🌐 38% revenue share</p>
#             </div>
#         """, unsafe_allow_html=True)

#     # 6. Charts Section
#     chart_col, region_col = st.columns([2, 1])

#     with chart_col:
#         st.markdown('<div class="glass-card">', unsafe_allow_html=True)
#         st.subheader("Product Sales Trends")
        
#         # Generate dummy data for chart
#         chart_data = pd.DataFrame(
#             np.random.randn(20, 2) * [10, 5] + [100, 50],
#             columns=['UltraLink', 'Legacy']
#         )
        
#         st.line_chart(chart_data, color=["#ff4b4b", "#71717a"])
#         st.markdown('</div>', unsafe_allow_html=True)

#     with region_col:
#         st.markdown('<div class="glass-card">', unsafe_allow_html=True)
#         st.subheader("Top Regions")
        
#         regions = {
#             "North America": 85,
#             "Europe": 65,
#             "Asia Pacific": 58,
#             "South America": 25
#         }
        
#         for region, val in regions.items():
#             st.write(f"{region} - ${val*5}k")
#             st.progress(val/100)
        
#         st.write("##")
#         st.button("View detailed report →", key="reg_btn")
#         st.markdown('</div>', unsafe_allow_html=True)

#     # 7. Bottom Status Grid
#     st.markdown("### System Status")
#     s1, s2, s3, s4 = st.columns(4)

#     status_data = [
#         ("Node Status", "98 Active", "🔴"),
#         ("Sync Speed", "42ms avg", "🟢"),
#         ("Storage", "12.4 TB", "🔵"),
#         ("Threat Level", "Low Risk", "🟠")
#     ]

#     for col, (label, val, icon) in zip([s1, s2, s3, s4], status_data):
#         with col:
#             st.markdown(f"""
#                 <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);">
#                     <p style="font-size: 10px; color: #71717a; margin: 0;">{label}</p>
#                     <p style="font-size: 16px; font-weight: bold; margin: 0;">{icon} {val}</p>
#                 </div>
#             """, unsafe_allow_html=True)

#     # Footer/FAB for Mobile (Simulated)
#     st.markdown("""
#         <div style="position: fixed; bottom: 20px; right: 20px; z-index: 99;">
#             <button style="background: #ff5351; color: white; border: none; width: 50px; height: 50px; border-radius: 50%; font-size: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); cursor: pointer;">
#                 +
#             </button>
#         </div>
#     """, unsafe_allow_html=True)
#     #########################################
#     st.write("Isi konten dashboard kamu di sini...")
#         # ... semua kode dashboard kamu
        

#     # SETELAN LEBAR HALAMAN DAN IKON
#     st.set_page_config(
#         page_title="Sales Dashboard",
#         page_icon="📊",
#         layout="wide"
#     )

    
# # #######################################
# # # SIDEBAR NAVIGATION
# # #######################################

# # with st.sidebar:
# #     st.title("MENU")
    
# #     if st.button("📊 DASHBOARD OVERVIEW", use_container_width=True):
# #                 st.session_state.page = "dashboard"
                
# #     if st.button("📈 TRENDING PRODUCTS", use_container_width=True):
# #                 st.session_state.page = "trending"
            
# #     if st.button("💰 PRODUCT RECOMENDATION", use_container_width=True):
# #                 st.session_state.page = "recomendation"
    
# #     if st.button("🌏 REGION ANALYSIS", use_container_width=True):
# #             st.session_state.page = "region"

# #######################################
# # TRENDING PRODUCTS
# #######################################

# # # if 'page' not in st.session_state:
# # #     st.session_state.page = "dashboard"

# # if st.session_state.page == "dashboard":

    
# #     st.title("🚀 Smart E-Commerce Analytics")
# #     st.markdown("""
# #     Welcome, **Bilal**! This AI-powered system helps you detect financial risks 
# #     and forecast future sales based on your transaction data.
# #     """)
    
# #     col1, col2, col3 = st.columns(3)
# #     col1.metric("Model Status", "Active", "Online")
# #     col2.metric("Accuracy", "92.5%", "+2.1%")
# #     col3.metric("System Load", "Normal", "0.2s")
    
# #     st.info("Select a tool from the sidebar to get started.")

# # #######################################
# # # TRENDING PRODUCTS
# # #######################################
# # elif st.session_state.page  == "trending":
# #     st.header("Trending Products")
# # st.write("Analysis of the most popular products in the market.")
# # st.title("� Top Selling Items")
# # st.write("Explore the products with the highest sales volume.")
# # #-------------------------------------------------------------------------------

# # st.info("📊 **Key Data Point:** Jan 18, 2024 - Sales: 19,500")

# # # Tab 2: Trending Products and Product Insights

# # col1, col2 = st.columns([1, 3])
    
# # with col1:
# #         st.subheader("Trending Products")
        
# #         trending_products = {
# #             "Smart Fitness Band": "+72%",
# #             "Wireless Earbuds": "+58%",
# #             "Home Security Camera": "+45%",
# #             "Gaming Laptop": "+39%",
# #             "Kitchen Blender": "+31%"
# #         }
        
# #         for product, growth in trending_products.items():
# #             col_a, col_b = st.columns([3, 1])
# #             with col_a:
# #                 st.write(f"**{product}**")
# #             with col_b:
# #                 st.write(f"`{growth}`")
# #             st.divider()
    
# # with col2:
# #         st.subheader("Product Insights")
# #         st.write("### Smart Fitness Band")
        
# #         # Create gauge chart for product performance
# #         fig_gauge = go.Figure(go.Indicator(
# #             mode="gauge+number+delta",
# #             value=72,
# #             title={'text': "Growth Rate"},
# #             delta={'reference': 50, 'increasing': {'color': "green"}},
# #             gauge={
# #                 'axis': {'range': [None, 100]},
# #                 'bar': {'color': "#FF6B6B"},
# #                 'steps': [
# #                     {'range': [0, 50], 'color': "lightgray"},
# #                     {'range': [50, 75], 'color': "gray"},
# #                     {'range': [75, 100], 'color': "darkgray"}
# #                 ],
# #                 'threshold': {
# #                     'line': {'color': "red", 'width': 4},
# #                     'thickness': 0.75,
# #                     'value': 90
# #                 }
# #             }
# #         ))
        
# #         fig_gauge.update_layout(height=300)
# #         st.plotly_chart(fig_gauge, use_container_width=True)
        
# #         st.write("**Key Features:**")
# #         st.write("• Highest growth among all products")
# #         st.write("• Strong performance in West Coast region")
# #         st.write("• Increased demand in Q1 2024")

# # #-------------------------------------------------------------------------------


# # with st.form("risk_form"):
# #         col1, col2 = st.columns(2)
# #         with col1:
# #             sales = st.number_input("Total Sales ($)", min_value=0.0)
# #             quantity = st.number_input("Quantity Sold", min_value=1)
# #             discount = st.slider("Discount Applied (%)", 0, 100, 10) / 100
        
# #         with col2:
# #             region = st.selectbox("Region", le_region.classes_)
# #             product = st.selectbox("Product Name", le_product.classes_)
        
# #         submit = st.form_submit_button("Analyze Transaction")

# # if submit:
# #         region_n = le_region.transform([region])[0]
# #         product_n = le_product.transform([product])[0]
# #         input_data = np.array([[sales, quantity, discount, region_n, product_n]])
# #         prediction = risk_model.predict(input_data)
        
# #         st.subheader("Analysis Result:")
# #         if prediction[0] == 1:
# #             st.error("⚠️ HIGH RISK DETECTED: This transaction is likely a loss or low-margin.")
# #         else:
# #             st.success("✅ SAFE: This transaction meets profit efficiency standards.")

# # #######################################
# # # product recommendation
# # #######################################

# # elif st.session_state.page  == "recomendation":
# #         st.header("Product Recommendation")
# #         st.write("Personalized product suggestions based on your preferences.")
# # # elif st.session_state.page == "Product Recommendation":
# # st.title("� Product Recommendations")
# # st.write("Discover new products that match your interests.")

# # future_months = np.array([[6], [7], [8]])
# # predictions = forecast_model.predict(future_months)
    
# # forecast_data = pd.DataFrame({
# #         'Month': ['Month 6', 'Month 7', 'Month 8'],
# #         'Predicted Sales': predictions
# #     })

# # fig = px.line(forecast_data, x='Month', y='Predicted Sales', title='Future Sales Projection', markers=True)
# # st.plotly_chart(fig, use_container_width=True)
# # st.write("The AI predicts a steady growth based on current market behavior.")
# # #######################################
# # # region analysis
# # #######################################
# # if st.session_state.page == "region":
# #     st.header("Region Analysis")
# #     st.title("📊 Market Insights & Trends")
# #     st.markdown("Analyze product performance over time and across different regions.")

# # elif st.session_state.page  == "region":
# #     st.header("Region Analysis")
# #     st.title("📊 Market Insights & Trends")
# #     st.markdown("Analyze product performance over time and across different regions.")

# #     # Menggunakan st.form agar ada tombol "Analyze"
# # with st.form("market_analysis_form"):
# #         st.subheader("📅 Select Analysis Period")
# #         col1, col2 = st.columns(2)
        
# #         with col1:
# #             start_date = st.date_input("Start Date", value=pd.to_datetime("2024-01-01"))
# #         with col2:
# #             end_date = st.date_input("End Date", value=pd.to_datetime("2024-12-31"))
        
# #         # Tombol "Play" / Analisis
# #         submit_button = st.form_submit_button(label='🚀 Run Market Analysis')

# #     # Logika Analisis hanya berjalan JIKA tombol diklik
# # if submit_button:
# #         st.divider()
        
# #         # Filtering data
# #         mask = (df['order_date'] >= pd.to_datetime(start_date)) & (df['order_date'] <= pd.to_datetime(end_date))
# #         df_period = df.loc[mask]

# #         if not df_period.empty:
# #             # 1. TRENDING PRODUCTS
# #             st.subheader(f"🔥 Top Products ({start_date} to {end_date})")
# #             trending = df_period.groupby('product_name')['sales'].sum().sort_values(ascending=False).reset_index()
            
# #             fig_trend = px.bar(trending, x='sales', y='product_name', orientation='h',
# #                                color='sales', color_continuous_scale='Magma',
# #                                labels={'sales': 'Total Sales ($)', 'product_name': 'Product'})
# #             st.plotly_chart(fig_trend, use_container_width=True)
            
# #             st.divider()

# #             # 2. REGIONAL LEADERBOARD
# #             st.subheader("📍 Regional Sales Leaderboard")
# #             region_sales = df_period.groupby(['region', 'product_name'])['sales'].sum().reset_index()
# #             top_per_region = region_sales.sort_values(['region', 'sales'], ascending=[True, False]).drop_duplicates('region')

# #             fig_region = px.bar(top_per_region, x='region', y='sales', color='product_name',
# #                                 text='product_name', title="Market Leader per Region")
# #             st.plotly_chart(fig_region, use_container_width=True)
            
            
# #         else:
# #             st.warning("No transactions found for this period. Please try a different date range.")
# #         from numpy.random import default_rng as rng

# #         df = pd.DataFrame(
# #             rng(0).standard_normal((1000, 2)) / [50, 50] + [37.76, -122.4],
# #             columns=["lat", "lon"],
# #         )

# #         st.map(df)
# #         st.success("Analysis Complete! Data successfully filtered.")

# # st.set_page_config(page_title="Smart E-Commerce AI", layout="wide", page_icon="💸")





# # ###################################
# # # Create tabs
# # # tab1, tab2, tab3 = st.tabs(["Dashboard Overview", "Trending Products", "Regional Sales Distribution"])

# # # Tab 1: Dashboard Overview
# # # with tab1:
# #     # Metrics Row
# # col1, col2 = st.columns(2)
    
# # with col1:
# #         st.metric(
# #             label="Total Products Analyzed",
# #             value="8,450",
# #             delta="+12% from last month"
# #         )
    
# # with col2:
# #         st.metric(
# #             label="Top Region",
# #             value="West Coast USA",
# #             delta="+15.2K sales"
# #         )
    
# #     # Product Sales Trends Chart
# # st.subheader("Product Sales Trends")
    
# #     # Sample data for sales trend
# # dates = ['Jan 4', 'Jan 11', 'Jan 18', 'Jan 25']
# # sales = [14500, 16800, 19500, 18200]
    
# # trend_df = pd.DataFrame({
# #         'Date': dates,
# #         'Sales': sales
# #     })
    
# # fig_trend = px.line(trend_df, x='Date', y='Sales', 
# #                         markers=True, 
# #                         title='Sales Trends Over Time',
# #                         labels={'Sales': 'Sales Amount ($)', 'Date': 'Week'})
# # fig_trend.update_traces(line=dict(color='#FF6B6B', width=3))
# # fig_trend.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    
# # st.plotly_chart(fig_trend, use_container_width=True)
    
# #     # Display specific data point
# # st.info("📊 **Key Data Point:** Jan 18, 2024 - Sales: 19,500")

# # # Tab 2: Trending Products and Product Insights
# # # with tab2:
# # col1, col2 = st.columns([1, 1])
    
# # with col1:
# #         st.subheader("Trending Products")
        
# #         trending_products = {
# #             "Smart Fitness Band": "+72%",
# #             "Wireless Earbuds": "+58%",
# #             "Home Security Camera": "+45%",
# #             "Gaming Laptop": "+39%",
# #             "Kitchen Blender": "+31%"
# #         }
        
# #         for product, growth in trending_products.items():
# #             col_a, col_b = st.columns([3, 1])
# #             with col_a:
# #                 st.write(f"**{product}**")
# #             with col_b:
# #                 st.write(f"`{growth}`")
# #             st.divider()
    
# # with col2:
# #         st.subheader("Product Insights")
# #         st.write("### Smart Fitness Band")
        
# #         # Create gauge chart for product performance
# #         fig_gauge = go.Figure(go.Indicator(
# #             mode="gauge+number+delta",
# #             value=72,
# #             title={'text': "Growth Rate"},
# #             delta={'reference': 50, 'increasing': {'color': "green"}},
# #             gauge={
# #                 'axis': {'range': [None, 100]},
# #                 'bar': {'color': "#FF6B6B"},
# #                 'steps': [
# #                     {'range': [0, 50], 'color': "lightgray"},
# #                     {'range': [50, 75], 'color': "gray"},
# #                     {'range': [75, 100], 'color': "darkgray"}
# #                 ],
# #                 'threshold': {
# #                     'line': {'color': "red", 'width': 4},
# #                     'thickness': 0.75,
# #                     'value': 90
# #                 }
# #             }
# #         ))
        
# #         fig_gauge.update_layout(height=300)
# #         st.plotly_chart(fig_gauge, use_container_width=True)
        
# #         st.write("**Key Features:**")
# #         st.write("• Highest growth among all products")
# #         st.write("• Strong performance in West Coast region")
# #         st.write("• Increased demand in Q1 2024")

# # # Tab 3: Regional Sales Distribution
# # # with tab3:
# # st.subheader("Sales by Region")
    
# #     # Regional sales data
# # regions = ['West Coast', 'Northeast', 'Midwest', 'Southeast', 'Southwest']
# # sales_values = [54.2, 38.7, 32.1, 28.5, 21.3]
    
# #     # Create bar chart
# # fig_bar = px.bar(
# #         x=regions, 
# #         y=sales_values,
# #         title="Sales Distribution by Region (in Thousands)",
# #         labels={'x': 'Region', 'y': 'Sales (K $)'},
# #         color=sales_values,
# #         color_continuous_scale='Viridis'
# #     )
    
# # fig_bar.update_layout(showlegend=False)
# # st.plotly_chart(fig_bar, use_container_width=True)
    
# #     # Map visualization (simulated)
# # st.subheader("Geographic Sales Distribution")
    
# #     # Create a simple map-like visualization using plotly scatter
# #     # Coordinates for US regions (approximate)
# # region_coords = {
# #         'West Coast': {'lat': 37.7749, 'lon': -122.4194, 'sales': 54.2},
# #         'Northeast': {'lat': 40.7128, 'lon': -74.0060, 'sales': 38.7},
# #         'Midwest': {'lat': 41.8781, 'lon': -87.6298, 'sales': 32.1},
# #         'Southeast': {'lat': 33.7490, 'lon': -84.3880, 'sales': 28.5},
# #         'Southwest': {'lat': 32.7157, 'lon': -97.0839, 'sales': 21.3}
# #     }
    
# # map_df = pd.DataFrame([
# #         {'Region': region, 'Lat': data['lat'], 'Lon': data['lon'], 'Sales': data['sales']}
# #         for region, data in region_coords.items()
# #     ])
    
# # fig_map = px.scatter_geo(
# #         map_df,
# #         lat='Lat',
# #         lon='Lon',
# #         size='Sales',
# #         hover_name='Region',
# #         text='Region',
# #         size_max=50,
# #         title="Regional Sales Distribution Map",
# #         projection="albers usa"
# #     )
    
# # fig_map.update_layout(
# #         geo=dict(
# #             scope='usa',
# #             projection_scale=0.8,
# #             center={'lat': 39.8283, 'lon': -98.5795}
# #         )
# #     )
    
# # st.plotly_chart(fig_map, use_container_width=True)
    
# #     # Top Regions Table
# # st.subheader("Top Regions Performance")
    
# # region_data = {
# #         'Rank': [1, 2, 3, 4, 5],
# #         'Region': regions,
# #         'Sales (K $)': sales_values,
# #         'Market Share': [f"{s/sum(sales_values)*100:.1f}%" for s in sales_values]
# #     }
    
# # region_df = pd.DataFrame(region_data)
# # st.dataframe(region_df, use_container_width=True, hide_index=True)
    
# #     # Additional insights
# # with st.expander("View Regional Insights"):
# #         st.write("""
# #         **Key Observations:**
# #         - **West Coast** leads with 54.2K in sales, representing 30.7% of total sales
# #         - **Northeast** follows closely with 38.7K (21.9% market share)
# #         - **Southwest** shows potential for growth with current sales of 21.3K
# #         - Overall regional distribution shows a strong coastal bias
# #         """)

# # # Sidebar with additional information
# # st.set_page_config(page_title="Dashboard Navigation", layout="wide", page_icon="")





# # #----------------------------------------------------------------------------------------------------