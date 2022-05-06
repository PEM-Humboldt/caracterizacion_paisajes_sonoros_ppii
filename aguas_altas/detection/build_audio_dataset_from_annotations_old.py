#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build dataset of raw audio
Load audio, resample, trim and write to disk
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
path_annot = '../manual_annotations/anotaciones_pkl_consolidado.csv'
wl = 10 # window length of each sample in seconds
target_fs = 22050 # target sampling frequency

#%% batch process annotations on pkl data

# Format dataframe
df = pd.read_csv(path_annot)
df.label.replace({'NYCALB': 'AVEVOC',
                  'CAMGRY': 'AVEVOC',
                  'TYRMEL': 'AVEVOC',
                  'MILCHI': 'AVEVOC',
                  'PITSULF': 'AVEVOC',
                  'ENGPOS': 'HERPET',
                  'TRAMOT': 'ANTROP',
                  'ALTVOZ': 'ANTROP'}, inplace=True)

# remove rows with indetermined or with poor representation, or with
keep_idx = ~df.label.isin(['SILENC', 'MAMIF', 'INDETE', 'MURCIE?'])
df = df.loc[keep_idx, :]

# remove unnecesary columns
df.drop(columns=['fname_pkl', 'length'], inplace=True)

# set sample names
df['sample_idx'] = [str(idx).zfill(4) for idx in range(0,df.shape[0])]
df.sample_idx = df.sample_idx+'.wav'

for idx_row, row in df.iterrows():
    print(idx_row+1, '/', len(df))
    full_path_audio = find_file(row.fname, path_audio)[0]
    s, fs = sound.load(full_path_audio)
    s = sound.resample(s, fs, target_fs, res_type='kaiser_fast')
    s_trim = sound.trim(s, target_fs, 0, wl)
    fname_save = os.path.join(path_save_audio, row.sample_idx) 
    sound.write(fname_save, fs=target_fs, data=s_trim, bit_depth=16)

# save data frame
df.to_csv(path_save_csv+'audio_labels.csv', index=False)