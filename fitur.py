import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import csv

datafile = 'C:\PROJE\yapayzeka\Data\Processed\cleaned_ecommerce_data.csv'

def read_data():
    def parse_lat_lion(point):
        return point.split ("(")[-1].split(")")[0].split()
    
    data = []
    with open(datafile, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        print("reading....")
        for row in reader:
            longitude, latitude = parse_lat_lion(row['C:\PROJE\yapayzeka\Data\Processed\cleaned_ecommerce_data.csv'])
            data.append({
                'latitude': float(latitude),
                'longitude': float(longitude)
            })

    return data


data = read_data()


st.header("E-commerce Data Visualization", "indian-map")
st.map(data, zoom=10)
