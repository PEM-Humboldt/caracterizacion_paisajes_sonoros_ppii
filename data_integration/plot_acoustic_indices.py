#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot acoustic indices

@author: jsulloa
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob

#%% Load data
df = pd.read_csv('./dataframes/compiled_acoustic_indices.csv')

#
df_gp = df.groupby(['eventID', 'season']).mean()

#%% single site
plt_data = df.loc[df.eventID=='ANH_064']

plt.close('all')
fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(10, 10))
sns.regplot(data=plt_data, x='time', y='ACI', order=6, scatter=False, ax=ax[0,0])
sns.regplot(data=plt_data, x='time', y='ADI', order=6, scatter=False, ax=ax[0,1])
sns.regplot(data=plt_data, x='time', y='BI', order=6, scatter=False, ax=ax[0,2])
sns.regplot(data=plt_data, x='time', y='H', order=6, scatter=False, ax=ax[1,0])
sns.regplot(data=plt_data, x='time', y='Ht', order=6, scatter=False, ax=ax[1,1])
sns.regplot(data=plt_data, x='time', y='Hf', order=6, scatter=False, ax=ax[1,2])
sns.regplot(data=plt_data, x='time', y='NDSI', order=6, scatter=False, ax=ax[2,0])
sns.regplot(data=plt_data, x='time', y='NP', order=6, scatter=False, ax=ax[2,1])
sns.regplot(data=plt_data, x='time', y='SC', order=6, scatter=False, ax=ax[2,2])
fig.set_tight_layout('tight')

#%% multiple sites

# remove rain days
df = df.loc[df.proba_rain<0.5,:]

# load colors
colors = {'Palma': '#66A61E',
          'Herbazales': '#E7298A',
          'Bosque Ripario': '#7570B3',
          'Pastos': '#E6AB02',
          'Bosque Denso': '#D95F02',
          'Bosque Abierto': '#1B9E77'}

#%% plot
plt.close('all')
fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(10, 10))
covers = df.Cobertura.unique()
for cover in covers:
    df_sel = df.loc[df.Cobertura==cover,:]
    sns.regplot(data=df_sel, x='time', y='ACI', order=6, scatter=False, color=colors[cover], ax=ax[0,0])
    sns.regplot(data=df_sel, x='time', y='ADI', order=6, scatter=False, color=colors[cover], ax=ax[0,1])
    sns.regplot(data=df_sel, x='time', y='BI', order=6, scatter=False, color=colors[cover], ax=ax[0,2])
    sns.regplot(data=df_sel, x='time', y='H', order=6, scatter=False, color=colors[cover], ax=ax[1,0])
    sns.regplot(data=df_sel, x='time', y='Ht', order=6, scatter=False, color=colors[cover], ax=ax[1,1])
    sns.regplot(data=df_sel, x='time', y='Hf', order=6, scatter=False, color=colors[cover], ax=ax[1,2])
    sns.regplot(data=df_sel, x='time', y='NDSI', order=6, scatter=False, color=colors[cover], ax=ax[2,0])
    sns.regplot(data=df_sel, x='time', y='NP', order=6, scatter=False, color=colors[cover], ax=ax[2,1])
    sns.regplot(data=df_sel, x='time', y='SC', order=6, scatter=False, color=colors[cover], ax=ax[2,2])

# arrange axes
for idx, ax_aux in enumerate(ax.ravel()):
    ax_aux.set_xticks([0, 6, 12, 18, 24])
    if idx >=6:
        ax_aux.set_xlabel('Time')
    else:
        ax_aux.set_xlabel('')


plt.subplots_adjust(left=0.125, right=0.9, bottom=0.2, top=0.95, wspace=0.35, hspace=0.2)
fig.legend(colors, loc ='lower center')
