#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build dataset using manual annotations from two sources: pkl and Raven.
    - pkl annotations were performed while doing a preliminary inspection on the data
    - Raven annotations were performed with similar protocol, but inspecting a random set of audio

Once the annotations are procesed and standardized. A simple loop will: load audio, 
resample, trim and write to disk

"""

import pandas as pd
from maad import sound
from utils import find_file
import os

#%% 
# set variables
path_audio = '/Volumes/PAPAYA/ANH/'
path_save_audio = '/Volumes/PAPAYA/ANH_ML_DATASET/audio/'
path_save_csv = '/Volumes/PAPAYA/ANH_ML_DATASET/'
wl = 10 # window length of each sample in seconds
target_fs = 22050 # target sampling frequency

# annotations
path_annot_pkl = '../manual_annotations/anotaciones_pkl_consolidado.csv'
path_annot_raven = '../manual_annotations/annot_random_sampling_consolidado.csv'

#%% Batch process annotations on pkl data

# Format dataframe
df_pkl = pd.read_csv(path_annot_pkl)
df_pkl.label.replace({'NYCALB': 'AVEVOC',
                  'CAMGRY': 'AVEVOC',
                  'TYRMEL': 'AVEVOC',
                  'MILCHI': 'AVEVOC',
                  'PITSULF': 'AVEVOC',
                  'ENGPOS': 'HERPET',
                  'TRAMOT': 'ANTROP',
                  'ALTVOZ': 'ANTROP'}, inplace=True)

# remove rows with indetermined or with poor representation, or with
keep_idx = ~df_pkl.label.isin(['SILENC', 'MAMIF', 'INDETE', 'MURCIE?'])
df_pkl = df_pkl.loc[keep_idx, :]

# remove unnecesary columns
df_pkl.drop(columns=['fname_pkl', 'length'], inplace=True)

# set sample names
df_pkl['sample_idx'] = [str(idx).zfill(4) for idx in range(0,df_pkl.shape[0])]
df_pkl.sample_idx = df_pkl.sample_idx+'.wav'


#%% Batch process annotations on Raven files

# read dataframe and previous annotations
df_raven = pd.read_csv(path_annot_raven)

# remove unnecesary columns and rename them
rm_idx = ['Unnamed: 0', 'Center Freq (Hz)', 'Tipo', 'Determinacion', 'fname_annot', 'sensor_name', 'Feeding buzz']
df_raven.drop(columns=rm_idx, inplace=True)
df_raven.rename(columns={'Begin Time (s)': 'min_t', 
                   'End Time (s)': 'max_t', 
                   'Low Freq (Hz)': 'min_f', 
                   'High Freq (Hz)': 'max_f',
                   'Id': 'label'}, inplace=True)

# remove rows with Id with NaN
df_raven = df_raven.loc[~df_raven.label.isna(), :]

# remove rows with no annotations in the first 10 seconds and adjust max_t
df_raven = df_raven.loc[df_raven['min_t'] < 10, :]
df_raven.max_t.loc[df_raven.max_t>10] = 10

# remove annotations that match previous pkl annotations
df_raven = df.loc[~df_raven.fname.isin(df_pkl.fname),:]

# format to desired output: one label per file
df_out = pd.DataFrame()
for fname, df_fname in df.groupby('fname'):
    if df_fname.label.str.contains('LLUVIA').any():
        df_out = df_out.append(df_fname.loc[df_fname.label=='LLUVIA',:])
    else:
        df_out = df_out.append(df_fname.iloc[0,:])

# Add sample idx column. 538 is the offset from the previous pkl annotations
df_out['sample_idx'] = [str(idx).zfill(4) for idx in range(538, 538 + df_out.shape[0])]
df_out.sample_idx = df_out.sample_idx+'.wav'

# append previous annotations and save to disk
df_out = df_out.append(df_pkl)
df_out.sort_values('sample_idx', inplace=True)
df_out.to_csv('/Volumes/PAPAYA/ANH_ML_DATASET/audio_labels.csv', index=False)

#%% Write audio
for idx_row, row in df_out.iterrows():
    print(idx_row+1, '/', len(df_out))
    full_path_audio = find_file(row.fname, path_audio)[0]
    s, fs = sound.load(full_path_audio)
    s = sound.resample(s, fs, target_fs, res_type='kaiser_fast')
    s_trim = sound.trim(s, target_fs, 0, wl)
    fname_save = os.path.join(path_save_audio, row.sample_idx) 
    sound.write(fname_save, fs=target_fs, data=s_trim, bit_depth=16)
