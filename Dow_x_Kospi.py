# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 22:52:41 2020

@author: yangs
"""


import yfinance as yf
from pandas_datareader import data as pdr
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

yf.pdr_override()
# 시작일, 종료일
start_date = datetime(2000, 11, 3)
end_date = datetime(2020, 12, 1)

# KOSPI, DOW 지수 불러오기 kospi:'^KS11', dow:'^DJI'
dowxkospi = pd.DataFrame()

dow = pdr.get_data_yahoo('^DJI', start_date, end_date)
kospi = pdr.get_data_yahoo('^KS11', start_date, end_date)

# 1.Kospi와 Dow의 Close 값으로 이루어진 데이터 프레임 생성
dowxkospi['dow'] = dow['Close']
dowxkospi['kospi'] = kospi['Close']

# data 정제
# 산점도 분석 !산점도는 x와 y가 1:1 매칭이 되어야 한다. 데이터 정제 필수
#(1)
dowxkospi.fillna(method='ffill', inplace=True)
dowxkospi.fillna(method='bfill', inplace=True)

# 3.선형회귀 분석 import scipy
#(2)
regr = stats.linregress(dowxkospi['dow'], dowxkospi['kospi'])
regr_line = 'Y={}*x*{}'.format(round(regr.slope,3), round(regr.intercept,3))
print(dowxkospi['kospi'])

# 지수화 비교 : 시작일로부터의 변화 정도
#(3)
k = (dowxkospi['kospi'] / dowxkospi['kospi'].loc[start_date]) * 100
d = (dowxkospi['dow'] / dowxkospi['dow'].loc[start_date]) * 100

# 두 지수에 대한 graphic visualization figsize=(9,5)
plt.figure(figsize=(10, 15))
plt.subplot(311)
plt.plot(dowxkospi.index, dowxkospi['kospi'], 'gold', label='Kospi')
plt.plot(dowxkospi.index, dowxkospi['dow'], 'tomato', label='Dow Jones')
plt.grid(True)
plt.legend(loc='best')
ax = plt.gca()
ax.set_facecolor('lightgrey')
plt.title('Dow x Kospi')
plt.xlabel('Time')
plt.ylabel('Index')

# 두 지수에 대한 graphic visualization
plt.subplot(312)
plt.plot(k.index, k, 'tan', label='Kospi(normalized)')
plt.plot(d.index, d, 'brown', label='Dow Jones(normalized)')
plt.grid(True)
plt.legend(loc='best')
ax = plt.gca()
ax.set_facecolor('lightgrey')
plt.title('Dow x Kospi (normalized)')
plt.xlabel('Time')
plt.ylabel('Index')

# 두 산점도와 회귀선 visualization 
plt.subplot(313)
#(4)
plt.scatter(dowxkospi['dow'], dowxkospi['kospi'], marker='.', facecolors='lavender', edgecolors='royalblue')
plt.plot(dowxkospi['dow'], regr.slope * dowxkospi['dow'] + regr.intercept, 'lime')
plt.legend(['Dow x Kospi', regr_line])
ax = plt.gca()
ax.set_facecolor('lightgrey')
plt.title('Dow x Kospi (R={})'.format(round(regr.rvalue, 3)))
plt.xlabel('Dow Jones')
plt.ylabel('Kospi')
plt.show()


