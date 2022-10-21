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
import time
from concurrent import futures

#%% Set variables
path_model = '../../aguas_bajas_t2/detection/models/RF_rain.joblib'
path_audio_metadata = '../audio_metadata/audio_metadata_aguas_bajas_t4_subsample.csv'
target_fs = 10000  # set target sampling rate for audio
nb_cpu = os.cpu_count()

#%% load model and file list
clf = load(path_model)
flist = pd.read_csv(path_audio_metadata)

#%% Deploy on new data
tic = time.perf_counter()


def predict_single_file(path_audio):
    s, fs = sound.load(path_audio)
    
    # transform - must be the same as in training
    s_trim = sound.trim(s, fs, 0, 10, pad=True)
    s_resamp = sound.resample(s_trim, fs, target_fs, res_type='kaiser_fast')

    # transform
    mfcc = feature.mfcc(y=s_resamp, sr=target_fs, n_mfcc=20, n_fft=1024,
                        win_length=1024, hop_length=512, htk=True)
    mfcc = np.median(mfcc, axis=1)
    
    # format dataframe
    pred_clf = clf.predict_proba(mfcc.reshape(1,20))[:,1]
    pred_out = pd.Series({'proba_rain': pred_clf[0], 'path_audio': path_audio})
    return pred_out


df_pred = pd.DataFrame()
with futures.ProcessPoolExecutor(max_workers=nb_cpu) as pool:
    # give the function to map on several CPUs as well its arguments as 
    # as list
    for pred_out in pool.map(
        predict_single_file, 
        flist['path_audio'].to_list(), 
    ):
        df_pred = df_pred.append(pred_out, ignore_index=True)
        fname = os.path.basename(pred_out.path_audio)
        print(fname, ' - proba', pred_out.proba_rain)

toc = time.perf_counter()
# time duration of the process
multicpu_duration = toc - tic

df_pred['fname'] = df_pred.path_audio.apply(lambda x: os.path.basename(x))
df_pred = df_pred.loc[:,['fname', 'proba_rain']]
df_pred.sort_values('fname', inplace=True)
df_pred.to_csv('rain_predictions_multi.csv', index=False)