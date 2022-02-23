#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detect audio recordings with bat activity

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from maad import sound, util, rois, features
import glob
import os
from librosa import feature
from utils import find_file
from skimage.transform import resize

def compute_features(s, fs):
    Sxx, tn, fn, ext = sound.spectrogram(s, fs, nperseg=4096, noverlap=0, flims=flims)
    Sxx = util.power2dB(Sxx, db_range=90)
    Sxx = resize(Sxx, output_shape = (256, 256), anti_aliasing=True)
    # compute features
    shape, _ = features.shape_features(Sxx, resolution='high', rois=None)
    return shape, Sxx


#%% Set variables
fpath_csv = '../../anotaciones_manuales/anotaciones_pkl_consolidado.csv'
path_audio = '/Volumes/PAPAYA/ANH/'
wl = 5
flims = (10000, 95000)

#%% Select samples
df = pd.read_csv(fpath_csv)

# Select only rain, insect and murcie
keep_labels = ['MURCIE', 'INSECT', 'LLUVIA', 'PULSOS', 'SENSAT']
df = df.loc[df.label.isin(keep_labels), :]

# remove overlapping samples
flist = df.fname.value_counts()
flist = (flist.loc[flist>1]).index.to_list()
for fname in flist:
    df_sample = df.loc[df.fname==fname, :]
    idx_remove = df_sample.loc[df_sample.label=='INSECT'].index
    df = df.drop(index=idx_remove)

df.reset_index(inplace=True)

#%% 
""" Compute features

Compute 2D wavlet features using scikit-maad at resolution high.
"""
df_features = pd.DataFrame()
for idx_row, row in df.iterrows():
    # Load data
    print(idx_row+1, '/', len(df))
    full_path_audio = find_file(row.fname, path_audio)[0]
    s, fs = sound.load(full_path_audio)
    # transform
    s = sound.trim(s, fs, row.min_t, row.min_t+wl)
    Sxx, tn, fn, ext = sound.spectrogram(s, fs, nperseg=4096, noverlap=0, flims=flims)
    Sxx = util.power2dB(Sxx, db_range=90)
    Sxx = resize(Sxx, output_shape = (256, 256), anti_aliasing=True)
    # compute features
    shape, params = features.shape_features(Sxx, resolution='high', rois=None)
    # save to dataframe
    row = row.append(shape.loc[0,:])
    row.name = idx_row
    df_features = df_features.append(row)


#%%
""" Build classification model 

Build a simple and predictable classifier using logistic regression
"""
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.metrics import f1_score, confusion_matrix
from classif_fcns import misclassif_idx, print_report
import joblib

#%% Set train test datasets
df_features = pd.read_csv('./model_data/df_shape_features_bat_detection.csv')
# assign variables
X = df_features.loc[:,df_features.columns.str.startswith('shp')]
y = (df_features.label=='MURCIE').astype(int)
y.value_counts()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#%% Tune classifier with cross validation

clf = LogisticRegression(solver='liblinear', max_iter=10000, class_weight='balanced')
clf = LogisticRegressionCV(Cs=1000, penalty='l2', solver='liblinear',
                           scoring='f1', max_iter=10000, class_weight='balanced', 
                           cv=10, random_state=123)

# fit classifier
clf.fit(X, y)

# simple plot
fig, ax = plt.subplots()
ax.plot(clf.Cs_, np.mean(clf.scores_[1],0))
ax.set_xlabel('C value')
ax.set_ylabel('Score')

#%% Final evaluation on test set and save model
# Note: Do not use the test set to select a model.
y_pred = clf.predict(X)
y_prob = clf.predict_proba(X)[:,1]
print_report(y, y_prob, curve_type='prc')

# Evaluate FP and FN
df_features['y_prob'] = y_prob
misclassified = misclassif_idx(y, y_pred)
df_features.loc[misclassified['fp'], ['fname', 'y_prob', 'label']]
df_features.loc[misclassified['fn'], ['fname', 'y_prob', 'label']]

# save model
joblib.dump(clf, 'clf_bats_logistic_regression.joblib')

#%% 
""" Deploy on new data

Select samples for deployment. 
Samples must be during peak of bat activity 05-08h and 17-20h, and for 5 days in each site.
"""
# variables and load data
num_rec_perday = 48
num_days = 5
flist_full = pd.read_csv('../../audio_metadata/audio_metadata_lluvias.csv')
flist_full['date_fmt'] = pd.to_datetime(flist_full.date, format='%Y-%m-%d %H:%M:%S')

# select samples - first 5 days per sensor
sensor_name_list = flist_full.sensor_name.unique()
flist_sel = pd.DataFrame()
for sensor in sensor_name_list:
    flist = flist_full.loc[flist_full.sensor_name==sensor,:]
    flist = flist.groupby(flist.date_fmt.dt.dayofyear).filter(lambda x:len(x)==num_rec_perday)
    flist = flist.iloc[0:num_days*num_rec_perday,:]
    flist_sel = flist_sel.append(flist)

# select samples - peak of bat activity 05-08h and 17-20h
idx_hour = (((flist_sel.date_fmt.dt.hour >= 5) & (flist_sel.date_fmt.dt.hour <= 8)) | 
            ((flist_sel.date_fmt.dt.hour >= 17) & (flist_sel.date_fmt.dt.hour <= 20)))
flist_sel = flist_sel.loc[idx_hour,:]

# save list
flist_sel[['path_audio','fname_audio']].to_csv('flist_sel_bat_activity.csv', index=False)

#%% Predict
clf = joblib.load('model_data/clf_bats_logistic_regression.joblib')
path_audio = '/Volumes/PAPAYA/ANH/'
flist_sel = pd.read_csv('flist_sel_bat_activity.csv')
flist = flist_sel.path_audio.tolist()

df_pred = dict()
for idx, fname in enumerate(flist):

    # load data
    print(idx+1, '/', len(flist), ':', fname)
    full_path_audio = os.path.join(path_audio, fname)
    s, fs = sound.load(full_path_audio)    

    # analyze each file by windows
    windows = zip(np.arange(0, 60, step=wl), np.arange(0, 60, step=wl)+5)
    shape_file = pd.DataFrame()
    for idx_tw, tw in enumerate(windows):
        s_trim = sound.trim(s, fs, tw[0], tw[1])
        shape, _ = compute_features(s_trim, fs)
        shape.index = [idx_tw]
        shape_file = shape_file.append(shape)
    
    # format data
    df_pred[os.path.basename(full_path_audio)] = np.round(clf.predict_proba(shape_file)[:,1],3)
    
df_pred = pd.DataFrame(df_pred).T
df_pred.to_csv('bat_predictions.csv')

#%% Post-process
# Select samples with probability higher than 0.5 and more than n detections per file.
df_pred_file = 'bat_predictions.csv'
th = 0.5
num_detections_per_file = 1
#path_save = 'flist_bats_manual_check.csv'

#df_pred = pd.read_csv(df_pred_file, index_col=0)
flist_manual_check = (df_pred>th).sum(axis=1)
flist_manual_check = flist_manual_check.loc[flist_manual_check>=num_detections_per_file]
print('Number of files selected:', len(flist_manual_check))
flist_manual_check.to_csv(path_save)