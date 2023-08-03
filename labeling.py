from utils.labeling import *
from utils.bars import get_run_dollar_bar
import pandas as pd
import numpy as np
import os
# from mlfinlab.util.multiprocess import mpPandasObj

# import data
ticks = pd.read_csv(os.path.join('data','BTCUSDT-trades-2023-06-16.csv'))
ticks.columns = ['id','price','volume','dollar','time','buyer_maker','_ignore']
ticks = ticks.set_index('id')
db = pd.read_csv(os.path.join('data/processed','BTCUSDT-trades-2023-06-16-run-dollars.csv'))
# db_indices = get_run_dollar_bar(ticks, 10, indices_only= True)
db_indices = db['id'].values




# compute std of pct_change
ewma_window = 100
stds = std_pct_change(ticks['price'].values, ewma_window)
stds = pd.Series(stds,index=ticks.index[ewma_window:])
# print(stds.describe())

# compute vertical barriers
# print(db['id'].diff().max())
vertical_barriers = get_vertical_barriers(ticks.index, db_indices, num_transactions=1000)
# print(vertical_barriers)

# compute events then labels
events = get_events(ticks['price'], db_indices,scalers_for_horizontal_barriers=(2,2),target=stds,min_return=0.0000001, num_threads=1, vertical_barriers=vertical_barriers)
events.to_csv(os.path.join('data/processed','events.csv'), index=True)
labels = get_labels(events, ticks['price'])

# store labels
labels.to_csv(os.path.join('data/processed','labels.csv'), index=True)