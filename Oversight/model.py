import numpy as np 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Lasso

df = pd.read_csv('admission_data.csv')

x = df.drop(['Chance of Admit '], axis=1)
y = df['Chance of Admit ']
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=30, test_size=.20)

svr = SVR()
svr.fit(x_train, y_train)
svr_y_pred = svr.predict(x_test)

dt = DecisionTreeRegressor(random_state=0)
dt.fit(x_train, y_train)
dt_y_pred = dt.predict(x_test)

knn = KNeighborsRegressor(n_neighbors=5)
knn.fit(x_train, y_train)
knn_y_pred = knn.predict(x_test)

lasso = Lasso()
lasso.fit(x_train, y_train)
lasso_y_pred = lasso.predict(x_test)

svr_mse = mean_squared_error(y_test, svr_y_pred)*100
dt_mse = mean_squared_error(y_test, dt_y_pred)*100
knn_mse = mean_squared_error(y_test, knn_y_pred)*100
lasso_mse = mean_squared_error(y_test, lasso_y_pred)*100


print('SVR MSE: {:.5f}'.format(svr_mse))
print('Decision Tree MSE: {:.5f}'.format(dt_mse))
print('K-Nearest Neighbors MSE: {:.5f}'.format(knn_mse))
print('Lasso MSE: {:.5f}'.format(lasso_mse))
