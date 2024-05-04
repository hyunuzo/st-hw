import folium
import streamlit as st
from folium.plugins import Draw

from streamlit_folium import st_folium

m = folium.Map(location=[35.162943, 129.053097], zoom_start=5)
Draw(export=True).add_to(m)

c1, c2 = st.columns([7,3])
with c1:
    output = st_folium(m, width=1000, height=500)

with c2:
    st.write(output)