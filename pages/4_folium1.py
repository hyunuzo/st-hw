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
import datetime



# 데이터 전처리
path_csv = 'img/국토교통부_전국 버스정류장 위치정보1_20231016.csv'
path_geo = 'img/s.geojson'
bus_stop = pd.read_csv(path_csv)
geometry = [Point(xy) for xy in zip(bus_stop['경도'],bus_stop['위도'])]
gdf_bs = gpd.GeoDataFrame(bus_stop,geometry=geometry,crs='epsg:4326')
gdf = gpd.read_file(path_geo)
geo_str = json.load(open(path_geo,encoding='utf-8'))





st.set_page_config(layout="wide")

# 영역 그리는 지도
m = folium.Map(location=[35.162943, 129.053097], zoom_start=11)
Draw(export=True).add_to(m)
# 지도 기능추가 (전체화면 기능)
folium.plugins.Fullscreen(
    position="topright",
    title="전체화면",
    title_cancel="나가기",
    force_separate_button=True,
).add_to(m)

# st_map = folium_static(m, width = 1100, height=500)
df_bs_poly = None


###### 화면 구성

t1,t2 = st.columns([0.9,0.1])
with t1:
    st.header("타이틀 내용 입력")
    with st.expander("📝  사용법 보기"):
                st.write("1. 지도 왼편 다각형(⬟) or 사각형(■) 선택")
                st.write("2. 원하는 영역 그리기")
                st.write("3. 지도 오른편 :blue-background[Export] 눌러 파일 다운받기")
                st.write("4. 지도 아래 :blue-background[Browse files] 눌러 다운받은 파일(*.geojson) 업로드")
                st.write("5. :blue-background[🔎 조회하기] 클릭")
                st.write("📢 영역을 다시 그리려면 :blue-background[🔄영역 재설정] 클릭 후 다시 진행")
    with st.container(height= 550):
        a1, a2 = st.columns([0.9,0.1])
            
    with st.container(height= 200,border=None):
        b1, b2 = st.columns(2)
        with b1:
            bt_search = st.button(label="🔎  :green[조  회  하  기]",use_container_width=True)  
            bt_reset = st.button("🔄  :blue[영역 재설정] ",use_container_width=True)
        with b2:
            uploaded_file = st.file_uploader("다운 받은 파일(*.geojson)을 업로드해주세요.",type='geojson')
           

    if bt_reset:
        with a1:
            output = folium_static(m,width=1100,height=500)
    
    if bt_search:
        if uploaded_file is not None:
            gdf = gpd.read_file(uploaded_file)
            location = [gdf['geometry'].centroid.y.mean(),gdf['geometry'].centroid.x.mean()]  # 폴리곤 중앙 좌표값    
            bs_poly = gpd.sjoin(gdf_bs,gdf,how='inner')
            df_bs_poly = pd.DataFrame(bs_poly.drop(columns='geometry'))
            m1 = folium.Map(location=location, zoom_start=15)
            folium.plugins.Fullscreen(position="topright",title="전체화면",title_cancel="나가기",force_separate_button=True).add_to(m1)
            folium.GeoJson(data=gdf['geometry'],).add_to(m1)
            if len(bs_poly) != 0: # 폴리곤 내 포함되는 값이 있는 경우만 마커 추가
                for idx, row in bs_poly.iterrows():
                    popup = folium.Popup("<b>정류장명 : </b>" + f"{row['정류장명']}",max_width=300) # 마커 팝업에 표시할 정보 설정
                    tooltip = f"정류장번호: {row['정류장번호']}"
                    folium.Circle(location=[row.geometry.y, row.geometry.x],radius=10,fill=True,fill_opacity=0.8,popup=popup,tooltip=tooltip).add_to(m1)
            with a1:
                    st_m = folium_static(m1,width=1100,height=500)
            with a2:
                st.metric(label="수량",value=len(df_bs_poly))
                st.metric(label="Metric_sample1",value= 80,delta="-3.5%")
                st.metric(label="Metric_sample2",value= 76,delta="3.5%")
                st.metric(label="Metric_sample3",value= 76,delta= str(len(df_bs_poly))+" 점")
            st.write("[RAW DATA]")
            st.dataframe(df_bs_poly)                    
        else:
            with a1:
                st.subheader("⛔   :red[파일을 업로드한 후 조회 해주세요.]   ⛔")
                output = folium_static(m,width=1100, height=500)
    else:
        with a1:
            output = folium_static(m,width=1100, height=500)
with t2:
    st.empty()



