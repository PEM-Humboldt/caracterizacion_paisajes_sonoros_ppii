#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build bat dataset using manual annotations from two sources: pkl and Raven.
    - pkl annotations were performed while doing a preliminary inspection on the data
    - Raven annotations were performed with similar protocol, but inspecting a random set of audio

Once the annotations are procesed and standardized. A simple loop will: load audio, 
resample, trim and write to disk

"""

import pandas as pd
from utils import roi2windowed
from maad import sound
from utils import find_file
import os

#%% 
# set variables
path_audio = '/Volumes/PAPAYA/anh_aguas_altas/'
path_save_audio = '/Volumes/PAPAYA/ANH_BAT_DATASET/audio/'
path_save_csv = '/Volumes/PAPAYA/ANH_BAT_DATASET/'
wl = 10 # window length of each sample in seconds
target_fs = 192000 # target sampling frequency

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

# select only ROIs that have high frequency (min_f>7000)
df_pkl = df_pkl.loc[df_pkl.min_f>7000,:]

# discretize bat anotations into fized time windows
df_fmt = pd.DataFrame()
for idx, roi in df_pkl.iterrows():
    roi_fmt = roi2windowed(wl, roi)
    roi_fmt['fname'] = roi.fname
    df_fmt = df_fmt.append(roi_fmt)

# fix start and end
for idx, roi in df_fmt.iterrows():
    if roi.min_t<0:
        df_fmt.loc[idx,'min_t'] = 0
        df_fmt.loc[idx,'max_t'] = 10
    elif roi.max_t>60:
        df_fmt.loc[idx,'min_t'] = 50
        df_fmt.loc[idx,'max_t'] = 60
    else:
        pass
    

df_pkl = df_fmt

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

# remove rows with indetermined or with poor representation, or with
keep_idx = ~df_raven.label.isin(['SILENC', 'INDETE', 'MURCIE?'])
df_raven = df_raven.loc[keep_idx, :]

# select only ROIs that have high frequency (min_f>7000)
df_raven = df_raven.loc[df_raven.min_f>7000,:]

# format to desired output: one label per file
df_out = pd.DataFrame()
for fname, df_fname in df_raven.groupby('fname'):
    if df_fname.label.str.contains('MURCIE').any():
        df_out = df_out.append(df_fname.loc[df_fname.label=='MURCIE',:])
    else:
        df_out = df_out.append(df_fname.iloc[0,:])

# discretize bat anotations into fized time windows
df_fmt = pd.DataFrame()
for idx, roi in df_out.iterrows():
    roi_fmt = roi2windowed(wl, roi)
    roi_fmt['fname'] = roi.fname
    df_fmt = df_fmt.append(roi_fmt)

# fix start and end
for idx, roi in df_fmt.iterrows():
    if roi.min_t<0:
        df_fmt.loc[idx,'min_t'] = 0
        df_fmt.loc[idx,'max_t'] = 10
    elif roi.max_t>60:
        df_fmt.loc[idx,'min_t'] = 50
        df_fmt.loc[idx,'max_t'] = 60
    else:
        pass
#Select all MURCIE samples and only a sample of the other sounds
df_out = df_fmt.loc[df_fmt.label=='MURCIE',:]
df_out = df_out.append(df_fmt.loc[df_fmt.label!='MURCIE',:].sample(400, random_state=123))

# Add sample idx column.
df_out['sample_idx'] = [str(idx).zfill(4) for idx in range(len(df_pkl), len(df_pkl) + df_out.shape[0])]
df_out.sample_idx = df_out.sample_idx+'.wav'

# append previous annotations and save to disk
df_out = df_out.append(df_pkl)
df_out.sort_values('sample_idx', inplace=True)
df_out.to_csv('/Volumes/Audiolib/ML_datasets/ANH_BAT_DATASET/audio_labels.csv', index=False)

#%% Write audio
for idx_row, row in df_out.iterrows():
    print(idx_row+1, '/', len(df_out))
    full_path_audio = find_file(row.fname, path_audio)[0]
    s, fs = sound.load(full_path_audio)
    s_trim = sound.trim(s, target_fs, row.min_t, row.max_t, pad=True)
    fname_save = os.path.join(path_save_audio, row.sample_idx) 
    sound.write(fname_save, fs=target_fs, data=s_trim, bit_depth=16)
