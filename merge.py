# build a random forest model to predict meta labels
import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from utils.labeling import *
from utils.model import *
import matplotlib.pyplot as plt

# import ticks data
ticks = pd.read_csv(os.path.join('data','ticks.csv'))
ticks.columns = ['id','price','volume','dollar','time','buyer_maker','_ignore']
ticks = ticks.set_index('id')

# compute stds
ewma_window = 100
stds = std_pct_change(ticks['price'].values, ewma_window)
stds = pd.Series(stds,index=ticks.index[ewma_window:],name='volatility')

# import run bars data
rb = pd.read_csv(os.path.join('data/processed','ticks-run-dollars.csv'))
rb.set_index('id',inplace=True)

# compute log return series for each columns (open,high,low,close,volume), remove inf values and nan values
rb['log_price'] = np.log(rb['close']).diff()
rb['log_volume'] = np.log(rb['volume']).diff()
rb['log_high'] = np.log(rb['high']).diff()
rb['log_low'] = np.log(rb['low']).diff()
rb['log_open'] = np.log(rb['open']).diff()


# fractional differentiation ([0.9453125 0.        0.9453125 0.9453125 0.9453125])
from fracdiff.sklearn import FracdiffStat,Fracdiff
# f = FracdiffStat()
# X = f.fit_transform(rb[['close', 'high', 'low', 'open','volume']])
# print(f.d_)
f =  Fracdiff(0.8)
X = f.fit_transform(rb[['close', 'high', 'low', 'open']])
# ADF
from statsmodels.tsa.stattools import adfuller
print("ADF p-values")
for i in range(X.shape[1]):
    print(f"pavlue : {adfuller(X[:,i])[1]}")



# add fractional diff series to rb
rb['fracdiff_close'] = X[:,0]
rb['fracdiff_high'] = X[:,1]
rb['fracdiff_low'] = X[:,2]
rb['fracdiff_open'] = X[:,3]
rb['fracdiff_volume'] = rb['volume']

rb = rb.replace([np.inf, -np.inf], np.nan).fillna(method="ffill").fillna(method="bfill")

# import labels
labels = pd.read_csv(os.path.join('data/processed','labels.csv'))
labels.columns = ['id','return','label']
labels.set_index('id',inplace=True)

# import meta labels
meta_labels = pd.read_csv(os.path.join('data/processed','meta_labels.csv'))
meta_labels.columns = ['id','return','meta_label']
meta_labels.set_index('id',inplace=True)

#import side
trend_following = pd.read_csv(os.path.join('data/processed','trend_following.csv'))
trend_following.columns = ['id','side']
trend_following = trend_following.set_index('id')
trend_following = trend_following.squeeze()

# merge meta labels with label column from labels, then merge with rb, then merge with side, then stds
df = labels.merge(meta_labels[['meta_label']],left_index=True,right_index=True)
df = df.merge(rb[['log_price','log_volume','log_high','log_low','log_open']],left_index=True,right_index=True)
df = df.merge(rb[['fracdiff_close','fracdiff_volume','fracdiff_high','fracdiff_low','fracdiff_open']],left_index=True,right_index=True)
df = df.merge(trend_following,left_index=True,right_index=True)
df = df.merge(stds,left_index=True,right_index=True)

# save df to csv
df.to_csv(os.path.join('data/processed','df.csv'), index=True)