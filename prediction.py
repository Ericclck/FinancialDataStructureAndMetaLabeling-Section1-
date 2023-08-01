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

# import ticks data
ticks = pd.read_csv(os.path.join('data','BTCUSDT-trades-2023-06-16.csv'))
ticks.columns = ['id','price','volume','dollar','time','buyer_maker','_ignore']
ticks = ticks.set_index('id')

# compute stds
ewma_window = 100
stds = std_pct_change(ticks['price'].values, ewma_window)
stds = pd.Series(stds,index=ticks.index[ewma_window:],name='volatility')

# import run bars data
rb = pd.read_csv(os.path.join('data/processed','BTCUSDT-trades-2023-06-16-run-dollars.csv'))
rb.set_index('id',inplace=True)

# compute log return series for each columns (open,high,low,close,volume), remove inf values and nan values
rb['log_price'] = np.log(rb['close']).diff()
rb['log_volume'] = np.log(rb['volume']).diff()
rb['log_high'] = np.log(rb['high']).diff()
rb['log_low'] = np.log(rb['low']).diff()
rb['log_open'] = np.log(rb['open']).diff()
rb = rb.replace([np.inf, -np.inf], np.nan).dropna()

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
df = df.merge(trend_following,left_index=True,right_index=True)
df = df.merge(stds,left_index=True,right_index=True)

# save df to csv
# df.to_csv(os.path.join('data/processed','df.csv'), index=True)

# df columns : return,label,meta_label , index = id
# split data, 80% train, 20% test, maintain order
inputs_columns = ['log_price','log_volume','log_high','log_low','log_open','volatility','side']
X = df[inputs_columns+['return','label']]
y = df['meta_label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# train random forest model
rf = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0,oob_score=True)
rf.fit(X_train[inputs_columns], y_train)

# predict on test set
y_pred = rf.predict(X_test[inputs_columns])

# # accuracy score
print(accuracy_score(y_test, y_pred))

# confusion matrix
print("Confusion matrix of primary model : \n" , confusion_matrix(y_test, X_test['side'].replace(-1,0)))
print("Confusion matrix of secondary model : \n" , confusion_matrix(y_test, y_pred))

# classification report
print(classification_report(y_test, y_pred))

# feature importance
print(rf.feature_importances_)

y_pred_proba = rf.predict_proba(X_test[inputs_columns])
return_series = pd.Series(y_pred_proba[:,1]*X_test['return']*X_test['side'])

print(return_series.describe())