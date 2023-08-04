from utils.labeling import *
import pandas as pd 
import numpy as np
import os

# import data
ticks = pd.read_csv(os.path.join('data','ticks.csv'))
ticks.columns = ['id','price','volume','dollar','time','buyer_maker','_ignore']
ticks = ticks.set_index('id')
rb = pd.read_csv(os.path.join('data/processed','ticks-run-dollars.csv'))
rb.set_index('id',inplace=True)
labels = pd.read_csv(os.path.join('data/processed','labels.csv'))
labels.columns = ['id','return','label']
labels.set_index('id',inplace=True)


# use trend following strategy of cross moving average to generate signals and assign side to new series with id as index
trend_following = pd.Series(np.where(rb['close'].rolling(20).mean() > rb['close'].rolling(50).mean(), 1, -1),index = rb.index,name='side')
trend_following = trend_following[50:]

# save trend following strategy to csv
trend_following.to_csv(os.path.join('data/processed','trend_following.csv'), index=True)

# read trend following strategy from csv
trend_following = pd.read_csv(os.path.join('data/processed','trend_following.csv'))
trend_following.columns = ['id','side']
trend_following = trend_following.set_index('id')
trend_following = trend_following.squeeze()

# Compute events
windows = 100
targets = pd.Series(std_pct_change(rb['close'].values, windows),index=rb.index[windows:])
vertical_barriers = get_vertical_barriers(ticks.index, rb.index, num_ticks=10000)
events = get_events(ticks['price'],rb.index,scalers_for_horizontal_barriers=(2,2),target=targets,min_return=0.0000001, num_threads=1, vertical_barriers=vertical_barriers,side=trend_following)
events.to_csv(os.path.join('data/processed','events.csv'), index=True)
meta_labels = get_labels(events, ticks['price'])

# store meta labels
meta_labels.to_csv(os.path.join('data/processed','meta_labels.csv'), index=True)