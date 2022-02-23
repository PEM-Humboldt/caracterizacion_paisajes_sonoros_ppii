#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Use a machine learning approach to identify which acoustic index is more important to
discriminate between landscape cover.

env_cover ~ acoustic_indices


"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

#%% Load data
df_env = pd.read_csv('../../env_data/ANH_to_GXX.csv')
df_env = df_env[['sensor_name', 'Cobertura']]
df_rain = pd.read_csv('../../detection/rain_predictions.csv')

#%% Load acoustic indices -- mean hour
indices_names = ['ACI', 'ADI', 'BI', 'H', 'Hf', 'Ht', 'NDSI', 'NP', 'SC']
feature_names = indices_names * 24
# load indices data
flist = glob.glob('../acoustic_indices/dataframes/per_site/*.csv')
df_indices = pd.DataFrame()
for fname in flist:
    df_site = pd.read_csv(fname)
    df_site['time'] = df_site.date.str[11:13].astype(int)
    aux = df_site.groupby('time').mean()
    df_indices = df_indices.append(pd.Series(aux.values.ravel(),  
                                             name=df_site.sensor_name[0]))

df_indices.reset_index(inplace=True)
df_indices.rename(columns={'index': 'sensor_name'}, inplace=True)

# merge acoustic indices and spatial cover
df_indices = df_indices.merge(df_env, on='sensor_name')
df_indices = df_indices.loc[df_indices.Cobertura.isin(['Palma', 'Bosque Ripario', 'Herbazales']),:]
X = df_indices.loc[:,0:215]
y = df_indices.Cobertura

#%% Build model
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import confusion_matrix, classification_report

clf = RandomForestClassifier(n_estimators=300, random_state=123)
clf.fit(X, y)
y_pred = cross_val_predict(clf, X, y, cv=10)
print(classification_report(y, y_pred))
feature_importance = clf.feature_importances_

#%% Plot data
import seaborn as sns


plt_data = pd.DataFrame({'fimp': feature_importance, 
                         'Indices acústicos': feature_names,
                         'Tiempo (h)' : np.repeat(np.arange(24), 9)})
plt_data = plt_data.pivot('Indices acústicos', 'Tiempo (h)', 'fimp')

fig, ax = plt.subplots(1, 2, figsize=(10,6))
ax[0].bar(plt_data.sum(axis=1).index, plt_data.sum(axis=1))
ax[0].set_ylabel('Disminución media de la precisión del modelo')
ax[0].set_xlabel('Indices acústicos')
ax[0].grid(color='w', axis='y', linewidth=0.5)
sns.heatmap(plt_data, cmap='viridis', linewidths=.5, ax=ax[1])
fig.tight_layout()
