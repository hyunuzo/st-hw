import requests
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
from datetime import datetime
from streamlit_folium import folium_static

import folium
from folium import plugins

### 오픈API(공공데이터포털)  #  url1 . 전국문화축제표준데이터 url2 . 전국공연행사정보표준데이터
svkey = "JBgfMOzc2H1AraeZJkFTdGrDkfJJ4mOEyAU1/iWxTbQJI043Vgf0m0WA6vxUJXVzrzsSXFmPuDr3/7pmbjR/1w=="
url1 = 'http://api.data.go.kr/openapi/tn_pubr_public_cltur_fstvl_api'
url2 = 'http://api.data.go.kr/openapi/tn_pubr_public_pblprfr_event_info_api'


st.set_page_config(layout="wide")

@st.cache_data
def api_data(url):    
    response = requests.get(url, params={'serviceKey' : svkey, 'type' : 'xml', 'numOfRows' : '99999'})
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
    data = pd.DataFrame(row_list, columns=name_list)
    return data

def marker(dataframe,zoom_lv):
            lat_mean = dataframe.loc[dataframe['위도'] !=0,'위도'].mean()
            lon_mean = dataframe.loc[dataframe['경도'] !=0,'경도'].mean()
            fstvlnm = dataframe['축제명']
            opar = dataframe['개최장소']
            fstvlstartdate = dataframe['축제시작일자']
            fstvlenddate = dataframe['축제종료일자']
            lat = dataframe['위도']
            lon = dataframe['경도']
            location = [lat, lon]
            m = folium.Map(location= [lat_mean,lon_mean], zoom_start= zoom_lv)
            folium.TileLayer('cartodbpositron').add_to(m)
            for i in dataframe.index:
                folium.Marker(
                    [lat[i],lon[i]],
                    popup= folium.Popup("<b>축제명 : </b>" + str(fstvlnm[i]) + "<br><b>개최장소 : </b>" + str(opar[i]) + "<br><b>축제기간 : </b>" + str(fstvlstartdate[i]) + " ~ " + str(fstvlenddate[i]),parse_html=False,max_width= 300),
                    tooltip= fstvlnm[i],
                    icon= folium.Icon(
                        # color='Blue',
                        icon= 'hashtag',
                        prefix='fa'
                        )
                            ).add_to(m)
            return m

# 데이터 불러오기 
df_fest_raw = api_data(url1)
# df_event_raw = api_data(url2)

# 필요한 컬럼만
df = df_fest_raw[['fstvlNm', 'opar', 'fstvlStartDate', 'fstvlEndDate', 'fstvlCo', 'mnnstNm', 'auspcInsttNm', 'suprtInsttNm', 'phoneNumber', 'homepageUrl', 'rdnmadr', 'lnmadr', 'latitude', 'longitude']]
# df_event = df_event_raw[['eventNm', 'opar', 'eventStartDate', 'eventEndDate', 'eventCo', 'mnnstNm', 'auspcInsttNm', 'suprtInsttNm', 'phoneNumber', 'homepageUrl', 'rdnmadr', 'lnmadr', 'latitude', 'longitude']]

# df = pd.merge([df_fest, df_event])


### 데이터 가공
df.loc[df['lnmadr']=='','lnmadr'] = df['rdnmadr'] # 도로명/지번 주소 중 1가지만 있는 경우가 있어 지번기준 공란일시 도로명주소로 채움
df['latitude'] = df['latitude'].replace('',0).astype(float)
df['longitude'] = df['longitude'].replace('',0).astype(float)
lat_mean = df.loc[df['latitude'] !=0,'latitude'].mean()
lon_mean = df.loc[df['longitude'] !=0,'longitude'].mean()



# df1 = df[['fstvlnm','opar','lnmadr','fstvlstartdate', 'fstvlenddate', 'fstvlCo', 'mnstnm', 'auspcinsttnm','suprtinsttnm', 'phonenumber', 'homepageurl', 'relateinfo', 'latitude', 'longitude', 'instt_nm', 'referencedate']]

# 컬럼명 한글화
df1 = df.rename(columns={'fstvlnm' : '축제명', 
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
'lnmadr' : '소재지주소', 
'latitude' : '위도', 
'longitude' : '경도', 
'referencedate' : '데이터기준일자', 
'instt_nm' : '제공기관기관명'})

#df1 = df_name[['축제명','개최장소','소재지주소','축제시작일자','축제종료일자','축제내용','주관기관명','주최기관명','전화번호','홈페이지주소','관련정보']]

# 축제 수 카운트
count =len(df)




#### 화면 출력

st.sidebar.subheader("🔍축제 검색")
with st.sidebar.form(key='search_form'):
    place = st.selectbox("지역",['서울특별시','부산광역시','대구광역시','인천광역시','광주광역시','대전광역시','울산광역시','세종특별자치시','경기도','강원도','충청북도','충청남도','전라북도','전라남도','경상북도','경상남도','제주특별자치도'],index=None)
    fstvlsttd = st.date_input("축제 시작일자",value=None)
    submit_button = st.form_submit_button(label='검색')
    if submit_button:
        if place is not None:
            if fstvlsttd is not None:
                filter_df = df1[(df1['소재지주소'].str.contains(place))&(df1['축제시작일자'] >= str(fstvlsttd))]
                zoom_lv = 9
                mk = marker(filter_df,zoom_lv)
            else:
                filter_df = df1[df1['소재지주소'].str.contains(place)]
                zoom_lv = 9
                mk = marker(filter_df,zoom_lv)
        else:
            if fstvlsttd is not None:
                filter_df = df1[df1['축제시작일자'] >= str(fstvlsttd)]
                zoom_lv = 9
                mk = marker(filter_df,zoom_lv)
            else:
                filter_df = df1
                zoom_lv = 9
                mk = marker(filter_df,zoom_lv)
    else:
        filter_df = df1
        zoom_lv = 7
        mk = marker(filter_df,zoom_lv)


st.subheader("🎈🎪전국 문화축제 리스트🎡🎠")

col1, col2, col3 = st.columns([1,9,1])
with col1:
    st.metric(label="수집된 축제 수", value= count)
with col2:
    st.empty()
with col3:
    st.metric(label="검색된 축제 수", value= len(filter_df))
st.empty()
with st.spinner():
    st_map = folium_static(mk, width = 1100, height=500)
    st.data_editor(filter_df.sort_values(by=['축제시작일자','축제종료일자']),height=1500,column_order=("축제명","개최장소","소재지주소","축제시작일자","축제종료일자","축제내용","주관기관명","주최기관명","전화번호","홈페이지주소","관련정보"),column_config={"홈페이지주소" : st.column_config.LinkColumn()})

