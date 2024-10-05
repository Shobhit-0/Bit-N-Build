import numpy as np
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
# Import specific modules from tensorflow.keras for building the model
from keras import models
from keras import layers
from tensorflow.python.keras.models import Sequential  # Sequential model for stacking layers
from tensorflow.python.keras.layers import Dense

# sklearn: Used for splitting the data into training and testing sets
from sklearn.model_selection import train_test_split
df=pd.read_csv("CV_PROJECT_DATA.csv")
df.head()
l=[]
for i in df['Date']:
    l.append(pd.to_datetime(i).month)
df['month']=pd.Series(l)

df.set_index('Date',inplace=True)
df.drop(df.columns[0],axis=1,inplace=True)


Y=[]
for i in df['Plates Used']:
    Y.append(i)
Y=np.array(Y)
X=df.drop('Plates Used',axis=1)
X_train,X_test,y_train,y_test=train_test_split(X,Y,test_size=0.2,random_state=42)
# Standardize the features manually using numpy (mean = 0, variance = 1)
# axis 0 for calculating along columns
X_train_mean = np.mean(X_train, axis=0)
X_train_std = np.std(X_train, axis=0)

# Apply standardization
X_train = np.abs(X_train - X_train_mean) / X_train_std #since X_train can come out to be negatvie so mod function used
X_test =  np.abs(X_test - X_train_mean) / X_train_std

print(X_train, len(y_train))
# Initialize a sequential model
from tensorflow.python.keras.optimizers import Adam
model = Sequential()


model.add(Dense(32, input_dim=X_train.shape[1], activation='relu'))
#adding batch dropout to make the model efficient and reduce overfitting
tf.keras.layers.Dropout(rate=0.333) 
# Hidden layer with 120 neurons
# 'relu' activation function is used again to introduce non-linearity
model.add(Dense(120, activation='relu'))
model.add(Dense(120, activation='relu'))
model.add(Dense(120, activation='relu'))
model.add(Dense(120, activation='relu'))
model.add(Dense(120, activation='relu'))
model.add(Dense(120, activation='relu'))




model.add(Dense(1, activation='relu'))
opt = Adam(learning_rate=0.01)
# Compile the model

# 'adam' is an efficient optimizer used for gradient descent optimization

model.compile(loss='mse', metrics=['mse'],optimizer=opt)
model.summary()

model.fit(X_train, y_train, epochs = 500, batch_size = 96, verbose = 1)

y_pred = model.predict(X_test)
print(len(y_pred))
x=np.arange(0,24)
plt.scatter(x=x,y=y_pred,label='predicted',marker='+',color='red')
plt.ylabel('power consumption in MW')
plt.xlabel('index')
plt.scatter(x=x,y=y_test,label='actual',alpha=0.5)
plt.legend()