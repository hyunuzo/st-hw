import requests
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
from datetime import datetime


### API 호출
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

### 데이터 가공
today = datetime.now().date().strftime("%Y-%m-%d")



df1 = df[df['fstvlstartdate'] >= '2024-04-18']

# 축제 수 카운트
count =len(df1)

# 컬럼명 한글화
output = df1.rename(columns={'fstvlnm' : '축제명', 
'opar' : '개최장소', 
'fstvlstartdate' : '축제시작일자', 
'fstvlenddate' : '축제종료일자', 
'fstvlco' : '축제내용', 
'mnnstnm' : '주관기관명', 
'auspcinsttnm' : '주최기관명', 
'suprtinsttnm' : '후원기관명', 
'phonenumber' : '전화번호', 
'homepageurl' : '홈페이지주소', 
'relateinfo' : '관련정보', 
'rdnmadr' : '소재지도로명주소', 
'lnmadr' : '소재지지번주소', 
'latitude' : '위도', 
'longitude' : '경도', 
'referencedate' : '데이터기준일자', 
'instt_code' : '제공기관코드', 
'instt_nm' : '제공기관기관명'})


#### 화면 출력

st.set_page_config(layout="wide")

st.subheader("전국 문화축제 리스트")
st.metric(label="축제 수", value= count )
st.data_editor(output,column_config={"homepageurl" : st.column_config.LinkColumn()})
