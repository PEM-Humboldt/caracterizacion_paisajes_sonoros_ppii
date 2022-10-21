#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compute basic statistics about monitoring

@author: jsulloa
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dic_anh = {'ANH_64': 'ANH_064', 
           'ANH_38': 'ANH_038', 
           'ANH_99': 'ANH_099', 
           'ANH_66': 'ANH_066', 
           'ANH_58': 'ANH_058', 
           'ANH_62': 'ANH_062',
           'ANH_81': 'ANH_081', 
           'ANH_89': 'ANH_089', 
           'ANH_85': 'ANH_085',
           'ANH_95': 'ANH_095', 
           'ANH_12': 'ANH_012', 
           'ANH_69': 'ANH_069',
           'ANH_31': 'ANH_031', 
           'ANH_88': 'ANH_088', 
           'ANH_77': 'ANH_077'}

#%% Load env data
df_env = pd.read_excel('./env_data/BDPuntosMuestreoMag1012.xlsx', sheet_name='BDPuntosMuestreoMag')
df_env = df_env.loc[(df_env['GrupoBiolo'] == 'Sensores Pasivos') | (df_env['GrupoBiolo'] == 'Grabadoras'),:]
df_env = df_env.loc[:,['eventID', 'decimalLat', 'decimalLon', 'Cobertura', 'Plataf']]
df_env.eventID.replace(dic_anh, inplace=True)

#%% Load audio metadata
dft1 = pd.read_csv('../aguas_altas_t1/audio_metadata/audio_metadata_lluvias.csv')
df_dic = pd.read_csv('../aguas_altas_t1/env_data/ANH_to_GXX.csv').loc[:,['sensor_name', 'eventID']]
dft1 = dft1.merge(df_dic, on='sensor_name')
dft1.drop(columns='recorder_model', inplace=True)
dft1.rename(columns={'fname_audio': 'fname', 'sample.rate': 'sample_rate'}, inplace=True)
dft1.eventID.replace(dic_anh, inplace=True)

dft2 = pd.read_csv('../aguas_bajas_t2/audio_metadata/audio_metadata_aguas_bajas_t2.csv')
df_dic = pd.read_csv('../aguas_bajas_t2/env_data/ANH_to_GXX.csv').loc[:,['sensor_name', 'eventID']]
dft2 = dft2.merge(df_dic, on='sensor_name')
dft2.eventID.replace(dic_anh, inplace=True)

dft3 = pd.read_csv('../aguas_bajas_t3/audio_metadata/audio_metadata_aguas_bajas_t3.csv')
df_dic = pd.read_csv('../aguas_bajas_t3/env_data/ANH_to_GXX_Cobertura.csv').loc[:,['sensor_name', 'eventID']]
dft3 = dft3.merge(df_dic, on='sensor_name')
dft3.eventID.replace(dic_anh, inplace=True)

dft4 = pd.read_csv('../aguas_bajas_t4/audio_metadata/audio_metadata_aguas_bajas_t4.csv')
df_dic = pd.read_csv('../aguas_bajas_t4/env_data/ANH_to_GXX_Cobertura.csv').loc[:,['sensor_name', 'eventID']]
dft4 = dft4.merge(df_dic, on='sensor_name')
dft4.eventID.replace(dic_anh, inplace=True)

df_all = pd.concat([dft1, dft2, dft3, dft4], axis=0)
df_all.to_csv('./audio_metadata/compiled_audio_metadata.csv', index=False)


#%% Plot data by platform
df_all = df_all.merge(df_env, on='eventID')
gp = df_all.groupby('Plataf')
area = 'Caracterizacion'

plt_data = gp.get_group(area)
plt_data = pd.DataFrame(plt_data.groupby('eventID').sum()['length'])
plt_data.length = plt_data.length/60/60
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
ax.set_xlim(0,125)
ax.vlines(ax.get_xticks(), -0.5, len(plt_data), colors='white', lw=0.5)
ax.tick_params(axis='y', which='major', labelsize=8)

# set legend
labels = plt_data.Cobertura.sort_values().unique()
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
ax.legend(handles, labels, bbox_to_anchor=(0.9, .5))
sns.despine(left=True)

fig.set_tight_layout(True)
fig.savefig('./figures/esfuerzo_muestreo_caracterizacion.png')

#%% Print statistics
print('Number of recordings:')
df_all.Plataf.value_counts()

print('Length of recordings:')
plt_data.length.sum()

#%% Plot para todas las áreas
plt_data = df_all
plt_data = pd.DataFrame(plt_data.groupby('eventID').sum()['length'])
plt_data.length = plt_data.length/60/60
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
ax.vlines(ax.get_xticks(), -0.5, len(plt_data), colors='white', lw=0.5)
ax.set_xlim(0,125)
#ax.set_yticklabels('')
ax.tick_params(axis='y', which='major', labelsize=5)

# set legend
labels = plt_data.Cobertura.sort_values().unique()
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
ax.legend(handles, labels, bbox_to_anchor=(0.9, .5))
sns.despine(left=True)

fig.set_tight_layout(True)
fig.savefig('./figures/esfuerzo_muestreo_todas.png')