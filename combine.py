import pandas as pd
import numpy as np

# combine any csv files in data folder started with "BTCUSDT"
# and save to data folder
def combine_csv():
    import os
    import glob
    os.chdir("data")
    extension = 'csv'
    all_filenames = [i for i in glob.glob('BTCUSDT*.{}'.format(extension))]
    # set columns to ['id','price','volume','dollar','time','buyer_maker','_ignore'] in read_csv
    combined_csv = pd.concat([pd.read_csv(f,names=['id','price','volume','dollar','time','buyer_maker','_ignore']) for f in all_filenames ])
    # order columns according to id
    combined_csv = combined_csv.sort_values(by=['id'])
    combined_csv.to_csv( "ticks.csv", index=False, encoding='utf-8-sig')
    os.chdir("..")

combine_csv()

# check if ticks.csv id is in order
def check_ticks_id():
    ticks = pd.read_csv('data/ticks.csv')
    ticks.columns = ['id','price','volume','dollar','time','buyer_maker','_ignore']
    print((ticks['id'].diff()<0).sum())
    print((ticks['time'].diff()<0).sum())

check_ticks_id()
