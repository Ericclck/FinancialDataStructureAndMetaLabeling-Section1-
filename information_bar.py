import numpy as np
import pandas as pd
import os
from utils.bars import *

ticks = pd.read_csv(os.path.join('data','ticks.csv'))
ticks.columns = ['id','price','volume','dollar','time','buyer_maker','_ignore']

# truncate to 10k rows
# ticks = ticks.iloc[:10000]

# imb = get_imbalance_dollar_bar(ticks,10)

# save to csv
# imb.to_csv(os.path.join('data/processed','ticks.csv'), index=False)

rb = get_run_dollar_bar(ticks,1000)

# save to csv
rb.to_csv(os.path.join('data/processed','ticks-run-dollars.csv'), index=False)