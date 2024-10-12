import dash
import pandas as pd
import numpy as np
import os


df = pd.read_csv('D:/dev/bias/pages/sqllab_dul_tb__sfp_bias__sfp_vendor_20241012T071133.csv')

date1 = df['dt'].max()
date2 = df['dt'].min()

# 데이터 가공 (bias 값 %제거, Null값 처리)
df['txbs1_set'] = df['txbs1'].str.split('%').str[0]
df['txbs1_set'] = pd.to_numeric(df['txbs1_set'], errors='coerce')
df['txbs2_set'] = df['txbs2'].str.split('%').str[0]
df['txbs2_set'] = pd.to_numeric(df['txbs2_set'], errors='coerce')
df['txbs1_set'] = df['txbs1_set'].fillna(0).astype(int)
df['txbs2_set'] = df['txbs2_set'].fillna(0).astype(int)


# 불량국소 추출 

# txbs1 불량
def classify1(row):
    if row['txbs1_set'] >=80:
        return '불량'
    else:
        return '양호'

# txbs2불량
def classify2(row):
    if row['txbs2_set'] >=80:
        return '불량'
    else:
        return '양호'

df['Noti1'] = df.apply(lambda row: classify1(row), axis=1)
df['Noti2'] = df.apply(lambda row: classify2(row), axis=1)

# Total 불량내역
def classify3(row):
    if row['Noti1'] == '불량':
        if row['Noti2'] == '불량':
            return 'txbs1,txbs2 불량'
        else:
            return 'txbs1 불량'
    elif row['Noti2'] == '불량':
        return 'txbs2 불량'
    else:
        return '양호'

df['Noti3'] = df.apply(lambda row: classify3(row), axis=1)

# 전일 데이터
df1 = df.loc[df['dt'] == date1]

# 2일 전 데이터
df2 = df.loc[df['dt'] == date2]


df1_bad = df1.loc[df1['Noti3'] != '양호']
df2_bad = df2.loc[df2['Noti3'] != '양호']

df1_bad_bs1 = df1_bad.loc[df1_bad['Noti1'] == '불량']
# df1_bad_bs1_vd = df1_bad_bs1.groupby(['vendor1')['dul_'].count()

# # df1_bad.to_csv('df1_bad.csv',encoding='utf-8-sig')
# df1_bad.to_csv('df1_bad.csv',encoding='utf-8-sig')
