import pandas as pd
import folium
import streamlit as st
from streamlit_folium import folium_static
from folium.plugins import Draw
from io import StringIO
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.geometry import Point
import json


path_csv = 'img/국토교통부_전국 버스정류장 위치정보1_20231016.csv'
path_geo = 'img/s.geojson'
bus_stop = pd.read_csv(path_csv)
geometry = [Point(xy) for xy in zip(bus_stop['경도'],bus_stop['위도'])]
gdf_bs = gpd.GeoDataFrame(bus_stop,geometry=geometry,crs='epsg:4326')
gdf = gpd.read_file(path_geo)
geo_str = json.load(open(path_geo,encoding='utf-8'))





st.set_page_config(layout="wide")




m = folium.Map(location=[35.162943, 129.053097], zoom_start=11)
Draw(export=True).add_to(m)


m1 = folium.Map(location=[35.176934,129.178065], zoom_start=6)

# st_map = folium_static(m, width = 1100, height=500)

df_bs_poly = None


with st.sidebar.form(key='search_form'):
    submit_button = st.form_submit_button(label='조회')
    uploaded_file = st.file_uploader("폴리곤파일(.geojson)을 업로드해주세요.")
    if uploaded_file is not None:
        gdf = gpd.read_file(uploaded_file)
        if submit_button:
            bs_poly = gpd.sjoin(gdf_bs,gdf,how='inner')
            df_bs_poly = pd.DataFrame(bs_poly.drop(columns='geometry'))
            m1 = folium.Map(location=[bs_poly.geometry.y.mean(),bs_poly.geometry.x.mean()], zoom_start=14)
            folium.GeoJson(data=gdf['geometry']).add_to(m1)
            # folium.GeoJson(data=gdf['geometry'],style_function=lambda feature: {'fillColor': 'yellow','color': 'yellow'}).add_to(m1)
            for idx, row in bs_poly.iterrows():
                popup = f"Name: {row['정류장명']}"  # 마커 팝업에 표시할 정보 설정
                folium.Circle(location=[row.geometry.y, row.geometry.x],radius=10,fill=True,fill_opacity=0.8,popup=popup).add_to(m1)





output = folium_static(m, width=1000, height=500,returned_objects=["last_active_drawing"])
st_m = folium_static(m1, width=1000, height=500)
if df_bs_poly is not None:
    st.write(df_bs_poly)
else:
    st.write("조회시 테이블이 표시됩니다.")