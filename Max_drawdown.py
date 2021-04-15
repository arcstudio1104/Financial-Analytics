#주식에서의 1년 - 252일
import yfinance as yf
from pandas_datareader import data as pdr
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
yf.pdr_override()

# 시작일, 종료일
start_date = datetime(1990, 11, 3)
end_date = datetime(2020, 12, 1)

# google -> 검색창 -> yahoo finance kospi
# KOSPI 지수 받아오기 '^KS11'
kospi_index = pdr.get_data_yahoo('^KS11', start_date, end_date)
window = 100

#plt.plot(kospi_index.index, kospi_index['Adj Close'], c='orange')
#plt.show()

# peak, drawdown, max_drawdown : rolling()

# window 기준으로 가장 높은 값을 찾는다.
peak = kospi_index['Adj Close'].rolling(window, min_periods=1).max()
# drawdown은 peak로부터 얼만큼 떨어졌는지 (낙폭)
drawdown = kospi_index['Adj Close']/peak - 1
max_drawdown = drawdown.rolling(window, min_periods=1).min()
print(max_drawdown[max_drawdown == max_drawdown.min()])
# visualization figsize=9,7
plt.figure(figsize=(9,7))
plt.subplot(211)
kospi_index['Close'].plot(label='KOSPI', title='KOSPI MDD')
plt.subplot(212)
drawdown.plot(c='b', label='Drawdown')
max_drawdown.plot(c='red', label='Max Drawdonw')
plt.show()
# max_dd 가 최소였던 지점
