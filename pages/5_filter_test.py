import pandas as pd
import folium
import streamlit as st
from streamlit_folium import folium_static
from folium.plugins import Draw
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.geometry import Point
import json
import datetime

path_csv = 'img/도로교통공단_일자별 시군구별 교통사고 건수_20221231.csv'
df = pd.read_csv(path_csv)

sido = df['시도'].unique()
gungu = df['시군구'].unique()

def filter_select(select):
    df[['시도']== select]



select_sido = st.selectbox('시도 선택',sido)
select_gungu = st.selectbox('시군구 선택',gungu)

a = df[['시도']== '부산'].unique()

st.write(a)

st.write(df)