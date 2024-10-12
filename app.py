from dash import Dash, html, dcc, Input, Output, State
import dash
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import dash_leaflet as dl
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from pages.data import df1,df1_bad,df2_bad

# Initialize the Dash app
app = Dash(__name__,suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.BOOTSTRAP])

# 팀별 대상(전일)
df1_db = df1.loc[df1['duh_op_team_org_id_nm'] == '동부산품질개선팀']
df1_sb = df1.loc[df1['duh_op_team_org_id_nm'] == '서부산품질개선팀']
df1_gh = df1.loc[df1['duh_op_team_org_id_nm'] == '김해품질개선팀']
df1_us = df1.loc[df1['duh_op_team_org_id_nm'] == '울산품질개선팀']
df1_jj = df1.loc[df1['duh_op_team_org_id_nm'] == '진주품질개선팀']
df1_cw = df1.loc[df1['duh_op_team_org_id_nm'] == '창원품질개선팀']
df1_ty = df1.loc[df1['duh_op_team_org_id_nm'] == '통영품질개선팀']

# 팀별 불량대상(전일)
df1_bad_db = df1_bad.loc[df1_bad['duh_op_team_org_id_nm'] == '동부산품질개선팀']
df1_bad_sb = df1_bad.loc[df1_bad['duh_op_team_org_id_nm'] == '서부산품질개선팀']
df1_bad_gh = df1_bad.loc[df1_bad['duh_op_team_org_id_nm'] == '김해품질개선팀']
df1_bad_us = df1_bad.loc[df1_bad['duh_op_team_org_id_nm'] == '울산품질개선팀']
df1_bad_jj = df1_bad.loc[df1_bad['duh_op_team_org_id_nm'] == '진주품질개선팀']
df1_bad_cw = df1_bad.loc[df1_bad['duh_op_team_org_id_nm'] == '창원품질개선팀']
df1_bad_ty = df1_bad.loc[df1_bad['duh_op_team_org_id_nm'] == '통영품질개선팀']

# 팀별 불량대상(2일전)  / 비교용
df2_bad_db = df2_bad.loc[df2_bad['duh_op_team_org_id_nm'] == '동부산품질개선팀']
df2_bad_sb = df2_bad.loc[df2_bad['duh_op_team_org_id_nm'] == '서부산품질개선팀']
df2_bad_gh = df2_bad.loc[df2_bad['duh_op_team_org_id_nm'] == '김해품질개선팀']
df2_bad_us = df2_bad.loc[df2_bad['duh_op_team_org_id_nm'] == '울산품질개선팀']
df2_bad_jj = df2_bad.loc[df2_bad['duh_op_team_org_id_nm'] == '진주품질개선팀']
df2_bad_cw = df2_bad.loc[df2_bad['duh_op_team_org_id_nm'] == '창원품질개선팀']
df2_bad_ty = df2_bad.loc[df2_bad['duh_op_team_org_id_nm'] == '통영품질개선팀']


map = dl.Map([dl.TileLayer(
                url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
                attribution="&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors &copy; <a href=\"https://carto.com/attributions\">CARTO</a>"
                ),
            ]
            , center=[35.1746,129.0528], zoom=11, style={'width': '30vw','height': '60vh','margin':'10px'})


df1_bad_tb = df1_bad[['dt','duh_op_team_org_id_nm','dul_eqp_nm','duh_nm','NRCellDU','Noti3','txbs1','temp1','txdbm1','rxdbm1','txbs2','temp2','txdbm2','rxdbm2','vendor1','vendorprod1','serial1','vendor2','vendorprod2','serial2','duh_erp_bld_addr']]

tb1 = dag.AgGrid(
        id='table1',
        rowData=df1_bad_tb.to_dict('records'),
        columnDefs=[{"field": i} for i in df1_bad_tb.columns],
        dashGridOptions={
            'rowSelection': 'single',  # Allow single row selection
            'enableCellTextSelection': True,
            'onGridReady': {'autoSizeColumns': True}
        },
        className="ag-theme-balham",
    )

def team_indicator1(title,current_value):
    fig = go.Figure(go.Indicator(
            mode="number",  # 숫자와 델타 값을 함께 표시
            value=current_value,  # 현재 값
            number={
                'valueformat': 'f',  # 숫자 포맷
                'font': {'size': 25}  # 숫자 폰트 크기
            },
            title={'text': title, 'font':{'size':15}}  # 인디케이터 제목
            ))
    fig.update_layout(height=150)
    return fig

def team_indicator2(title,current_value,previous_value):
    fig = go.Figure(go.Indicator(
            mode="number+delta",  # 숫자와 델타 값을 함께 표시
            value=current_value,  # 현재 값
            delta={
                'position': "bottom",  # 델타 위치
                'reference': previous_value,  # 이전 값
                'valueformat': 'f',  # 델타 값 포맷
                'relative': False,  # 상대적 변화 표시
            },
            number={
                'valueformat': 'f',  # 숫자 포맷
                'font': {'size': 25,'color':'red'}  # 숫자 폰트 크기
            },
            title={'text': title, 'font':{'size':15}}  # 인디케이터 제목
            ))
    fig.update_layout(height=100)
    return fig


cards1 = html.Div([
    dbc.CardGroup(
    [
        dbc.Card(
            [
                dbc.CardHeader("경남Access", className="card-title"),
                dbc.CardBody(
                    [
                        dcc.Graph(figure=team_indicator1("장비수",len(df1))),
                        dcc.Graph(figure=team_indicator2("bias 불량",len(df1_bad),len(df2_bad)))
                    ]
                )                
            ]
        ),
        dbc.Card(
            [
                dbc.CardHeader("동부산품질개선팀", className="card-title"),
                dbc.CardBody(
                    [
                        dcc.Graph(figure=team_indicator1("장비수",len(df1_db))),
                        dcc.Graph(figure=team_indicator2("bias 불량",len(df1_bad_db),len(df2_bad_db)))
                    ]
                )                
            ]
        ),
        dbc.Card(
            [
                dbc.CardHeader("서부산품질개선팀", className="card-title"),
                dbc.CardBody(
                    [
                        dcc.Graph(figure=team_indicator1("장비수",len(df1_sb))),
                        dcc.Graph(figure=team_indicator2("bias 불량",len(df1_bad_sb),len(df2_bad_sb)))
                    ]
                )                
            ]
        ),
        dbc.Card(
            [
                dbc.CardHeader("김해품질개선팀", className="card-title"),
                dbc.CardBody(
                    [
                        dcc.Graph(figure=team_indicator1("장비수",len(df1_gh))),
                        dcc.Graph(figure=team_indicator2("bias 불량",len(df1_bad_gh),len(df2_bad_gh)))
                    ]
                )                
            ]
        ),
        dbc.Card(
            [
                dbc.CardHeader("울산품질개선팀", className="card-title"),
                dbc.CardBody(
                    [
                        dcc.Graph(figure=team_indicator1("장비수",len(df1_us))),
                        dcc.Graph(figure=team_indicator2("bias 불량",len(df1_bad_us),len(df2_bad_us)))
                    ]
                )                
            ]
        ),
        dbc.Card(
            [
                dbc.CardHeader("진주품질개선팀", className="card-title"),
                dbc.CardBody(
                    [
                        dcc.Graph(figure=team_indicator1("장비수",len(df1_jj))),
                        dcc.Graph(figure=team_indicator2("bias 불량",len(df1_bad_jj),len(df2_bad_jj)))
                    ]
                )                
            ]
        ),
        dbc.Card(
            [
                dbc.CardHeader("창원품질개선팀", className="card-title"),
                dbc.CardBody(
                    [
                        dcc.Graph(figure=team_indicator1("장비수",len(df1_cw))),
                        dcc.Graph(figure=team_indicator2("bias 불량",len(df1_bad_cw),len(df2_bad_cw)))
                    ]
                )                
            ]
        ),
        dbc.Card(
            [
                dbc.CardHeader("통영품질개선팀", className="card-title"),
                dbc.CardBody(
                    [
                        dcc.Graph(figure=team_indicator1("장비수",len(df1_ty))),
                        dcc.Graph(figure=team_indicator2("bias 불량",len(df1_bad_ty),len(df2_bad_ty)))
                    ]
                )                
            ]
        ),
        
    ],style={'width': '70vw','height': '60vh',"margin":'10px'}
)
])

# Layout
app.layout = html.Div(
    [
        html.H2("📡 SFP Bias 관리 시스템 📡 ",style={'font-weight':'bold','margin':'10px'}),
        dbc.Stack(
            [
                map,
                cards1
            ],
            direction="horizontal",
        ),
        html.Div(tb1)
    ]
)

    
if __name__ == '__main__':
    app.run_server(debug=True)
