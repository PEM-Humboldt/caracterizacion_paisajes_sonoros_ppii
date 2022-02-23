#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detect audio recordings with rain using MFCC and logistic regression

Assuming that rain events are stable during a period of 60s or more, the detector analyzes
the first 10 seconds of each recording. It computes the MFCC and uses a trained model to
evaluate the probability of having rain in the recording.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from maad import sound
import glob
import os
from librosa import feature
from utils import find_file

#%% Set variables
fpath_csv = '../../anotaciones_manuales/anotaciones_pkl_consolidado.csv'
path_audio = '/Volumes/PAPAYA/ANH/'
target_fs = 16000
wl = 10

#%% Compute features
df = pd.read_csv(fpath_csv)

df_features = pd.DataFrame()
for idx_row, row in df.iterrows():
    print(idx_row+1, '/', len(df))
    full_path_audio = find_file(row.fname, path_audio)[0]
    s, fs = sound.load(full_path_audio)
    
    # transform
    s = sound.trim(s, fs, 0, wl)
    mfcc = feature.mfcc(s, sr=target_fs, n_mfcc=20, hop_length=1024, fmax=8000)
    mfcc = np.median(mfcc, axis=1)
    
    # format dataframe
    idx_names = ['mfcc_' + str(idx).zfill(2) for idx in range(1,mfcc.size+1)]
    row = row.append(pd.Series(mfcc, index=idx_names))
    row.name = idx_row
    df_features = df_features.append(row)

#%% Set train test datasets
# assign variables
X = df_features.loc[:,df_features.columns.str.startswith('mfcc')]
y = (df_features.label=='LLUVIA').astype(int)
y.value_counts()
 
#%% Tune classifier with cross validation
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.metrics import f1_score, confusion_matrix
from classif_fcns import misclassif_idx
import joblib

clf = LogisticRegression(solver='liblinear', max_iter=10000, class_weight='balanced')
clf = LogisticRegressionCV(Cs=1000, penalty='l2', solver='liblinear',
                           scoring='f1', max_iter=10000, class_weight='balanced', 
                           cv=10, random_state=123)

# fit classifier
clf.fit(X, y)

#%% Final evaluation on test set and save model
# Note: Do not use the test set to select a model.

X = df_features.loc[:,df_features.columns.str.startswith('mfcc')]
y = (df_features.label=='LLUVIA').astype(int)
y_pred = clf.predict(X)
y_prob = clf.predict_proba(X)
df_features['y_prob'] = clf.predict_proba(X)[:,1]

f1_score(y, y_pred)
confusion_matrix(y, y_pred)
misclassified = misclassif_idx(y, y_pred)
df_features.loc[misclassified['fp'], ['fname', 'y_prob', 'label']]
df_features.loc[misclassified['fn'], ['fname', 'y_prob', 'label']]

# save model
joblib.dump(clf, 'clf_rain_logistic_regression.joblib')

#%% Deploy on new data
import glob
flist = pd.read_csv('../../audio_metadata/audio_metadata_lluvias.csv')
flist = flist.fname_audio.tolist()

df_pred = dict()
for idx, fname in enumerate(flist):
    print(idx+1, '/', len(flist))
    full_path_audio = find_file(fname, path_audio)[0]
    s, fs = sound.load(full_path_audio)
    
    # transform - must be the same as in training
    s = sound.trim(s, fs, 0, wl)
    mfcc = feature.mfcc(s, sr=target_fs, n_mfcc=20, hop_length=1024, fmax=8000)
    mfcc = np.median(mfcc, axis=1)
    
    # format dataframe
    pred_clf = clf.predict_proba(mfcc.reshape(1,20))[:,1]
    df_pred[os.path.basename(fname)] = np.round(pred_clf,2)
    
df_pred = pd.DataFrame(df_pred, index=['proba_rain']).T
df_pred.to_csv('rain_predictions.csv')