#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot:
    - graphical soundscapes per site
    - mean graphical soundscapes per cover
    - indicator species

@author: jsulloa
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

#%% Single plot

df = pd.read_csv('./dataframes/G001.csv')
fig, ax = plt.subplots()
ax.imshow(df.drop(columns='hour').T, aspect='auto', origin='lower', extent=[0, 24, 0, 24])
ax.set_xticks([0, 6, 12, 18, 24])

plt_data = df.drop(columns='hour').values.ravel()
fig, ax = plt.subplots()
ax.imshow(plt_data.reshape([24, 128]).T, aspect='auto', origin='lower', extent=[0, 24, 0, 24])
ax.set_xticks([0, 6, 12, 18, 24])

#%% Multiple plots by cover

# load env data
df_env = pd.read_csv('../../env_data/ANH_to_GXX_Cobertura.csv')
df_env = df_env[['sensor_name', 'Cobertura']]

# load indices data
flist = glob.glob('./dataframes/*.csv')
df = pd.DataFrame()
for fname in flist:
    aux = pd.read_csv(fname)
    aux.drop(columns='hour', inplace=True)
    aux = pd.Series(aux.values.ravel(), name=fname[13:17])
    df = df.append(aux)

plt_data = df.mean().values

# merge acoustic indices and spatial cover
df.reset_index(inplace=True)
df.rename(columns={'index': 'sensor_name'}, inplace=True)
df = df.merge(df_env, on='sensor_name')
df_aggregated = df.groupby('Cobertura').mean()

# plot
plt.close('all')
fig, ax = plt.subplots(nrows=3, ncols=2, sharex=True, sharey=True, figsize=(8, 10))
ax = ax.ravel()
for i, (idx, row) in enumerate(df_aggregated.iterrows()):
    plt_data = row.values
    pos = ax[i].imshow(plt_data.reshape([24, 128]).T, aspect='auto', origin='lower', 
                       extent=[0, 24, 0, 24])
    ax[i].set_xticks([0, 6, 12, 18, 24])
    ax[i].set_title(idx)

fig.text(0.5, 0.04, 'Time (h)', ha='center')
fig.text(0.04, 0.5, 'Frequency (kHz)', va='center', rotation='vertical')

# add colorbar
fig.subplots_adjust(right=0.85)
cbar_ax = fig.add_axes([0.9, 0.15, 0.02, 0.7])
cbar_ax.set_xlabel('Z')
fig.colorbar(pos, cax=cbar_ax)

#%% Plot indicator species

df_ind = pd.read_csv('./indicator_species_data/indval.csv')
idx_names = ['V' + str(idx) for idx in np.arange(1, 3072+1)]

plt.close('all')
fig, ax = plt.subplots(nrows=2, ncols=2, sharey=True, figsize=(8, 8))
ax = ax.ravel()
for ax_idx, (group_name, df_cover) in enumerate(df_ind.groupby('group')):
    plt_data = pd.Series(data=np.zeros(3072), index=idx_names)    
    for idx, row in df_cover.iterrows():
        plt_data[row.tf_bin] = row.indval #0.05 - row.pvalue
    
    pos = ax[ax_idx].imshow(plt_data.values.reshape([24, 128]).T, 
                            aspect='auto', origin='lower', extent=[0, 24, 0, 24],
                            vmin=0, vmax=0.7)
    ax[ax_idx].set_xticks([0, 6, 12, 18, 24])
    ax[ax_idx].set_title(group_name)

fig.delaxes(ax[3])
fig.text(0.5, 0.04, 'Tiempo (h)', ha='center')
fig.text(0.04, 0.5, 'Frecuencia (kHz)', va='center', rotation='vertical')

# add color bar
cbar_ax = fig.add_axes([0.65, 0.1, 0.02, 0.35])
cbar = fig.colorbar(pos, cax=cbar_ax)
cbar.set_ticks([0, 0.35, 0.7])
cbar_ax.set_ylabel('Valor indicador')
cbar_ax.yaxis.set_label_position('left')
