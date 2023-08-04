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

# import prices 
prices = pd.read_csv(os.path.join('data','ticks.csv'))
prices.columns = ['id','price','volume','dollar','time','buyer_maker','_ignore']
prices = prices.set_index('id')

# import rb
rb = pd.read_csv(os.path.join('data/processed','ticks-run-dollars.csv'))
rb.set_index('id',inplace=True)

df = pd.read_csv(os.path.join('data/processed','df.csv'),index_col=0)

# ffill nans then bfill nans
df = df.fillna(method='ffill').fillna(method='bfill')

# df columns : return,label,meta_label , index = id
# split data, 80% train, 20% test, maintain order
inputs_columns = ['log_price','log_volume','log_high','log_low','log_open','volatility','side']
fractional_diff_columns = ['fracdiff_close','fracdiff_high','fracdiff_low','fracdiff_open','fracdiff_volume']
X = df[inputs_columns+['return','label']+fractional_diff_columns]
y = df['meta_label']

# split at 0.8
X_train = X[X.index < prices.index[int(0.8*len(prices.index))]]
X_test = X[X.index >= prices.index[int(0.8*len(prices.index))]]
y_train = y[y.index < prices.index[int(0.8*len(prices.index))]]
y_test = y[y.index >= prices.index[int(0.8*len(prices.index))]]



n_estimators = 1000
max_depth = 10
visualize_model(X_train, y_train, X_test, y_test, inputs_columns,model=RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=0))

# get sample weights
sample_weights = pd.read_csv(os.path.join('data/processed','final_weights.csv'),index_col=0).squeeze()

print(f"Sample mean : {sample_weights.mean()}")

# truncate sample weights with indices of X_train
sample_weights = sample_weights[X_train.index]

print(f"Sample mean in Train : {sample_weights.mean()}")

y_pred = bagging(X_train, y_train, X_test, y_test, inputs_columns,None, sample_weights,parameters={'n_estimators':n_estimators,'max_depth':max_depth})
return_series = y_pred * X_test['side'] * X_test['return']

print(return_series.describe())

y_pred = bagging(X_train, y_train, X_test, y_test, fractional_diff_columns+['volatility','side'],None, sample_weights,parameters={'n_estimators':n_estimators,'max_depth':max_depth})
return_series = y_pred * X_test['side'] * X_test['return']
print(return_series.describe())

