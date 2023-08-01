import pandas as pd
import numpy as np
from utils.analysis import *
from utils.bars import *

# import dollar bars, dollar imbalance bars, dollar run bars
db = pd.read_csv('data/processed/BTCUSDT-trades-2023-06-16-dollar-bars.csv')
imb = pd.read_csv('data/processed/BTCUSDT-trades-2023-06-16-imbalance-dollars.csv')
rb = pd.read_csv('data/processed/BTCUSDT-trades-2023-06-16-run-dollars.csv')


# cusum filter
cusum_filter_db = get_events(db['close'], 0.1)
cusum_filter_imb = get_events(imb['close'], 0.1)
cusum_filter_rb = get_events(rb['close'], 0.1)

# index using cusum filter
db_cusum = db.loc[cusum_filter_db]
imb_cusum = imb.loc[cusum_filter_imb]
rb_cusum = rb.loc[cusum_filter_rb]

# compute log return series for each bar type, remove inf values and nan values
db_cusum = np.log(db_cusum['close']).diff()
db_cusum = db_cusum.replace([np.inf, -np.inf], np.nan).dropna()
imb_cusum = np.log(imb_cusum['close']).diff()
imb_cusum = imb_cusum.replace([np.inf, -np.inf], np.nan).dropna()
rb_cusum = np.log(rb_cusum['close']).diff()
rb_cusum = rb_cusum.replace([np.inf, -np.inf], np.nan).dropna()

# stationary test
adf_tests(db_cusum,log_diff=False)
adf_tests(imb_cusum,log_diff=False)
adf_tests(rb_cusum,log_diff=False)

# normality test
normal_plots(db_cusum,"Dollar Bars Cusum Filter",log_diff=False)
normal_plots(imb_cusum,"Imb Bars Cusum Filter",log_diff=False)
normal_plots(rb_cusum,"Run Bars Cusum Filter",log_diff=False)

# acf (6 subplots) 3 bars without cusum filter, 3 bars with cusum filter
from statsmodels.graphics.tsaplots import plot_acf

plt.figure(figsize=(16,12))
ax1 = plt.subplot(231)
plot_acf(np.log(db['close']).diff().dropna(), lags=10, zero=False, ax=ax1)
ax1.set_ylim([-0.05,0.3])
plt.title('Dollar Bars AutoCorrelation')

ax2 = plt.subplot(232)
plot_acf(np.log(imb['close']).diff().dropna(), lags=10, zero=False, ax=ax2)
ax2.set_ylim([-0.05,0.3])
plt.title('Imb Bars AutoCorrelation')

ax3 = plt.subplot(233)
plot_acf(np.log(rb['close']).diff().dropna(), lags=10, zero=False, ax=ax3)
ax3.set_ylim([-0.05,0.3])
plt.title('Run Bars AutoCorrelation')

ax4 = plt.subplot(234)
plot_acf(db_cusum, lags=10, zero=False, ax=ax4)
ax4.set_ylim([-0.05,0.3])
plt.title('Dollar Bars Cusum Filter AutoCorrelation')

ax5 = plt.subplot(235)
plot_acf(imb_cusum, lags=10, zero=False, ax=ax5)
ax5.set_ylim([-0.05,0.3])
plt.title('Imb Bars Cusum Filter AutoCorrelation')

ax6 = plt.subplot(236)
plot_acf(rb_cusum, lags=10, zero=False, ax=ax6)
ax6.set_ylim([-0.05,0.4])
plt.title('Run Bars Cusum Filter AutoCorrelation')

plt.show()




