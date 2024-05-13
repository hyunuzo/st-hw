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

sido = df['시도'].unique().append('전국')
gungu = df['시군구'].unique()
a = df[df['시도']== '부산']['시군구'].unique()

def sido_gungu(data,select):
    filter_gungu = data[data['시도']== select]['시군구'].unique()
    return filter_gungu


select_sido = st.selectbox('시도 선택',sido)
select_gungu = st.selectbox('시군구 선택',sido_gungu(df,select_sido))



# df1 = df[df['시도']==select_sido]




st.write(select_sido)
st.write(select_gungu)
st.write(df)