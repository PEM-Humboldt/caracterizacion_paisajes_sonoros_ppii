#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# Realiza un muestreo aleatorio de 6 grabaciones en un directorio 
# asociado a un punto de muestreo. El muestreo se restringe a cada 
# uno de los picos de actividad acústica al amanecer (05h-08h) y 
# atardecer (17h-20h) para identificar vocalizaciones de aves 
# y anfibios, y anotar presencia o ausencia de antropofonía, 
# biofonía y geofonía.

"""
import shutil
import pandas as pd
import matplotlib.pyplot as plt

path_files = 'Dropbox/Audiolib/ML_datasets/Putumayo_2018/1k_random_samples/'
path_audio_metadata = '../audio_metadata/audio_metadata_aguas_bajas.csv'
path_save_files = '/Volumes/PAPAYA/aguas_bajas_muestreo_aleatorio/'
n_samples_per_site = 6
peak_hours = ['05', '06', '07', '08', '17', '18', '19', '20']

#%% Load data

df = pd.read_csv(path_audio_metadata)
df['hour'] = df.date.str[11:13].astype(str)
sensor_list = df.sensor_name.unique()[0:45]  # to process in batches
# sensor_list = df.sensor_name.unique()[0:45]  # to process in a singlo run

#%% Batch process
flist_out = pd.DataFrame()
for sensor_name in sensor_list:
    df_sel = df.loc[(df.sensor_name==sensor_name) & (df.hour.isin(peak_hours)),:]    
    df_sel = df_sel.sample(n_samples_per_site, random_state=0)
    flist_out = flist_out.append(df_sel)

flist_out.reset_index(drop=True, inplace=True)

# Check that all sites have 6 samples
flist_out.fname.str[0:4].value_counts()

# Check that times are distributed in a uniform way
flist_out.hour.value_counts() / len(flist_out)

# save flist
flist_out.to_csv('../manual_annotation/random_flist_mannot.csv', index=False)

#%% Copy selected files to a new folder

for idx, row in flist_out.iterrows():
    src_file = row.path_audio
    dst_file = path_save_files + row.fname
    shutil.copyfile(src_file, dst_file)