# -*- coding: utf-8 -*-
"""Copy of Stock Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GMKZWN-bn0-D9HQrOSxI4KRZdnwP4Zsw
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import datetime
import pandas_datareader.data as web
from pandas import Series, DataFrame

import pandas as pd
# %matplotlib inline
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score


#import packages
import pandas as pd
import numpy as np

#to plot within notebook
import matplotlib.pyplot as plt
# %matplotlib inline

#setting figure size
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 20,10

#for normalizing data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))

stock_data = pd.read_csv("AAPL.csv")
stock_data.tail()

stock_data.describe()



#setting index as date
stock_data['Date'] = pd.to_datetime(stock_data.Date,format='%Y-%m-%d')
stock_data.index = stock_data['Date']

#plot
plt.figure(figsize=(16,8))
plt.plot(stock_data['Close'], label='Close Price history')

#get nrow for training/testing
nrow = len(stock_data)
nrow

#sorting
data = stock_data.sort_index(ascending=True, axis=0)

#creating a separate dataset
new_data = pd.DataFrame(index=range(0,len(stock_data)),columns=['Date', 'Close'])

for i in range(0,len(data)):
    new_data['Date'][i] = data['Date'][i]
    new_data['Close'][i] = data['Close'][i]
    
new_data.head()

#create features (not working)
#from fastai.structured import  add_datepart
#add_datepart(new_data, 'Date')
#new_data.drop('Elapsed', axis=1, inplace=True)  #elapsed will be the time stamp

new_data['Date'] = new_data['Date'].apply(lambda x: x.strftime('%d%m%Y'))

#split into train and validation
train_nbr = nrow*(2/3)
train_nbr = int(round(train_nbr))
train = new_data[:train_nbr]
valid_nbr = nrow/3
valid_nbr = int(round(train_nbr))
valid = new_data[valid_nbr:]

x_train = train.drop('Close', axis=1)
y_train = train['Close']
x_valid = valid.drop('Close', axis=1)
y_valid = valid['Close']

valid.tail()

#implement linear regression
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(x_train,y_train)

#make predictions and find the rmse
preds = model.predict(x_valid)
rms=np.sqrt(np.mean(np.power((np.array(y_valid)-np.array(preds)),2)))
print("RMSE for Linear Regression:", rms)

#plot
valid['Predictions'] = 0
valid['Predictions'] = preds

valid.index = new_data[valid_nbr:].index
train.index = new_data[:train_nbr].index

plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])

#split into train and validation
train_nbr = nrow*(2/3)
train_nbr = int(round(train_nbr))
train_rr = new_data[:train_nbr]
valid_nbr = nrow/3
valid_nbr = int(round(train_nbr))
valid_rr = new_data[valid_nbr:]

x_train_rr = train_rr.drop('Close', axis=1)
y_train_rr = train_rr['Close']
x_valid_rr = valid_rr.drop('Close', axis=1)
y_valid_rr = valid_rr['Close']

from sklearn.linear_model import Ridge
rr = Ridge(alpha=145)
rr.fit(x_train_rr, y_train_rr)

#make predictions and find the rmse
preds_rr = rr.predict(x_valid_rr)
rms_rr=np.sqrt(np.mean(np.power((np.array(y_valid_rr)-np.array(preds_rr)),2)))
print("RMSE for Ridge Regression:", rms_rr)

#plot
valid_rr['Predictions'] = 0
valid_rr['Predictions'] = preds_rr

valid_rr.index = new_data[valid_nbr:].index
train_rr.index = new_data[:train_nbr].index

plt.plot(train_rr['Close'])
plt.plot(valid_rr[['Close', 'Predictions']])

from sklearn.linear_model import Lasso

lasso = Lasso()

lasso.fit(x_train, y_train)
#make predictions and find the rmse
preds_lasso = lasso.predict(x_valid_rr)
rms_lasso=np.sqrt(np.mean(np.power((np.array(y_valid)-np.array(preds_lasso)),2)))
print("RMSE for Lasso Regression:", rms_lasso)

print(rms , rms_rr, rms_lasso)

#plot
valid['Predictions'] = 0
valid['Predictions'] = preds_rr

valid.index = new_data[valid_nbr:].index
train.index = new_data[:train_nbr].index

plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])



