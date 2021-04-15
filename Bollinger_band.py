import yfinance as yf
from pandas_datareader import data as pdr
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# 시작일, 종료일 (2019, 11 ,3 - 2020, 12, 1)
start_date = datetime(2019, 11, 3)
end_date = datetime(2020, 12, 1)
#get_data_yahoo '005930.KS'

yf.pdr_override()
df = pd.DataFrame()
df = pdr.get_data_yahoo('005930.KS', start_date, end_date)

# 볼린저밴드 MA20, stddev, upper, lower
df['MA20'] = df['Close'].rolling(window=20, min_periods=1).mean()
df['stddev'] = df['Close'].rolling(window=20, min_periods=1).std()
df['upper'] = df['MA20'] + (df['stddev'] * 2)
df['lower'] = df['MA20'] - (df['stddev'] * 2)
print(df)

# plot
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['Close'], color='green', label='Samsung')
plt.plot(df.index, df['MA20'], 'k--', label='MA20')
plt.plot(df.index, df.upper, 'r--', label='upper')
plt.plot(df.index, df.lower, 'b--', label='lower')
plt.fill_between(df.index, df.upper, df.lower, color='0.9')
plt.grid(True)
plt.legend(loc='best')
plt.show()

# percent b + bandwidth
# (%b = (종가 - 하단) / (상단 - 하단)
# bandwidth = (상단 - 하단) / MA20
df['pb'] = (df.Close - df.lower) / (df.upper - df.lower)
df['bandwidth'] = (df.upper - df.lower) / df.MA20

# plot bandwidth
plt.figure(figsize = (10, 5))
plt.plot(df.index, df.pb, c='black', label='Bandwidth')
plt.plot(df.index, df.bandwidth, c='orange', label='Bandwidth')
plt.legend(loc='best')
plt.show()

# 추세추종[trend follwing]
# 1.tp[typical price] = (고가 + 저가 + 종가) / 3
df['tp'] = (df.High + df.Low + df.Close) /3
print(df)

# 1번째 tp < i+1번째 tp인 경우 p(positive)mf
# 1번째 tp >= i+1번째 tp인 경우 n(negative)mf
df['pmf'] = 0
df['nmf'] = 0
for i in range(len(df.Close) - 1):
    if df.tp.values[i] < df.tp.values[i+1]:
        # 중심가 * 거래량
        df.pmf.values[i+1] = df.tp.values[i+1] * df.Volume.values[i+1]
        df.nmf.values[i+1] = 0
    else:
        # df.tp.values[i] >= df.tp.values[i+1]
        df.nmf.values[i+1] = df.tp.values[i+1] * df.Volume.values[i+1]
        df.pmf.values[i+1] = 0

# MFR(money flow ratio): 10일 동안의 pmf의 합 / 10일 동안의 nmf의 합
df['mfr'] = df.pmf.rolling(window=10).sum() / df.nmf.rolling(window=10).sum()

# MFI10: 10일 동안의 현금 흐름 100 - (100 / ( 1 + mfr))
df['mfi10'] = 100 - (100 / (1 + df.mfr))

# 20일(window size) 이전 데이터 정제
df = df[19:]

# plot [ %b, mfi 10 ]
plt.figure(figsize=(10, 5))
plt.plot(df.index, df.pb * 100, c='black', label='pb')
plt.plot(df.index, df.mfi10, 'r--', label='MFI 10d')
plt.yticks([-20, 0, 20, 40, 60, 80, 100, 120])

# plot [ 추세추종 매매 시기 (매수) pb > 0.8, mfi > 80 (매도) pb < 0.2, mfi < 20
for i in range(len(df.Close)):
    if df.pb.values[i] > 0.8 and df.mfi10.values[i] > 80:
        plt.plot(df.index.values[i], 0, 'r^')
    elif df.pb.values[i] < 0.2 and df.mfi10.values[i] > 20:
        plt.plot(df.index.values[i], 0, 'bv')
plt.legend(loc='best')
plt.grid(True)
plt.show()

# 일중강도[intraday intensity]: 종가의 위치를 토대로 주식 종목의 자금흐름
# II = (2 * 종가 - 고가 - 저가 / 고가 - 저가) * 거래량
df['ii'] = (2 * df['Close'] - df['High'] - df['Low'] / df['High'] - df['Low']) * df['Volume']

# II%[intraday intensity %]: 거래량으로 II를 표준화 (21일) = 일중강도의 21일합 / 거래량의 21일 합 * 100
df['iip21'] = df.ii.rolling(window=21).sum() / df.Volume.rolling(window=21).sum() * 100
print(df)

#plot [ 추세추종 매매 시기 (매수) pb < 0.05 iip21>0, (매도) pb > 0.95 iip21<0
plt.figure(figsize=(10, 5))
plt.bar(df.index, df['iip21'], color='g', label='II% 21d')
for i in range(len(df.Close)):
    if df.pb.values[i] < 0.05 and df.iip21.values[i] > 0:
        plt.plot(df.index.values[i], 0, 'r^')
    elif df.pb.values[i] > 0.95 and df.iip21.values[i] < 0:
        plt.plot(df.index.values[i], 0, 'bv')
plt.legend(loc='best')
plt.grid(True)
plt.show()

#################################

plt.figure(figsize=(10, 10))
plt.subplot(411)
plt.plot(df.index, df.MA20, 'k--', label='MA20')
plt.plot(df.index, df.Close, c='green')
plt.plot(df.index, df.upper, 'r--', label='upper')
plt.plot(df.index, df.lower, 'b--', label='lower')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
for i in range(len(df.Close)):
    if df.pb.values[i] > 0.8 and df.mfi10.values[i] > 80:
        plt.plot(df.index.values[i], df.Close.values[i], 'r^')
    elif df.pb.values[i] < 0.2 and df.mfi10.values[i] < 20:
        plt.plot(df.index.values[i], df.Close.values[i], 'bv')
for i in range(len(df.Close)):
    if df.pb.values[i] < 0.05 and df.iip21.values[i] > 0:
        plt.plot(df.index.values[i], df.Close.values[i], 'r^')
    elif df.pb.values[i] > 0.95 and df.iip21.values[i] < 0:
        plt.plot(df.index.values[i], df.Close.values[i], 'bv')

plt.legend(loc='best')
plt.grid(True)
plt.subplot(412)
plt.plot(df.index, df.pb * 100, c='black', label='pb')
plt.plot(df.index, df.mfi10, 'r--', label='MFI 10 days')
plt.yticks([-20, 0, 20, 40, 60, 80, 100, 120])
for i in range(len(df.Close)):
    if df.pb.values[i] > 0.8 and df.mfi10.values[i] > 80:
        plt.plot(df.index.values[i], 0, 'r^')
    elif df.pb.values[i] < 0.2 and df.mfi10.values[i] < 20:
        plt.plot(df.index.values[i], 0, 'bv')

plt.grid(True)
plt.legend(loc='best')
plt.subplot(413)
plt.plot(df.index, df.bandwidth, c='orange', label='pb')
plt.grid(True)
plt.legend(loc='best')
plt.subplot(414)
plt.bar(df.index, df['iip21'], color='g', label='II% 21day')
for i in range(len(df.Close)):
    if df.pb.values[i] < 0.05 and df.iip21.values[i] > 0:
        plt.plot(df.index.values[i], 0, 'r^')
    elif df.pb.values[i] > 0.95 and df.iip21.values[i] < 0:
        plt.plot(df.index.values[i], 0, 'bv')
plt.grid(True)
plt.legend(loc='best')
plt.show()

