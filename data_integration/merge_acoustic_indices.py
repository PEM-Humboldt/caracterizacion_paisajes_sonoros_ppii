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

#%% Load data T1
path_metadata = '../aguas_altas_t1/audio_metadata/audio_metadata_aguas_altas_t1_subsample.csv'
path_indices = '../aguas_altas_t1/acoustic_community_characterization/acoustic_indices/dataframes/*.csv'
path_env = '../aguas_altas_t1/env_data/ANH_to_GXX.csv'

# Audio metadata
df_metadata = pd.read_csv(path_metadata)
df_env = pd.read_csv(path_env).loc[:,['sensor_name', 'eventID']]
df_env.eventID.replace({'ANH_64': 'ANH_064', 
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
                        'ANH_77': 'ANH_077'}, inplace=True)

# Acoustic indices
flist = glob.glob(path_indices)
df_indices = pd.DataFrame()
for fname in flist:
    df_indices = df_indices.append(pd.read_csv(fname))

df_indices_t1 = df_indices.loc[df_indices.fname_audio.isin(df_metadata.fname_audio),:]  #select only subsample
df_indices_t1 = df_indices_t1.merge(df_env, on='sensor_name')
df_indices_t1.rename(columns={'fname_audio': 'fname'}, inplace=True)
df_indices_t1['season'] = 'T1'

#%% Load data T2
path_metadata = '../aguas_bajas_t2/audio_metadata/audio_metadata_aguas_bajas_t2_subsample.csv'
path_indices = '../aguas_bajas_t2/acoustic_community_characterization/acoustic_indices/dataframes/*.csv'
path_env = '../aguas_bajas_t2/env_data/ANH_to_GXX_Cobertura.csv'
path_proba_rain = '../aguas_bajas_t2/detection/rain_predictions.csv'

# Audio metadata and env
df_metadata = pd.read_csv(path_metadata)
df_env = pd.read_csv(path_env).loc[:,['eventID','sensor_name','Cobertura']]
df_proba_rain = pd.read_csv(path_proba_rain)

# Acoustic indices
flist = glob.glob(path_indices)
df_indices = pd.DataFrame()
for fname in flist:
    df_indices = df_indices.append(pd.read_csv(fname))

df_indices_t2 = df_indices.loc[df_indices.fname.isin(df_metadata.fname),:]  #select only subsample
df_indices_t2 = df_indices_t2.merge(df_env, on='sensor_name')
df_indices_t2 = df_indices_t2.merge(df_proba_rain, on='fname')
df_indices_t2['time'] = df_indices_t2['fname'].str[-10:-8].astype(int)
df_indices_t2['season'] = 'T2'

#%% combine data
df = pd.concat([df_indices_t1, df_indices_t2], axis=0)
df.to_csv('./dataframes/compiled_acoustic_indices.csv')

