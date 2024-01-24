import numpy as np 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
import joblib

df = pd.read_csv('oversight/gradpred/model/admission_data.csv')

x = df.drop(['Chance of Admit '], axis=1)
y = df['Chance of Admit ']
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=30, test_size=.60)
svr = SVR()
fitted_model = svr.fit(x_train, y_train)

filename='gradpredmodel.sav'
joblib.dump(fitted_model,filename)