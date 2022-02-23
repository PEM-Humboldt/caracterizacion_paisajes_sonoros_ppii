#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compute basic statistics about monitoring

@author: jsulloa
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#%% Load env data
df_env = pd.read_excel('../env_data/BDPuntosMuestreoMag1012.xlsx', sheet_name='BDPuntosMuestreoMag')
df_env = df_env.loc[(df_env['GrupoBiolo'] == 'Sensores Pasivos') | (df_env['GrupoBiolo'] == 'Grabadoras'),:]

#%% Load sampling points
sel_cols = ['Código grabadora (Gxxx)', 'Punto de muestreo (ANH)', 
            'Latitud/Longitud (grados decimales)', 'Presión sonora 1', 'Presión sonora 2',
            'Presión sonora 3', 'Presión sonora 4']
df_pam = pd.read_excel('../env_data/sampling_points_rain.xlsx', sheet_name='Hoja1')
df_pam = df_pam.loc[:,sel_cols]
df_pam.rename(columns={'Punto de muestreo (ANH)': 'eventID', 
                       'Código grabadora (Gxxx)': 'sensor_name'}, inplace=True)

#%% Combine
df = df_env.merge(df_pam, on='eventID')

#%% Combine to add information for each audio recording
df_audio = pd.read_csv('../audio_metadata/audio_metadata_lluvias.csv')
df_audio = df_audio.merge(df, on='sensor_name')
df_audio.to_csv('../audio_metadata/audio_metadata_lluvias_with_environmental.csv')

#%% Plot data by platform
import seaborn as sns
gp = df_audio.groupby('Plataf')
area = 'Kale'
plt_data = gp.get_group(area)
plt_data = pd.DataFrame(plt_data.groupby('sensor_name').sum()['length'])
plt_data.length = plt_data.length/60/60
plt_data = plt_data.merge(df_pam, on='sensor_name')
plt_data = plt_data.merge(df_env, on='eventID')
plt_data = plt_data.loc[:,['eventID', 'length', 'Cobertura']]
plt_data = plt_data.sort_values(['Cobertura','length'], ascending=[False, True])

colors = {'Bosque Denso': '#264653',
          'Bosque Abierto': '#2a9d8f',
          'Bosque Ripario': '#e9c46a', 
          'Palma': '#f4a261', 
          'Herbazales': '#e76f51',
          'Pastos': '#bb3e03'}

plt.close('all')
fig, ax = plt.subplots(figsize=(10,7))
ax.barh(y=plt_data.eventID, width=plt_data.length, height=0.9,
        color=[colors[i] for i in plt_data['Cobertura']])
ax.set_xlabel('Esfuerzo de muestreo (horas)')
ax.set_ylabel('Unidad de muestreo')
ax.set_title(area)
ax.set_xlim(0,18)
ax.vlines(ax.get_xticks(), -0.5, len(plt_data), colors='white', lw=0.5)
ax.tick_params(axis='y', which='major', labelsize=8)

# set legend
labels = plt_data.Cobertura.sort_values().unique()
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
ax.legend(handles, labels, bbox_to_anchor=(0.9, .5))
sns.despine(left=True)

fig.set_tight_layout(True)
fig.savefig('../figuras/esfuerzo_muestreo_caracterizacion.pdf')
fig.savefig('../figuras/esfuerzo_muestreo_caracterizacion.png')

#%% Plot para todas las áreas
plt_data = df_audio
plt_data = pd.DataFrame(plt_data.groupby('sensor_name').sum()['length'])
plt_data.length = plt_data.length/60/60
plt_data = plt_data.merge(df_pam, on='sensor_name')
plt_data = plt_data.merge(df_env, on='eventID')
plt_data = plt_data.loc[:,['eventID', 'length', 'Cobertura']]
plt_data = plt_data.sort_values(['Cobertura','length'], ascending=[False, True])

colors = {'Bosque Denso': '#264653',
          'Bosque Abierto': '#2a9d8f',
          'Bosque Ripario': '#e9c46a', 
          'Palma': '#f4a261', 
          'Herbazales': '#e76f51',
          'Pastos': '#bb3e03'}

plt.close('all')
fig, ax = plt.subplots(figsize=(10,10))
ax.barh(y=plt_data.eventID, width=plt_data.length, height=0.8,
        color=[colors[i] for i in plt_data['Cobertura']])
ax.set_xlabel('Esfuerzo de muestreo (horas)')
ax.set_ylabel('Unidad de muestreo')
ax.set_title('Todas las áreas de estudio')
ax.set_xlim(0,18)
ax.vlines(ax.get_xticks(), -0.5, len(plt_data), colors='white', lw=0.5)
#ax.set_yticklabels('')
ax.tick_params(axis='y', which='major', labelsize=5)

# set legend
labels = plt_data.Cobertura.sort_values().unique()
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
ax.legend(handles, labels, bbox_to_anchor=(0.9, .5))
sns.despine(left=True)

fig.set_tight_layout(True)
fig.savefig('../figuras/esfuerzo_muestreo_todas.pdf')
fig.savefig('../figuras/esfuerzo_muestreo_todas.png')