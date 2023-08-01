import pandas as pd
import numpy as np
from utils.bars import *
from utils.analysis import *
import os

#import data AdrBalCnt
AdrBalCnt = pd.read_csv(os.path.join('data','AdrBalCnt.csv'))
NetFlowBinance = pd.read_csv(os.path.join('data','NetFlowBinance.csv'))

AdrBalCnt['10k_to_100k_native'] = AdrBalCnt['BTC / Addresses, with balance, greater than 10K native units, count'] - AdrBalCnt['BTC / Addresses, with balance, greater than 100K native units, count']
AdrBalCnt['10k_to_100k_native_log_diff'] = np.log(AdrBalCnt['10k_to_100k_native']).diff()
AdrBalCnt['log_price'] = np.log(AdrBalCnt['BTC / Price, USD']).diff()
AdrBalCnt = AdrBalCnt.replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)

NetFlowBinance['log_price'] = np.log(NetFlowBinance['BTC / Price, USD']).diff()
NetFlowBinance['BTC / Flow, net, Binance, native units log_diff'] = np.log(NetFlowBinance['BTC / Flow, net, Binance, native units']).diff()
NetFlowBinance = NetFlowBinance.replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)


# cusum filter
price_events = get_events(AdrBalCnt['log_price'], 0.1) 
price_cusum = AdrBalCnt.loc[price_events,:]
price_cusum['log_price'] = np.log(price_cusum['BTC / Price, USD']).diff()
price_cusum = price_cusum.replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)

balance_events = get_events(AdrBalCnt['10k_to_100k_native_log_diff'], 0.02)
balance_cusum = AdrBalCnt.loc[balance_events,:]
balance_cusum['10k_to_100k_native_log_diff'] = np.log(balance_cusum['10k_to_100k_native']).diff()
balance_cusum['log_price'] = np.log(balance_cusum['BTC / Price, USD']).diff()
balance_cusum = balance_cusum.replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)

flow_cusum = NetFlowBinance.loc[get_events(NetFlowBinance['BTC / Flow, net, Binance, native units'], 1),:]
flow_cusum['log_price'] = np.log(flow_cusum['BTC / Price, USD']).diff()
flow_cusum['BTC / Flow, net, Binance, native units log_diff'] = np.log(flow_cusum['BTC / Flow, net, Binance, native units']).diff()
flow_cusum = flow_cusum.replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)

# descriptive stats for cusum filter
print(price_cusum['log_price'].describe())
print(balance_cusum['10k_to_100k_native_log_diff'].describe())
print(flow_cusum['BTC / Flow, net, Binance, native units log_diff'].describe())


# stationary test
adf_tests(AdrBalCnt['log_price'],log_diff=False)
adf_tests(price_cusum['log_price'],log_diff=False)
adf_tests(flow_cusum['log_price'],log_diff=False)
adf_tests(balance_cusum['log_price'],log_diff=False)

# normality plots
normal_plots(AdrBalCnt['log_price'],title='BTC log Price')
normal_plots(price_cusum['log_price'],title='BTC log Price cusum filter')
normal_plots(flow_cusum['log_price'],title='Binance net flow cusum filter')
normal_plots(balance_cusum['log_price'],title='Balance 10k counts cusum filter')

# acf plots
from statsmodels.graphics.tsaplots import plot_acf

plt.figure(figsize=(16,12))

ax1 = plt.subplot(221)
plot_acf(AdrBalCnt['log_price'], lags=10, zero=False, ax=ax1)
ax1.set_ylim(-0.15,0.15)
plt.title('BTC log Price')

ax2 = plt.subplot(222)
plot_acf(flow_cusum['log_price'], lags=10, zero=False, ax=ax2)
ax2.set_ylim(-0.15,0.15)
plt.title('BTC / Flow, net, Binance, native units cusum filter')

ax3 = plt.subplot(223)
plot_acf(price_cusum['log_price'], lags=10, zero=False, ax=ax3)
ax3.set_ylim(-0.15,0.15)
plt.title('BTC log Price cusum filter')

ax4 = plt.subplot(224)
plot_acf(balance_cusum['log_price'], lags=10, zero=False, ax=ax4)
ax4.set_ylim(-0.15,0.15)
plt.title('BTC 10k to 100k native log diff (log_price) cusum filter')

plt.show()


