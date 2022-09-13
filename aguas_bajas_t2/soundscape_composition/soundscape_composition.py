#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Read manual annotations and evaluate trends in composition accross cover types


"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import seaborn as sns
import numpy as np

dic_soundtypes = {'ALTVOZ': 'Altavoces', 
                  'MAMIFE': 'Mamíferos no voladores', 
                  'ANIDOM': 'Animales domésticos', 
                  'FLUAGU': 'Flujo agua', 
                  'LLUVIA': 'Lluvia', 
                  'MURCIE': 'Murciélagos',
                  'HERPET': 'Herpetos', 
                  'TRAMOT': 'Transporte motorizado', 
                  'AVEVOC': 'Aves', 
                  'INSECT': 'Insectos',
                  'SONIND': 'Sonido industria',
                  'SONVIE': 'Viento',
                  'VOZHUM': 'Voz humana'}

dic_sound_categories = {
                        'FLUAGU': 'GEO',
                        'SONVIE': 'GEO',
                        'LLUVIA': 'GEO',
                        'HERPET': 'BIO',
                        'INSECT': 'BIO',
                        'AVEVOC': 'BIO',
                        'MAMIFE': 'BIO',
                        'MURCIE': 'BIO',
                        'ANIDOM': 'ANT',
                        'ALTVOZ': 'ANT',
                        'TRAMOT': 'ANT',
                        'VOZHUM': 'ANT',
                        'SONIND': 'ANT'}

#%% Load manual annotations
fpath = '../manual_annotations/annot_random_flist/*.txt'

# A dictionary with all typo error that will allow to standardize column names
rename_col_dict = {'ID': 'Id',
                   'Determinaci�n': 'Determinacion',
                   'Determinacin': 'Determinacion',
                   'DETERMINACION': 'Determinacion',
                   'Determianci�n': 'Determinacion',
                   'Determimaci�n': 'Determinacion',
                   'Determinanci�n': 'Determinacion',
                   'DETERMINACI�N': 'Determinacion',
                   'DESCRIPCION': 'Determinacion',
                   'Descripci�n': 'Determinacion',
                   'Descripcion': 'Determinacion',
                   'TIPO': 'Tipo',
                   'Fedding buzz': 'Feeding buzz',
                   'Feeding Buzz': 'Feeding buzz'}

df = pd.DataFrame()
flist_annot = glob.glob(fpath)
for fname_annot in flist_annot:
    df_aux = pd.read_csv(fname_annot, sep='\t', encoding_errors='ignore')
    # rename columns to standard name
    df_aux.rename(columns=rename_col_dict, inplace=True)
    # remove rows with NaN and Waveform View
    df_aux = df_aux.loc[df_aux.View=='Spectrogram 1',:]
    #df_aux = df_aux.loc[df_aux.Id.notna(),:]
    df_aux.drop(columns=['Selection', 'View', 'Channel'], inplace=True)
    # add fname column
    df_aux['fname'] = os.path.basename(fname_annot).replace('.txt', '.WAV')
    df_aux['fname_annot'] = os.path.basename(fname_annot)
    df_aux['sensor_name'] = os.path.basename(fname_annot)[0:4]
    # append
    df = df.append(df_aux)

df.reset_index(inplace=True, drop=True)


#%%Get proportion of components
# Get general overview of the data without separating into land covers

df_prop = pd.crosstab(index=df['fname'], columns=df['Tipo'])
df_prop = (df_prop>0).astype(int)
df_prop = df_prop.drop(columns=['INDETE', 'PULSOS'])
prop_soundscape = df_prop.sum(axis=0)/len(df_prop) * 100
print('Proporción media de cada uno de los componentes principales\n', prop_soundscape.round(2))

df_prop_id = pd.crosstab(index=df['fname'], columns=df['Id'])
df_prop_id = (df_prop_id>0).astype(int)
prop_soundscape_id = df_prop_id.sum(axis=0)/len(df_prop) * 100
print('Proporción media de cada uno de los componentes principales\n', 
      prop_soundscape_id.round(2).sort_values())

plt_data = prop_soundscape_id.drop(['HERRAM', 'PULSOS', 'INDETE', 'SENSAT'])
plt_data = pd.DataFrame(plt_data, columns=['Prop'])
plt_data['Tipo'] = plt_data.rename(index=dic_sound_categories).index.values
plt_data['Tipo 2'] = plt_data.rename(index=dic_soundtypes).index.values
plt_data = plt_data.sort_values(by=['Tipo', 'Prop'])
plt_data['color'] = np.concatenate([np.repeat('#CD6155', 5), np.repeat('#229954', 5), np.repeat('#2E86C1', 3)])
plt_data.reset_index(inplace=True)

fig, ax = plt.subplots(figsize=(8,5))
for idx, row in plt_data.iterrows():
    ax.scatter(row.Prop, idx, color=row.color)
    ax.text(x=row.Prop+2, y=idx-0.15, s=np.round(row.Prop,1), color=row.color)

ax.hlines(plt_data['Tipo 2'], xmin=0, xmax=plt_data['Prop'], colors=plt_data.color)
ax.set_xlabel('Proporción (%)')
sns.despine(ax=ax, trim=True)
plt.grid(linestyle=':', axis='x')
fig.set_tight_layout('tight')

#%% Save dataframes for posterior analysis
df.to_csv('../manual_annotations/annot_random_sampling_consolidado.csv')
df_prop.to_csv('./dataframes/presence_absence_global_components.csv')
df_prop_id.to_csv('./dataframes/presence_absence_detailed_components.csv')

#%% Get proportion of sound types for each site and each land cover
df_env = pd.read_csv('../env_data/ANH_to_GXX_Cobertura.csv')
df_env = df_env[['sensor_name', 'Cobertura']]

#%% Get proportion of presence by Id
df_id = pd.crosstab(index=df['fname'], columns=df['Id'])
df_id = (df_id>0).astype(int)
df_id['sensor_name'] = df_id.index.str[0:4]
df_id.reset_index(inplace=True)
df_id = df_id.merge(df_env, on='sensor_name')
df_id = df_id.groupby('sensor_name').mean()
df_id.reset_index(inplace=True)
df_id = df_id.merge(df_env, on='sensor_name')

# plot
plt_data = df_id.groupby('Cobertura').mean().T
plt_data.drop(index=['HERRAM', 'INDETE', 'PULSOS', 'SENSAT', 'INDETE'], inplace=True)
plt_data.rename(index=dic_soundtypes, inplace=True)
plt_data = plt_data.reindex(plt_data.sum(axis=1).sort_values().index)

# fig soundscape composition
fig, ax = plt.subplots(figsize=(10,5.5))
sns.heatmap(plt_data, annot=True, ax=ax, cbar_kws={'label': 'Proporción'})
fig.set_tight_layout('tight')

# fig soundscape composition cluster
sns.clustermap(plt_data, annot=True, cbar_kws={'label': 'Proporción'}, 
               metric='euclidean',
               method='average',
               figsize=(10,8))
fig.set_tight_layout('tight')

#%% Get proportion of presence by Id
df_tipo = pd.crosstab(index=df['fname'], columns=df['Tipo'])
df_tipo = (df_tipo>0).astype(int)
df_tipo['sensor_name'] = df_tipo.index.str[0:4]
df_tipo.reset_index(inplace=True)
df_tipo = df_tipo.merge(df_env, on='sensor_name')
df_tipo = df_tipo.groupby('sensor_name').mean()
df_tipo.reset_index(inplace=True)
df_tipo = df_tipo.merge(df_env, on='sensor_name')
df_tipo = df_tipo.drop(columns=['INDETE', 'PULSOS'])

# plot
plt_data = df_tipo.groupby('Cobertura').mean().T
plt_data.rename(index={'BIO': 'Biofonía', 'ANT': 'Antropofonía', 'GEO': 'Geofonía'}, inplace=True)
plt_data = plt_data.reindex(plt_data.sum(axis=1).sort_values().index)
fig, ax = plt.subplots(figsize=(10,5.5))
sns.heatmap(plt_data, annot=True, ax=ax, cbar_kws={'label': 'Proporción'})
fig.set_tight_layout('tight')

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10,8))
sns.heatmap(plt_data, annot=True, ax=ax[0], cbar_kws={'label': 'Proporción'})
sns.heatmap(plt_data, annot=True, ax=ax[1], cbar_kws={'label': 'Proporción'})


#%% Get proportion by specific elements
# Murcie
df_murcie = pd.crosstab(index=df['sensor_name'], columns=df['Id'])
df_murcie = df_murcie['MURCIE'].to_frame() / 6
df_murcie.reset_index(inplace=True)
df_murcie = df_murcie.merge(df_env, on='sensor_name')
df_murcie.groupby('sensor_name').mean()
sns.boxplot(x='Cobertura', y='MURCIE', data=df_murcie)

