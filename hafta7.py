import duckdb 
import pandas as pd
from plotly import data
import streamlit as st  
import plotly.express as px  
import plotly.graph_objects as go
import random

st.title("🚀 Smart E-Commerce Analytics")
st.markdown("_percobaan sebelum vize_")

#######################################
# DATA LOADING
#######################################

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    data = pd.read_excel(path)
    return data


df = load_data('C:\\PROJE\\yapayzeka - Copy\\Data\\Processed\\version1.xlsx')

with st.expander("Data Summary"):
    st.dataframe(df)

#######################################
# DATA VISUALIZATION
#######################################

def plot_metric(label, value, prefix="", suffix="", show_graph=False, color_graph=""):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis": {"visible": False}},
            number={
                "prefix": prefix,
                "suffix": suffix,
                "font.size": 28,
            },
            title={
                "text": label,
                "font": {"size": 24},
            },
        )
    )

    if show_graph:
        fig.add_trace(
            go.Scatter(
                y=random.sample(range(0, 101), 30),
                hoverinfo="skip",
                fill="tozeroy",
                fillcolor=color_graph,
                line={
                    "color": color_graph,
                },
            )
        )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        margin=dict(t=30, b=0),
        showlegend=False,
        plot_bgcolor="white",
        height=100,
    )

    st.plotly_chart(fig, use_container_width=True)
















# def plot_top_left(df):
#     sales_by_region = duckdb.sql(
#         f"""
#         SELECT region, SUM(sales) AS total_sales
#         FROM df
#         GROUP BY region
#         ORDER BY total_sales DESC
#         """

#     ).df()

#     fig =px.line(
#             sales_by_region,
#             x='region', 
#             y='total_sales', 
#             title='Total Sales by Region')
#     st.plotly_chart(fig, use_container_width=True)


#     plot_top_left(df)

   
    
    # def plot_bottom_left(df):
    #     result = duckdb.sql(
    #         f"""
    #         WITH sales_data AS (
    #             SELECT order_date, SUM(sales) AS total_sales
    #             FROM df
    #             GROUP BY order_date
    #             ORDER BY order_date
    #         )
    #         SELECT * FROM sales_data
    #     """
    #     ).df()
        
    #     return result

    # result = plot_bottom_left(df)
    # st.write(result)
