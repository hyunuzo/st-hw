import requests
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup

svkey = "JBgfMOzc2H1AraeZJkFTdGrDkfJJ4mOEyAU1/iWxTbQJI043Vgf0m0WA6vxUJXVzrzsSXFmPuDr3/7pmbjR/1w=="

url = 'http://api.data.go.kr/openapi/tn_pubr_public_cltur_fstvl_api'
params = {'serviceKey' : svkey, 'type' : 'xml', 'numOfRows' : '99999'}

response = requests.get(url, params=params)

content = response.content


xml_obj = BeautifulSoup(content,'lxml')
rows = xml_obj.findAll('item')

# 각 행의 컬럼, 이름, 값을 가지는 리스트 만들기
row_list = [] # 행값
name_list = [] # 열이름값
value_list = [] #데이터값

# xml 안의 데이터 수집
for i in range(0, len(rows)):
    columns = rows[i].find_all()
    #첫째 행 데이터 수집
    for j in range(0,len(columns)):
        if i ==0:
            # 컬럼 이름 값 저장
            name_list.append(columns[j].name)
        # 컬럼의 각 데이터 값 저장
        value_list.append(columns[j].text)
    # 각 행의 value값 전체 저장
    row_list.append(value_list)
    # 데이터 리스트 값 초기화
    value_list=[]

df = pd.DataFrame(row_list, columns=name_list)

df1 = df[df['fstvlstartdate'] >= '2024-04-18']


st.set_page_config(layout="wide")


st.data_editor(df1,column_config={"homepageurl" : st.column_config.LinkColumn()})
