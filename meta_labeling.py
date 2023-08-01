from utils.labeling import *
import pandas as pd 
import numpy as np
import os

# import data
ticks = pd.read_csv(os.path.join('data','BTCUSDT-trades-2023-06-16.csv'))
ticks.columns = ['id','price','volume','dollar','time','buyer_maker','_ignore']
ticks = ticks.set_index('id')
rb = pd.read_csv(os.path.join('data/processed','BTCUSDT-trades-2023-06-16-run-dollars.csv'))
rb.set_index('id',inplace=True)
labels = pd.read_csv(os.path.join('data/processed','labels.csv'))
labels.columns = ['id','return','label']
labels.set_index('id',inplace=True)

# use trend following strategy of cross moving average to generate signals and assign side to new series with id as index
# trend_following = pd.Series(np.where(ticks['price'].rolling(100).mean() > ticks['price'].rolling(1000).mean(), 1, -1),index = ticks.index,name='side')
# trend_following = trend_following[1000:]

# save trend following strategy to csv
# trend_following.to_csv(os.path.join('data/processed','trend_following.csv'), index=True)

# read trend following strategy from csv
trend_following = pd.read_csv(os.path.join('data/processed','trend_following.csv'))
trend_following.columns = ['id','side']
trend_following = trend_following.set_index('id')
trend_following = trend_following.squeeze()

# Compute events
targets = pd.Series(std_pct_change(ticks['price'].values, 100),index=ticks.index[100:])
vertical_barriers = get_vertical_barriers(ticks.index, rb.index, num_transactions=100)
events = get_events(ticks['price'],rb.index,scalers_for_horizontal_barriers=(1,1),target=targets,min_return=0.000001, num_threads=1, vertical_barriers=vertical_barriers,side=trend_following)
meta_labels = get_labels(events, ticks['price'])

# store meta labels
meta_labels.to_csv(os.path.join('data/processed','meta_labels.csv'), index=True)