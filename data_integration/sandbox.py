#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 20:14:09 2022

@author: jsulloa
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# load nmds data for t1
nmds = pd.read_csv('../aguas_altas_t1/acoustic_community_characterization/graphical_soundscapes/nmds_data/nmds_data.csv')

# load tfbins for t1
tfbins = pd.read_csv('./dataframes/tfbins_aguas_altas_t1.csv')
acoustic_activity = pd.DataFrame({'activity': tfbins.sum(axis=1) / 3071,
                                  'sensor_name': tfbins.sensor_name})

affinis = pd.DataFrame()
for idx, row in tfbins.iterrows():
    aux = row['0':'3071'].values.reshape([24, 128])
    affinis = affinis.append({'sensor_name': row.sensor_name,
                              'activity': aux[:,60:128].sum()}, ignore_index=True)
affinis.act

# load acoustic indices
indices = pd.read_csv('../aguas_altas_t1/build_gdb/dataframes/gdb_sites_T1.csv')



tfbins_t1 = pd.read_csv('./dataframes/tfbins_aguas_altas_t1.csv')
tfbins_t4 = pd.read_csv('./dataframes/tfbins_aguas_bajas_t4.csv')

herbazal_t1 = tfbins_t1.loc[tfbins_t1.Cobertura=='Herbazales']
herbazal_t4 = tfbins_t4.loc[tfbins_t4.Cobertura=='Herbazales']

plt.figure()
plt.imshow(herbazal_t1.sum(axis=0)['0':'3071'].values.reshape([24,128]).astype(float).T,
           origin='lower', aspect='auto')

plt.figure()
plt.imshow(herbazal_t4.sum(axis=0)['0':'3071'].values.reshape([24,128]).astype(float).T,
           origin='lower', aspect='auto', extent=[0, 24, 0, 24])


#%% Plot N. affinis
from maad import sound, util

s, fs = sound.load('/Volumes/Audiolib/COLOMBIA_2021/FINCA_LACHACONA/FINCA_20211015_110200_Neoconocephalus_affinis.WAV')
s = sound.trim(s, fs, 1.7, 37.4)
s = sound.resample(s, fs, target_fs = 48000)
s = sound.normalize(s, max_amp=1)
fs = 48000

Sxx, tn, fn, ext = sound.spectrogram(s, 48000, flims=[0, 24000], display=True)
pxx, f_idx = sound.spectrum(s, fs, nperseg=1024)
Sxx, tn, fn, ext = sound.spectrogram(s,fs)

plt.close('all')
fig, ax = plt.subplots(2,1, figsize=(8,5))

util.plot_spectrum(pxx, f_idx, ax=ax[0], log_scale=True)
ax[0].set_title('Neoconocephalus affinis', style='italic')
ax[0].set_xlabel('Frecuencia (Hz)')
ax[0].set_ylabel('Amplitud')
ax[0].set_ylim([-60, 0])

util.plot_spectrogram(Sxx, ext, db_range=60, gain=30, colorbar=False, ax=ax[1])
ax[1].set_xlabel('Tiempo (s)')
ax[1].set_ylabel('Frecuencia (Hz)')

#%%
# Murcis por cobertura

df = pd.read_csv('/Volumes/lacie_macosx/Dropbox/PostDoc/iavh/ANH-PPII/Análisis_paisajes_sonoros/caracterizacion_paisajes_sonoros_ppii/aguas_bajas_t2/soundscape_composition/dataframes/species_with_names.csv')
df = pd.read_csv('/Volumes/lacie_macosx/Dropbox/PostDoc/iavh/ANH-PPII/Análisis_paisajes_sonoros/caracterizacion_paisajes_sonoros_ppii/aguas_bajas_t2/soundscape_composition/dataframes/annotations_compiled.csv')

df_env = pd.read_csv('../aguas_bajas_t2/env_data/ANH_to_GXX_Cobertura.csv')

df = df.merge(df_env, on='sensor_name')
df = df.loc[df.Id=='MURCIE',:]

#%% Grabadoras dañadas
metadata = pd.read_csv('../aguas_bajas_t3/audio_metadata/audio_metadata_aguas_bajas_t3.csv')
env = pd.read_csv('../aguas_bajas_t4/env_data/ANH_to_GXX_Cobertura.csv')

len(metadata)
metadata.length.sum()/60/60


#%% Distancia palma
import statsmodels.api as sm
import seaborn as sns
df = pd.read_excel('/Users/jsulloa/Downloads/CovariablesPalma.xlsx')
env = pd.read_csv('../aguas_altas_t1/env_data/ANH_to_GXX.csv')
nmds = pd.read_csv('./dataframes/nmds.csv')
nmds = nmds.loc[nmds.temporada=='T1',:]
df = df.merge(nmds, left_on='ID_MUES_PT', right_on='eventID')
df = df.merge(env, on='eventID')

bosque = df.loc[df.Cobertura_x=='Bosque Ripario',:]
palma = df.loc[df.Cobertura_x=='Palma',:]
edge = df.loc[(df.Cobertura_x=='Bosque Ripario') | (df.Cobertura_x=='Palma'),:]

#% Plot Bosque
plt.close('all')
plt.figure()
#sns.scatterplot(x=df.MDS1, y=df.MDS2, color='gray', alpha=0.3)
sns.scatterplot(x=bosque.MDS1, y=bosque.MDS2, 
                size=np.log1p(bosque.Dis_Palma),
                hue=np.log1p(bosque.Dis_Palma), palette='crest')

plt.figure()
fig, ax = plt.subplots()
sns.regplot(y=bosque.MDS1, x=np.log1p(bosque.Dis_Palma), order=1, ax=ax)
ax.set_xticks(np.arange(0,7))
ax.set_xticklabels(np.exp(np.arange(0,7)+1).astype(int))


model = sm.OLS(bosque.MDS1, np.log1p(bosque.Dis_Palma))
res = model.fit()
print(res.summary())

# Plot Palma
plt.close('all')
plt.figure()
#sns.scatterplot(x=df.MDS1, y=df.MDS2, color='gray', alpha=0.3)
sns.scatterplot(x=palma.MDS1, y=palma.MDS2, 
                size=np.log1p(palma.DisBosque),
                hue=np.log1p(palma.DisBosque), palette='crest')

fig, ax = plt.subplots()
sns.regplot(y=palma.MDS1, x=np.log1p(palma.DisBosque), order=1, ax=ax)
ax.set_xticks(np.arange(0,7))
ax.set_xticklabels(np.exp(np.arange(0,7)+1).astype(int))

# Plot Edge
edge['dist_edge_log'] = np.log1p(edge.DisBosque) - np.log1p(edge.Dis_Palma)
edge['dist_edge'] = edge.DisBosque - edge.Dis_Palma
plt.close('all')
plt.figure()
sns.scatterplot(x=edge.MDS1, y=edge.MDS2, 
                size=np.log1p(edge.dist_edge),
                hue=np.log1p(edge.dist_edge), palette='crest')

fig, ax = plt.subplots()
sns.scatterplot(y=edge.MDS1, x=edge.dist_edge_log)
ax.set_xticks(np.arange(-7,8))
xticklabels = np.concatenate([-np.exp(np.arange(0,7))+1, 
                              np.exp(np.arange(0,8))+1]).astype(int)
ax.set_xticklabels(xticklabels)
ax.grid(visible=True)

