#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deploy model on new data

@author: jsulloa
"""

import numpy as np
import pandas as pd
from joblib import load
from utils import find_file
from maad import sound
from librosa import feature
import os

#%% Set variables
path_model = './models/RF_rain.joblib'
path_audio_metadata = '../audio_metadata/audio_metadata_aguas_bajas.csv'
path_audio = '/Volumes/PAPAYA/anh_aguas_bajas/'
target_fs = 10000  # set target sampling rate for audio

#%% load model and file list
clf = load(path_model)
flist = pd.read_csv(path_audio_metadata)

#%% Deploy on new data


flist = flist.fname.tolist()

df_pred = dict()
for idx, fname in enumerate(flist):
    print(idx+1, '/', len(flist))
    full_path_audio = find_file(fname, path_audio)[0]
    s, fs = sound.load(full_path_audio)
    
    # transform - must be the same as in training
    s_trim = sound.trim(s, fs, 0, 10, pad=True)
    s_resamp = sound.resample(s_trim, fs, target_fs, res_type='kaiser_fast')

    # transform
    mfcc = feature.mfcc(y=s_resamp, sr=target_fs, n_mfcc=20, n_fft=1024,
                        win_length=1024, hop_length=512, htk=True)
    mfcc = np.median(mfcc, axis=1)
    
    # format dataframe
    pred_clf = clf.predict_proba(mfcc.reshape(1,20))[:,1]
    df_pred[os.path.basename(fname)] = np.round(pred_clf,2)
      
df_pred = pd.DataFrame(df_pred, index=['proba_rain']).T
df_pred.to_csv('rain_predictions.csv')