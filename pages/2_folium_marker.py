import pandas as pd
import folium
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import st_folium
from io import StringIO
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.geometry import Point
import json
from streamlit_folium import folium_static
from folium.plugins import MeasureControl


path_csv = 'img/국토교통부_전국 버스정류장 위치정보1_20231016.csv'
path_geo = 'img/s.geojson'
bus_stop = pd.read_csv(path_csv)
geometry = [Point(xy) for xy in zip(bus_stop['경도'],bus_stop['위도'])]
gdf_bs = gpd.GeoDataFrame(bus_stop,geometry=geometry,crs='epsg:4326')
gdf = gpd.read_file(path_geo)
geo_str = json.load(open(path_geo,encoding='utf-8'))

st.set_page_config(layout="wide")



# st.write(uploaded_file.getvalue())
# st.write(StringIO(uploaded_file.getvalue().decode("utf-8")))

# if uploaded_file is not None:
#     gdf = gpd.read_file(uploaded_file)
#     geo_str = json.load(open(uploaded_file,encoding='utf-8'))
# else:
#     st.write("폴리곤 파일을 업로드해주세요.")

# gdf = gpd.read_file(path_geo)
# geo_str = json.load(open(path_geo,encoding='utf-8'))
# m = folium.Map(location=[35.176934,129.178065], zoom_start=6)
# folium.Choropleth(    geo_data = geo_str).add_to(m)

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
            m1 = folium.Map(location=[bs_poly.geometry.y.mean(),bs_poly.geometry.x.mean()], zoom_start=11)
            folium.GeoJson(data=gdf['geometry']).add_to(m1)
            m1.add_child(MeasureControl())
            # folium.GeoJson(data=gdf['geometry'],style_function=lambda feature: {'fillColor': 'yellow','color': 'yellow'}).add_to(m1)
            for idx, row in bs_poly.iterrows():
                popup = f"Name: {row['정류장명']}"  # 마커 팝업에 표시할 정보 설정
                folium.Circle(location=[row.geometry.y, row.geometry.x],radius=10,fill=True,fill_opacity=0.8,popup=popup).add_to(m1)






st_m = folium_static(m1, width=1000, height=500)
if df_bs_poly is not None:
    st.write(df_bs_poly)
else:
    st.write("조회시 테이블이 표시됩니다.")


#     # To read file as bytes:
#     bytes_data = uploaded_file.getvalue()
#     st.write(bytes_data)

#     # To convert to a string based IO:
#     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
#     st.write(stringio)

#     # To read file as string:
#     string_data = stringio.read()
#     st.write(string_data)

#     # Can be used wherever a "file-like" object is accepted:
#     dataframe = pd.read_csv(uploaded_file)
#     st.write(dataframe)

