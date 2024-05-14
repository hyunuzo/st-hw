import pandas as pd
import folium
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import st_folium
from io import StringIO
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.geometry import Point
from streamlit_folium import folium_static


st.set_page_config(layout="wide")

def _max_width_(prcnt_width:int = 75):
    max_width_str = f"max-width: {prcnt_width}%;"
    st.markdown(f""" 
                <style> 
                .reportview-container .main .block-container{{{max_width_str}}}
                </style>    
                """, 
                unsafe_allow_html=True,
    )

_max_width_(80)

m = folium.Map(location=[35.162943, 129.053097], zoom_start=11)
Draw(export=True).add_to(m)


# c1, c2 = st.columns([7,3])
# with c1:
#     output = folium_static(m, width=1000, height=500)

# with c2:
#     st.write(st_folium(m, width=1000, height=500))
st.write(st_folium(m, width=1000, height=500,returned_objects="last_active_drawing"))
