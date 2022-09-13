#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integrate soundscape composition tables


"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#%% Set variables
path_global_soundscape_t1 = '../../aguas_altas_t1/soundscape_composition/dataframes/presence_absence_global_components.csv'
path_detailed_soundscape_t1 = '../../aguas_altas_t1/soundscape_composition/dataframes/presence_absence_detailed_components.csv'
path_global_soundscape_t2 = '../soundscape_composition/dataframes/presence_absence_global_components.csv'
path_detailed_soundscape_t2 = '../soundscape_composition/dataframes/presence_absence_detailed_components.csv'

path_env_data = '../env_data/ANH_to_GXX_Cobertura.csv'

#%% Load data
df_env = pd.read_csv(path_env_data)
df_env = df_env[['sensor_name', 'Cobertura']]
df_t1 = pd.read_csv(path_global_soundscape_t1)
df_t2 = pd.read_csv(path_global_soundscape_t2)
df_mix_global = pd.concat([df_t1,df_t2])

df_id_t1 = pd.read_csv(path_detailed_soundscape_t1)
df_id_t2 = pd.read_csv(path_detailed_soundscape_t2)
df_id_t1['perio']
df_mix_id = pd.concat([df_id_t1,df_id_t2])
df_mix_id.fillna(0, inplace=True)

#%% Proporción
df_prop = df_mix_global.loc[:,['ANT', 'BIO', 'GEO']].mean(axis=0) * 100
print('Proporción media de cada uno de los componentes principales\n', df_prop.round(2))

df_prop = df_mix_id.drop(columns=['fname']).mean(axis=0) * 100
print('Proporción media de cada uno de los componentes principales\n', df_prop.round(2))

#%% Spectral

# load data
df_t1 = pd.read_csv('../../aguas_altas_t1/soundscape_composition/dataframes/annotations_compiled.csv')
df_t2 = pd.read_csv('./dataframes/annotations_compiled.csv')
df = pd.concat([df_t1.drop(columns=['Feeding buzz']),
                   df_t2.drop(columns=['Comportamiento', 'Calidad'])])

df = df.loc[df.Tipo.isin(['BIO', 'ANT', 'GEO']),:]
df.reset_index(inplace=True, drop=True)


sns.kdeplot(x=df['Center Freq (Hz)'], hue=df['Tipo'], fill=True, alpha=0.5)