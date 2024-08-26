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



import requests

apikey = 'zxuuVVK8h9z9fvHU9kwZ5w'
url = 'https://api.odsay.com/v1/api/loadLane'
params ={'apiKey' : apikey,'lang':'1','mapObject':'0:0@2:2:-1:-1'}
	
response = requests.get(url, params=params)


st.write(response.content)
