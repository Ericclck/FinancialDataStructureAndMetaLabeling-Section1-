import pandas as pd
import numpy as np
import os
from utils.sequential_bootstrapping import *

# import data
prices = pd.read_csv(os.path.join('data','BTCUSDT-trades-2023-06-16.csv'))
prices.columns = ['id','price','volume','dollar','time','buyer_maker','_ignore']
prices = prices.set_index('id')

# import first touch
events = pd.read_csv(os.path.join('data','processed','events.csv'),index_col=0)

# sequential bootstrapping
indicator_matrix = construct_indicator_matrix(prices.index,events)
average_uniqueness = get_average_uniqueness(indicator_matrix)

print(average_uniqueness.describe())
print(average_uniqueness.head())
print(average_uniqueness.tail())