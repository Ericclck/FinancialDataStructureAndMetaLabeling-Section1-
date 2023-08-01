import pandas as pd
import numpy as np
from utils.analysis import *

tick_bars = pd.read_csv('data/processed/BTCUSDT-trades-2023-06-16-tick-bars.csv')
volume_bars = pd.read_csv('data/processed/BTCUSDT-trades-2023-06-16-volume-bars.csv')
dollar_bar = pd.read_csv('data/processed/BTCUSDT-trades-2023-06-16-dollar-bars.csv')
imb = pd.read_csv('data/processed/BTCUSDT-trades-2023-06-16-imbalance-dollars.csv')
rb = pd.read_csv('data/processed/BTCUSDT-trades-2023-06-16-run-dollars.csv')
tick_bars_returns = np.log(tick_bars['close']).diff().dropna()
volume_bars_returns = np.log(volume_bars['close']).diff().dropna()
dollar_bar_returns = np.log(dollar_bar['close']).diff().dropna()
imb_returns = np.log(imb['close']).diff().dropna()
rb_returns = np.log(rb['close']).diff().dropna()


adf_tests(tick_bars_returns,log_diff=False)
adf_tests(volume_bars_returns,log_diff=False)
adf_tests(dollar_bar_returns,log_diff=False)
adf_tests(imb_returns,log_diff=False)
adf_tests(rb_returns,log_diff=False)

normal_plots(tick_bars['close'],"Tick Bars",log_diff=True)
normal_plots(volume_bars['close'],"Volume Bars",log_diff=True)
normal_plots(dollar_bar['close'],"Dollar Bars",log_diff=True)
normal_plots(imb['close'],"Imbalance Bars",log_diff=True)
normal_plots(rb['close'],"Run Bars",log_diff=True)


from statsmodels.graphics.tsaplots import plot_acf
plt.figure(figsize=(16,12))

ax1 = plt.subplot(231)
plot_acf(tick_bars_returns, lags=10, zero=False, ax=ax1)
ax1.set_ylim([-0.05,0.3])
plt.title('Tick Bars AutoCorrelation')

ax2 = plt.subplot(232)
plot_acf(volume_bars_returns, lags=10, zero=False, ax=ax2)
ax2.set_ylim([-0.05,0.3])
plt.title('Volume Bars AutoCorrelation')

ax3 = plt.subplot(233)
plot_acf(dollar_bar_returns, lags=10, zero=False, ax=ax3)
ax3.set_ylim([-0.05,0.3])
plt.title('Dollar Bars AutoCorrelation')

ax4 = plt.subplot(234)
plot_acf(imb_returns, lags=10, zero=False, ax=ax4)
ax4.set_ylim([-0.05,0.3])
plt.title('Imb Bars AutoCorrelation')

ax5 = plt.subplot(235)
plot_acf(rb_returns, lags=10, zero=False, ax=ax5)
ax5.set_ylim([-0.05,0.3])
plt.title('Run Bars AutoCorrelation')

plt.show()
