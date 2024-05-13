import pandas as pd
import numpy as np
import folium
import streamlit as st
from streamlit_folium import folium_static
from folium.plugins import Draw
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.geometry import Point

import datetime

path_csv = 'img/도로교통공단_일자별 시군구별 교통사고 건수_20221231.csv'
df = pd.read_csv(path_csv)

sido = df['시도'].unique()
gungu = df['시군구'].unique()

def sido_gungu(data,select):
    filter_gungu = data[data['시도']== select]['시군구'].unique()
    return filter_gungu


select_sido = st.selectbox('시도 선택',sido,index=None)
select_gungu = st.selectbox('시군구 선택',sido_gungu(df,select_sido),index=None)

if select_sido is not None:
    if select_gungu is not None:
        filter_df = df[(df['시도']== select_sido)&(df['시군구']== select_gungu)]
    else:
        filter_df = df[df['시도']== select_sido]
else:
    if select_gungu is not None:
        filter_df = df[df['시군구']== select_gungu]
    else:
        filter_df = df


st.write(filter_df)