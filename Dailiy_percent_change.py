# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 21:56:13 2020

@author: yangs
"""

#pip install yfinance
#pip install pandas_datareader

import yfinance as yf
from pandas_datareader import data as pdr
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

# yahoo finance 에서 data를 추출
# datareader는 웹 상의 데이터를 dataframe 객체로 만드는 기능을 함

def get_my_data(stocks, startDate, endDate, columnName='Close'):
    df_res = pd.DataFrame()
    for i in stocks.keys():
        df_res[i] = pdr.get_data_yahoo(stocks[i], startDate, endDate)['Close']    
    return df_res

yf.pdr_override()
# 종목 dictionary : 'Samsung' : '005930.KS', 'Tesla' : 'TSLA'

my_stocks = dict({'Samsung' : '005930.KS', 'Tesla' : 'TSLA'})
# 시작일, 종료일
# get_data_yahoo로 data 얻기

start_date = datetime(2017, 11, 3)
end_date = datetime(2020, 12, 1)
my_data = get_my_data(my_stocks, start_date, end_date)
print(my_data)


# data = pdr.get_data_yahoo('005930.KS', start_date, end_date)

# df_temp_data = pd.DataFrame()
# df_temp_data['Close'] = pdr.get_data_yahoo('005930.KS', start_date, end_date)['Close']
# df_temp_data['Adj close'] = pdr.get_data_yahoo('005930.KS', start_date, end_date)['Adj Close']

# # KOSPI, DOW 지수 불러오기 kospi:'^KS11', dow:'^DJI'
# dowxkospi = pd.DataFrame()

# dow = pdr.get_data_yahoo('^DJI', start_date, end_date)
# kospi = pdr.get_data_yahoo('^KS11', start_date, end_date)

# # 1.Kospi와 Dow의 Close 값으로 이루어진 데이터 프레임 생성
# dowxkospi['dow'] = dow['Close']
# dowxkospi['kospi'] = kospi['Close']



# data 정제
my_data.fillna(method='ffill', inplace=True)
my_data.fillna(method='bfill', inplace=True)
print(my_data)

#visualization 
plt.plot(my_data.index, my_data['Samsung'], c='orange', label='Samsung')
plt.plot(my_data.index, my_data['Tesla'], c='#cc0000', label='Tesla')
plt.legend(loc='best')
plt.show()
# 1. Price, 2. Daily percent change, 3. Cumulative summation
# Daily percent change 구하기 shift()
samsung_dpc = (my_data['Samsung'] - my_data['Samsung'].shift(1))/my_data['Samsung'].shift(1)
samsung_dpc[start_date] = 0
tesla_dpc = (my_data['Tesla'] - my_data['Tesla'].shift(1))/my_data['Tesla'].shift(1)
tesla_dpc[start_date] = 0

df_dpc = pd.DataFrame()
df_dpc['Samsung'] = samsung_dpc
df_dpc['Tesla'] = tesla_dpc
print(df_dpc)

# Cumulative summation. cumsum()
df_cumsum = pd.DataFrame()
df_cumsum['SamsungCumsum'] = samsung_dpc.cumsum()
df_cumsum['TeslaCumsum'] = tesla_dpc.cumsum()
print(df_cumsum)

temp_data = pd.concat([df_dpc, df_cumsum], axis=1)
print(temp_data)

#visualization
plt.figure(figsize=(10,15))
plt.subplot(311)
plt.plot(my_data.index, my_data['Samsung'], c='orange', label='Samsung')
plt.plot(my_data.index, my_data['Tesla'], c='#cc0000', label='Tesla')
plt.legend(loc='best')
plt.subplot(312)
plt.plot(df_dpc.index, df_dpc['Samsung'], c='orange', label='Samsung')
plt.plot(df_dpc.index, df_dpc['Tesla'], c='green', label='Tesla')
plt.legend(loc='best')
plt.subplot(313)
plt.plot(df_dpc.index, df_dpc['Samsung'].cumsum(), c='orange', label='Samsung')
plt.plot(df_dpc.index, df_dpc['Tesla'].cumsum(), c='green', label='Tesla')
plt.legend(loc='best')
plt.show()


# 산점도 분석 !산점도는 x와 y가 1:1 매칭이 되어야 한다. 데이터 정제 필수

# 3.선형회귀 분석 import scipy

# 지수화 비교 : 시작일로부터의 변화 정도

# 두 지수에 대한 graphic visualization figsize=(9,5)
plt.figure(figsize=(10, 15))
plt.subplot(311)
plt.plot(dowxkospi.index, dowxkospi['kospi'], 'r--', label='Kospi')
plt.plot(dowxkospi.index, dowxkospi['dow'], 'b', label='Dow Jones')
plt.grid(True)
plt.legend(loc='best')

# 두 지수에 대한 graphic visualization
plt.subplot(312)
plt.plot(k.index, k, 'r--', label='Kospi(normalized)')
plt.plot(d.index, d, 'b', label='Dow Jones(normalized)')
plt.grid(True)
plt.legend(loc='best')

# 두 산점도와 회귀선 visualization
plt.subplot(313)

plt.show()
