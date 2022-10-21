#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integrate soundscape composition tables
Colores 
T1 #a6cee3
T2 #1f78b4
T3 #b2df8a
T4 #33a02c

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#%% Set variables
path_global_soundscape_t1 = '../aguas_altas_t1/soundscape_composition/dataframes/presence_absence_global_components.csv'
path_detailed_soundscape_t1 = '../aguas_altas_t1/soundscape_composition/dataframes/presence_absence_detailed_components.csv'
path_global_soundscape_t2 = '../aguas_bajas_t2/soundscape_composition/dataframes/presence_absence_global_components.csv'
path_detailed_soundscape_t2 = '../aguas_bajas_t2/soundscape_composition/dataframes/presence_absence_detailed_components.csv'

dic_soundtypes = {'ALTVOZ': 'Altavoces', 
                  'MAMIFE': 'Mamíferos no voladores', 
                  'ANIDOM': 'Animales domésticos', 
                  'FLUAGU': 'Flujo agua', 
                  'LLUVIA': 'Lluvia', 
                  'MURCIE': 'Murciélagos',
                  'HERPET': 'Anuros', 
                  'TRAMOT': 'Transporte motorizado', 
                  'AVEVOC': 'Aves', 
                  'INSECT': 'Insectos'}

#path_env_data = '../env_data/ANH_to_GXX_Cobertura.csv'
#df_env = pd.read_csv(path_env_data)
#df_env = df_env[['sensor_name', 'Cobertura']]

#%% Proporciones general
df_t1 = pd.read_csv(path_global_soundscape_t1)
df_t2 = pd.read_csv(path_global_soundscape_t2)
df_mix_global = pd.concat([df_t1,df_t2])

df_prop = df_mix_global.loc[:,['ANT', 'BIO', 'GEO']].mean(axis=0) * 100
print('Proporción media de cada uno de los componentes principales\n', df_prop.round(2))

df_id_t1 = pd.read_csv(path_detailed_soundscape_t1)
df_id_t2 = pd.read_csv(path_detailed_soundscape_t2)
df_mix_id = pd.concat([df_id_t1,df_id_t2])
df_mix_id.fillna(0, inplace=True)

df_prop_id = df_mix_id.drop(columns=['fname']).mean(axis=0) * 100
print('Proporción media de cada uno de los componentes principales\n', df_prop.round(2))


# Plot
sel_id = ['ALTVOZ', 'ANIDOM', 'TRAMOT', 'LLUVIA', 'FLUAGU', 'MAMIFE', 'HERPET', 
          'MURCIE', 'AVEVOC', 'INSECT']
plt_data = df_prop_id.loc[sel_id]
plt_data.rename(index=dic_soundtypes, inplace=True)
color = np.concatenate([np.repeat('#CD6155', 3), np.repeat('#2E86C1', 2), np.repeat('#229954', 5)])

fig, ax = plt.subplots(figsize=(8,5))
ax.scatter(x=plt_data, y=plt_data.index, color=color)
ax.hlines(plt_data.index, xmin=0, xmax=plt_data, colors=color)
for name, value in plt_data.items():
    ax.text(x=value+2, y=name, s=np.round(value,1), color='gray')

ax.set_xlabel('Proporción (%)')
ax.set_xlim([0,100])
sns.despine(ax=ax, trim=True)
plt.grid(linestyle=':', axis='x')
fig.set_tight_layout('tight')


#%% Proporciones general - Cobertura
sel_id = ['ALTVOZ', 'ANIDOM', 'TRAMOT', 'LLUVIA', 'FLUAGU', 'MAMIFE', 'HERPET', 
          'MURCIE', 'AVEVOC', 'INSECT']

df_env = pd.read_csv('../aguas_altas_t1/env_data/ANH_to_GXX.csv')
df_env = df_env[['sensor_name', 'Cobertura']]
df_t1 = pd.read_csv('../aguas_altas_t1/soundscape_composition/dataframes/annotations_compiled.csv')
df_id = pd.crosstab(index=df_t1['fname'], columns=df_t1['Id'])
df_id = (df_id>0).astype(int)
df_id = df_id.loc[:,sel_id]
df_id['sensor_name'] = df_id.index.str[0:4]
df_id.reset_index(inplace=True)
df_id = df_id.merge(df_env, on='sensor_name')
df_id = df_id.groupby('sensor_name').mean()
df_id.reset_index(inplace=True)
df_id_t1 = df_id.merge(df_env, on='sensor_name')

df_env = pd.read_csv('../aguas_bajas_t2/env_data/ANH_to_GXX_Cobertura.csv')
df_env = df_env[['sensor_name', 'Cobertura']]
df_t2 = pd.read_csv('../aguas_bajas_t2/soundscape_composition/dataframes/annotations_compiled.csv')
df_id = pd.crosstab(index=df_t2['fname'], columns=df_t2['Id'])
df_id = (df_id>0).astype(int)
df_id = df_id.loc[:,sel_id]
df_id['sensor_name'] = df_id.index.str[0:4]
df_id.reset_index(inplace=True)
df_id = df_id.merge(df_env, on='sensor_name')
df_id = df_id.groupby('sensor_name').mean()
df_id.reset_index(inplace=True)
df_id_t2 = df_id.merge(df_env, on='sensor_name')

df_id = pd.concat([df_id_t1, df_id_t2])

# plot
plt_data = df_id.groupby('Cobertura').mean().T
plt_data.rename(index=dic_soundtypes, inplace=True)
plt_data = plt_data.reindex(plt_data.sum(axis=1).sort_values().index)
fig, ax = plt.subplots(figsize=(10,5.5))
sns.heatmap(plt_data, annot=True, ax=ax, cbar_kws={'label': 'Proporción'})
fig.set_tight_layout('tight')

fig, ax = plt.subplots(figsize=(10,5.5))
sns.clustermap(plt_data, annot=True, cbar_kws={'label': 'Proporción'}, 
               metric='euclidean',
               method='average',
               figsize=(10,8))
fig.set_tight_layout('tight')


#%% Cambio de proporciones entre temporadas

df_id_t1 = pd.read_csv(path_detailed_soundscape_t1)
df_id_t2 = pd.read_csv(path_detailed_soundscape_t2)


sel_id = ['ALTVOZ', 'ANIDOM', 'AVEVOC', 'FLUAGU', 'HERPET', 'INSECT', 'LLUVIA', 
          'MAMIFE', 'MURCIE', 'TRAMOT']

df_prop_t1 = df_id_t1.loc[:,sel_id].mean(axis=0) * 100
df_prop_t2 = df_id_t2.loc[:,sel_id].mean(axis=0) * 100

df_prop = pd.DataFrame({'t1': df_prop_t1, 't2': df_prop_t2})
df_prop.rename(index=dic_soundtypes, inplace=True)
df_prop.sort_values('t1', inplace=True)

fig, ax = plt.subplots(figsize=(8,5))
for idx, row in df_prop.iterrows():
    ax.hlines(idx, row.t1, row.t2, color='gray', linewidth=0.5)
    scat1 = ax.scatter(row.t1, idx, color='#a6cee3', label='T1')
    scat2 = ax.scatter(row.t2, idx, color='#1f78b4', label='T2')

ax.legend([scat1,scat2], ['T1', 'T2'], loc='lower right')
ax.set_xlabel('Proporción (%)')
sns.despine(ax=ax, trim=True)
plt.grid(linestyle=':', axis='x')
fig.set_tight_layout('tight')
plt.savefig('./figures/cambio_proporciones_t1-t2.png')


#%% Spectral distribution

# load data
df_t1 = pd.read_csv('../aguas_altas_t1/soundscape_composition/dataframes/annotations_compiled.csv')
df_t2 = pd.read_csv('../aguas_bajas_t2/soundscape_composition/dataframes/annotations_compiled.csv')
df = pd.concat([df_t1.drop(columns=['Feeding buzz']),
                   df_t2.drop(columns=['Comportamiento', 'Calidad'])])

df = df.loc[df.Tipo.isin(['BIO', 'ANT', 'GEO']),:]
df.reset_index(inplace=True, drop=True)
df['Componente'] = df.Tipo.replace({'BIO': 'Biofonía',
                                    'GEO': 'Geofonía',
                                    'ANT': 'Antropofonía'})

df_bio = df.loc[df.Tipo=='BIO',:]
df_bio = df_bio.loc[df.Id.isin(['INSECT', 'AVEVOC', 'HERPET', 'MURCIE', 'MAMIFE']),:]
df_bio['Grupo taxonómico'] = df_bio.Id.replace({'INSECT': 'Insectos', 
                                                'AVEVOC': 'Aves', 
                                                'HERPET': 'Herpetos', 
                                                'MURCIE': 'Murciélagos', 
                                                'MAMIFE': 'Mamíferos no-voladores'})

# Plot
color = {'Biofonía': '#229954', 
         'Antropofonía': '#CD6155', 
         'Geofonía': '#2E86C1'}

plt.close('all')
fig, ax = plt.subplots(2,1, figsize=(8,10))
sns.kdeplot(x='Center Freq (Hz)', hue='Componente', fill=True, alpha=0.2, 
            bw_adjust=0.7, clip=[0, 80000], ax=ax[0], palette=color, data=df)
ax[0].set_xlabel('Frecuencia (Hz)')
ax[0].set_ylabel('Densidad')
sns.despine(trim=True, ax=ax[0])

sns.kdeplot(x=df_bio['Center Freq (Hz)'], hue=df_bio['Grupo taxonómico'], fill=True, alpha=0.4, 
            palette='Set2', bw_adjust=0.7, clip=[0, 80000], ax=ax[1])
ax[1].set_xlabel('Frecuencia (Hz)')
ax[1].set_ylabel('Densidad')
sns.despine(trim=True, ax=ax[1])

# save data
pd.crosstab(df.Determinacion, df.Id).sort_values('AVEVOC').to_csv('./dataframes/species.csv')
# sns.histplot(x=df['Center Freq (Hz)'], hue=df['Tipo'], fill=True, alpha=0.5, stat='percent', element='poly')