from pandas_datareader import data as pdr
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 시작일, 종료일
# meta_data: 1. 일년 개장일
start_date = datetime(2020, 11, 3)
end_date = datetime(2020, 12, 1)
one_year = 252

# 포트폴리오 종목 4개 : dictionary / 'Coca cola': 'COKE', 'Tesla': 'TSLA', 'Amazon': 'AMZN', 'Google': 'GOOG'
my_stocks = dict({'Coca cola': 'COKE', 'Tesla': 'TSLA', 'Amazon': 'AMZN', 'Google': 'GOOG'})

# close 가격으로 데이터 프레임 생성 my_portfolio, ['Close']
df_stocks = pd.DataFrame()
# print(my_stocks['Coca cola'])

# 1. 포트폴리오 데이터 프레임 생성
for i in my_stocks.keys():
    df_stocks[i] = pdr.get_data_yahoo(my_stocks[i], start_date, end_date)['Close']
# print(df_stocks)

# 2. 종목 데이터 -> 데이터 프레임
# 누락데이터 정제
df_stocks.fillna(method='ffill', inplace=True)
df_stocks.fillna(method='bfill', inplace=True)
print(df_stocks)

# 1.일간 수익률: pct_chage(), 2. 연간 수익률: mean()*one_year, 3.일간 리스크: cov():일간 변동률의 공분산, 4. 연간 리스크
# 연간 수익률 = 일간 수익률의 평균 * 252
daily_ret = df_stocks.pct_change()
annual_ret = daily_ret.mean() * 252
daily_cov = daily_ret.cov()
annual_cov = daily_cov * 252
print(annual_cov)
# 이 포트폴리오의 수익률, 위험률, 각 종목의 비중
port_weights = []
port_ret = []
port_risk = []
sharpe_ratio = []
#print(len(my_stocks))

my_res = pd.DataFrame()
my_res_left = pd.DataFrame()

# 몬테카를로 시뮬레이션을 통한 다양한 포트폴리오의 생성 (포트폴리오 리스크 : sqrt ( (종목별비증)T((종목별 위험)(종목별비중) )
for _ in range(50000):
    # 1. 종목별 가중치 생성
    weights = np.random.random(len(my_stocks))
#    print(weights, np.sum(weights))
    weights /= np.sum(weights)
#    print(weights, np.sum(weights))

    # 2. 가중치에 따른 수익률
    returns = np.dot(weights, annual_ret)
    # 3. 가중치에 따른 위험률
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))

    port_weights.append(weights)
    port_ret.append(returns)
    port_risk.append(risk)
    sharpe_ratio.append(returns/risk)

my_res_left['returns'] = port_ret
my_res_left['risk'] = port_risk
my_res_left['sharpe'] = sharpe_ratio
#print(my_res)

# res_portfolio_right dataframe 'my_stocks_weight' 생성
my_stock_weight = pd.DataFrame()

# 1. 종목별 가중치 전치 with np
transpose_weight = np.array(port_weights).T
#print(port_weights)
#print(transpose_weight)

# 2. 종목별 가중치 Dataframe 생성
for i, v in enumerate(my_stocks.keys()):
    my_stock_weight[v] = transpose_weight[i]

# 최종 데이터 프레임 생성 with concat
my_res = pd.concat([my_res_left, my_stock_weight], axis=1)
print(my_res)

# sharpe_ratio : 1.max_sharpe, 2.min_risk
max_sharpe = my_res.loc[my_res['sharpe'] == my_res['sharpe'].max()]
min_risk = my_res.loc[my_res['risk'] == my_res['risk'].min()]
print(max_sharpe, min_risk)

#chart visualization scatter, cmap=viridis, figsize = 11,7
my_res.plot.scatter(x='risk', y='returns', c='sharpe', cmap='viridis', edgecolors='black', figsize=(11, 7), grid=True)
plt.scatter(x=max_sharpe['risk'], y=max_sharpe['returns'], marker='X', s=200)
plt.scatter(x=min_risk['risk'], y=min_risk['returns'], marker='*', s=200)
plt.title('Efficient Frontier')
plt.show()
