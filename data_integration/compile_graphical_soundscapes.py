#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 18:20:26 2022

@author: jsulloa
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

#%% Aguas altas T1
# load env data
df_env = pd.read_csv('../aguas_altas_t1/env_data/ANH_to_GXX.csv')
df_env = df_env[['sensor_name', 'eventID', 'Cobertura']]

# load indices data
flist = glob.glob('../aguas_altas_t1/acoustic_community_characterization/graphical_soundscapes/dataframes/*.csv')
df = pd.DataFrame()
for fname in flist:
    aux = pd.read_csv(fname)
    aux.drop(columns='hour', inplace=True)
    aux = pd.Series(aux.values.ravel(), name=fname[-8:-4])
    df = df.append(aux)

# merge acoustic indices and spatial cover
df.reset_index(inplace=True)
df.rename(columns={'index': 'sensor_name'}, inplace=True)
df = df.merge(df_env, on='sensor_name')

# save to a dataframe
df.to_csv('./dataframes/tfbins_aguas_altas_t1.csv', index=False)

#%% Aguas bajas T2
# load env data
df_env = pd.read_csv('../aguas_bajas_t2/env_data/ANH_to_GXX_Cobertura.csv')
df_env = df_env[['sensor_name', 'eventID', 'Cobertura']]

# load indices data
flist = glob.glob('../aguas_bajas_t2/acoustic_community_characterization/graphical_soundscape/dataframes/*.csv')
df = pd.DataFrame()
for fname in flist:
    aux = pd.read_csv(fname)
    aux.drop(columns='hour', inplace=True)
    aux = pd.Series(aux.values.ravel(), name=fname[-8:-4])
    df = df.append(aux)

# merge acoustic indices and spatial cover
df.reset_index(inplace=True)
df.rename(columns={'index': 'sensor_name'}, inplace=True)
df = df.merge(df_env, on='sensor_name')

# save to a dataframe
df.to_csv('./dataframes/tfbins_aguas_bajas_t2.csv', index=False)

#%% Aguas bajas T3
# load env data
df_env = pd.read_csv('../aguas_bajas_t3/env_data/ANH_to_GXX_Cobertura.csv')
df_env = df_env[['sensor_name', 'eventID', 'Cobertura']]

# load indices data
flist = glob.glob('../aguas_bajas_t3/acoustic_community_characterization/graphical_soundscapes/dataframes/*.csv')
df = pd.DataFrame()
for fname in flist:
    aux = pd.read_csv(fname)
    aux.drop(columns='hour', inplace=True)
    aux = pd.Series(aux.values.ravel(), name=fname[-8:-4])
    df = df.append(aux)

# merge acoustic indices and spatial cover
df.reset_index(inplace=True)
df.rename(columns={'index': 'sensor_name'}, inplace=True)
df = df.merge(df_env, on='sensor_name')

# save to a dataframe
df.to_csv('./dataframes/tfbins_aguas_bajas_t3.csv', index=False)

#%% Aguas bajas T4
# load env data
df_env = pd.read_csv('../aguas_bajas_t4/env_data/ANH_to_GXX_Cobertura.csv')
df_env = df_env[['sensor_name', 'eventID', 'Cobertura']]

# load indices data
flist = glob.glob('../aguas_bajas_t4/acoustic_community_characterization/graphical_soundscapes/dataframes/*.csv')
df = pd.DataFrame()
for fname in flist:
    aux = pd.read_csv(fname)
    aux.drop(columns='hour', inplace=True)
    aux = pd.Series(aux.values.ravel(), name=fname[-8:-4])
    df = df.append(aux)

# merge acoustic indices and spatial cover
df.reset_index(inplace=True)
df.rename(columns={'index': 'sensor_name'}, inplace=True)
df = df.merge(df_env, on='sensor_name')

# save to a dataframe
df.to_csv('./dataframes/tfbins_aguas_bajas_t4.csv', index=False)

