import pandas as pd
import folium
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import st_folium
from io import StringIO

path_csv = 'img/국토교통부_전국 버스정류장 위치정보1_20231016.csv'
bus_stop = pd.read_csv(path_csv,encoding = 'ANSI')

st.set_page_config(layout="wide")

m = folium.Map(location=[35.162943, 129.053097], zoom_start=11)
Draw(export=True).add_to(m)

uploaded_file = st.file_uploader("Choose a file")
st.write(uploaded_file.getvalue())
st.write(StringIO(uploaded_file.getvalue().decode("utf-8")))
st.write(bus_stop.head(10))

# if uploaded_file is not None:
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



c1, c2 = st.columns([7,3])
with c1:
    output = st_folium(m, width=1000, height=500)

with c2:
    st.write(output)