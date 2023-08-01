import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from utils.bars import *

ticks = pd.read_csv(os.path.join('data','BTCUSDT-trades-2023-06-16.csv'))

# name the columns by id,price,volume,dollar,time,buyer_maker,_ignore
ticks.columns = ['id','price','volume','dollar','time','buyer_maker','_ignore']

tick_bars = get_tick_bar(ticks, 10)
# print(tick_bars.tail())
# # plot close price
# tick_bars['close'].plot()
# plt.show()

volume_bars = get_volume_bar(ticks, 1)
# # print(volume_bars['volume'].mean())
# # print(volume_bars['volume'].median())
# # volume_bars['volume'].plot()
# # plt.show()

dollar_bar = get_dollar_bar(ticks, 1000)

# save to csv in data/processed
tick_bars.to_csv(os.path.join('data/processed','BTCUSDT-trades-2023-06-16-tick-bars.csv'), index=False)
volume_bars.to_csv(os.path.join('data/processed','BTCUSDT-trades-2023-06-16-volume-bars.csv'), index=False)
dollar_bar.to_csv(os.path.join('data/processed','BTCUSDT-trades-2023-06-16-dollar-bars.csv'), index=False)