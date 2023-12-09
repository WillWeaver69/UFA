import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
from ISLP import load_data, confusion_table
from ISLP.models import ModelSpec as MS
from sklearn.naive_bayes import GaussianNB


#Data Preparation
Smarket = load_data('Smarket')
allvars = Smarket.columns.drop(['Today','Direction','Year'])
design = MS(allvars)
X = design.fit_transform(Smarket)
y = Smarket.Direction == 'Up'

# Splitting the dataset into training and testing sets
train = (Smarket.Year < 2005)
Smarket_train = Smarket.loc[train]
Smarket_test = Smarket.loc[~train]
Smarket_test.shape

X_train, X_test = X.loc[train], X.loc[~train]
y_train, y_test = y.loc[train], y.loc[~train]
D = Smarket.Direction
L_train, L_test = D.loc[train], D.loc[~train]
model = MS(['Lag1', 'Lag2']).fit(Smarket)
X = model.transform(Smarket)
X_train, X_test = X.loc[train], X.loc[~train]
X_train, X_test = [M.drop(columns=['intercept']) for M in [X_train, X_test]]

#Instantiate and Train the model
NB = GaussianNB()
NB.fit(X_train, L_train)

#Evaluate the model
nb_labels = NB.predict(X_test)
confusion_table(nb_labels, L_test)
