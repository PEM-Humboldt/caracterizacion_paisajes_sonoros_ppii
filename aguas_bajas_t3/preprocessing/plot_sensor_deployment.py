#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 16:17:59 2022

@author: jsulloa
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

path_audio_metadata = '../audio_metadata/audio_metadata_aguas_bajas_t3.csv'
df = pd.read_csv(path_audio_metadata)
df.loc[:,'date_fmt'] = pd.to_datetime(df.date,  format='%Y-%m-%d %H:%M:%S')


df_out = pd.DataFrame()
for sensor_name, df_sensor in df.groupby('sensor_name'):
    aux = pd.DataFrame(df_sensor.date_fmt.dt.date.value_counts())
    aux['sensor_name'] = sensor_name
    aux.reset_index(inplace=True)
    aux.rename(columns={'index': 'date', 'date_fmt': 'num_rec'}, inplace=True)
    df_out = df_out.append(aux)


df_site = pd.DataFrame()
for sensor_name, df_sensor in df.groupby('sensor_name'):
    df_sensor.sort_values('date', inplace=True)
    df_site = df_site.append({
        'sensor_name': sensor_name,
        'sample_rate': int(df_sensor.sample_rate.iloc[0]),
        'bit_depth': int(df_sensor.bits.iloc[0]),
        'date_ini': df_sensor.date.iloc[0][0:10],
        'date_end': df_sensor.date.iloc[-1][0:10],
        'time_ini': df_sensor.date.iloc[0][11:19],
        'time_end': df_sensor.date.iloc[-1][11:19]
        }, ignore_index=True)

fig, ax = plt.subplots(figsize=(15,8))
sns.scatterplot(y='date', x='sensor_name', 
                size='num_rec', size_norm = (10, 100), 
                hue='num_rec', hue_norm = (10, 100),
                data=df_out, ax=ax)

