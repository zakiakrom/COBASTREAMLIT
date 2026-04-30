import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(__file__))

import YZdashboard
import YZregion
import YZrekom
import YZtrending
import YZrisk

# with st.sidebar:
#     # st.title("📊 Analytics Pro")
#     # st.markdown("---")
    
#     page = st.radio(
#         "Menu",
#         ["🏠 Dashboard", "🌍 Region Analysis", "⚠️ Risk Prediction" , "💡 Rekomendasi", "🔥 Trending"],
#         label_visibility="collapsed"
#     )

# if page == "🏠 Dashboard":
#     YZdashboard.show()
# elif page == "🌍 Region Analysis":
#     YZregion.show()
# elif page == "💡 Rekomendasi":
#     YZrekom.show()
# elif page == "🔥 Trending":
#     YZtrending.show()
# elif page == "⚠️ Risk Prediction":
#     YZrisk.show()

with st.sidebar: 
    if st.button("🏠 Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"
    if st.button("🌍 Region Analysis", use_container_width=True):
        st.session_state.page = "Region Analysis"
    if st.button("💡 Rekomendasi", use_container_width=True):
        st.session_state.page = "Rekomendasi"
    if st.button("🔥 Trending", use_container_width=True):
        st.session_state.page = "Trending"

# Set default halaman pertama kali
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# Routing
if st.session_state.page == "Dashboard":
    YZdashboard.show()
elif st.session_state.page == "Region Analysis":
    YZregion.show()
elif st.session_state.page == "Rekomendasi":
    YZrekom.show()
elif st.session_state.page == "Trending":
    YZtrending.show()