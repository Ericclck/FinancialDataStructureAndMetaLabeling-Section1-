import pandas as pd
import numpy as np
from utils.sample_weights import *
import os

# import data 'data/ticks.csv'
prices = pd.read_csv(os.path.join('data','ticks.csv'))
prices.columns = ['id','price','volume','dollar','time','buyer_maker','_ignore']
prices = prices.set_index('id')

# import first touch 'data/processed/events.csv'
events = pd.read_csv(os.path.join('data','processed','events.csv'),index_col='id')

# truncate prices and events to 80% quartile of events index
events = events.loc[prices.index[0]:prices.index[int(len(prices.index)*0.8)]]
prices = prices.loc[prices.index[0]:prices.index[int(len(prices.index)*0.8)]]

# concurrency
concurrency = get_concurrency(prices.index, events['first_touch_index'])
print("Concurrency : ")
print(concurrency.describe())
print(concurrency.head())
print(concurrency.tail())

# uniqueness
uniqueness = get_uniqueness_from_concurrency(first_touch=events['first_touch_index'], concurrency=concurrency)
print(uniqueness.describe())
print(uniqueness.head())
print(uniqueness.tail())

# uniqueness decay
uniqueness_decay = get_uniqueness_decay(uniqueness, 0)
final_weights = uniqueness_decay * uniqueness
print(final_weights.describe())
print(final_weights.head())
print(final_weights.tail())

# save final_weights to csv
final_weights.to_csv(os.path.join('data','processed','final_weights.csv'), index=True)