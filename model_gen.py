import pandas                  as pd
import numpy                   as np
import matplotlib.pyplot       as plt
import seaborn                 as sns
import statsmodels.api         as sm
import statsmodels.formula.api as smf
import os
from util import *

from scipy import stats

dsname = 'Allstate-cost-cleaned.csv'
data = df_original = load_data(dsname)

df = df_original.copy()

df_encoded = preprocess_data(df_original)

# REMOVING REDUNDANT
numerical = df_encoded.drop(df_encoded.select_dtypes(exclude=["number"]).columns, axis=1)
redundant = ["A_0", "B_0", "E_0", "F_0"]
numerical_non_redundant = numerical.drop(redundant, axis=1)

train, test=split_data(numerical_non_redundant,1337, 0.8) 

cost_tr = train['cost']
cost_tt = test['cost']

train = train.drop('cost', axis=1)
test = test.drop('cost', axis=1)

# Boxcox
tr_fitted_data, tr_fitted_lambda = stats.boxcox(cost_tr)
tt_fitted_data, tt_fitted_lambda = stats.boxcox(cost_tt)

train['cost'] = tr_fitted_data
test['cost'] = tt_fitted_data

def train_model(datatr, fts, depvar):
    # Boxcox
    # fitted_data, fitted_lambda = stats.boxcox(depvar) 
    # datatr['cost'] = tr_fitted_data
    datatr['cost'] = depvar
    
    Xtr = datatr[fts]
    
    Ytr = tr_fitted_data
    
    Xtr = sm.add_constant(Xtr)
    
    mrnobx = sm.OLS(Ytr, Xtr).fit()
    return mrnobx

# FIFTH MODEL, BOX COX
all_fts = list(train.columns[train.columns != "cost"])
# all_fts = list(datatr.columns[datatr.columns != "cost"])

Xtt = test[all_fts]
Ytt = tt_fitted_data
Xtt = sm.add_constant(Xtt)

model = train_model(train, all_fts,cost_tr)
print("SUMMARY: ")
print(model.summary())
print("PREDICTIONS: ")
print(model.predict(Xtt))

