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
import os
from maad import sound
from librosa import feature
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import f1_score, classification_report
from joblib import dump, load
import matplotlib.pyplot as plt

#%% Set variables
path_annotations = r'C:\Users\gabriel.perilla\Documents\Ecoacustica\ANH_RAIN_DATASET/audio_labels.csv'  # manual annotations in csv table
path_audio = r'C:\Users\gabriel.perilla\Documents\Ecoacustica\ANH_RAIN_DATASET\audio'  # directory where the audio data is located
target_fs = 10000  # set target sampling rate for audio

#%% Load annotations
df = pd.read_csv(path_annotations, sep=",")

#%% Compute features
df_features = pd.DataFrame()

for idx_row, row in df.iterrows():
    full_path_audio = os.path.join(path_audio, row.sample_idx)
    s, fs = sound.load(full_path_audio)
    # resample
    s_trim = sound.trim(s, fs, 30, 40)
    s_resamp = sound.resample(s_trim, fs, target_fs, res_type='kaiser_fast')
    # transform
    mfcc = feature.mfcc(y=s_resamp, sr=target_fs, n_mfcc=20, n_fft=1024,
                        win_length=1024, hop_length=512, htk=True)
    mfcc = np.median(mfcc, axis=1)
    # format dataframe
    idx_names = ['mfcc_' + str(idx).zfill(2) for idx in range(1,mfcc.size+1)]
    row = row.append(pd.Series(mfcc, index=idx_names))
    row.name = idx_row
    df_features = df_features.append(row)

#%% Split development and test data
X = df_features.loc[:,df_features.columns.str.startswith('mfcc')]
y = (df_features.label=='LLUVIA').astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.2,
                                                    shuffle=True,
                                                    random_state=42)


#%% Tune model fixed hyperparameters
clf = MLPClassifier(random_state=245)


# Set tuning strategy for unfixed parameters
param_grid = {"hidden_layer_sizes":[2,5,10,50,100,150,200],
            "activation": ('identity', 'logistic', 'tanh', 'relu'),
            "alpha": [0.0001, 0.001, 0.01, 0.1],
            "learning_rate":('constant', 'invscaling', 'adaptive'),
            "solver":('lbfgs', 'sgd', 'adam'),
            "learning_rate_init":[0.001, 0.01, 0.1, 1],
            "max_iter":[200,500,1000]
            }

skf = StratifiedKFold(n_splits=10)
metric = 'f1'
clf_gs = GridSearchCV(clf, param_grid, scoring=[metric],
                           refit='f1', cv=skf, return_train_score=True,
                           n_jobs=-1, verbose=2).fit(X_train, y_train)


#%% Evaluation: compute metrics, error analysis
print('Mean cross-validated score of the best_estimator:', clf_gs.best_score_)
print('Parameter setting that gave the best results on hold out data', clf_gs.best_params_)


# Plots to explore results of cross-validation
params = ['param_max_features', 'param_n_estimators']
metrics = ['mean_test_f1', 'mean_fit_time']
fig, ax = plt.subplots(2,2, figsize=[10,10])

ax[0,0].plot(clf_gs.cv_results_[params[0]].tolist(), clf_gs.cv_results_[metrics[0]], 'o')
ax[0,0].set_xlabel(params[0]); ax[0,0].set_ylabel(metrics[0]);

ax[0,1].plot(clf_gs.cv_results_[params[1]].tolist(), clf_gs.cv_results_[metrics[0]], 'o')
ax[0,1].set_xlabel(params[1]); ax[0,1].set_ylabel(metrics[0]);

ax[1,0].plot(clf_gs.cv_results_[params[0]].tolist(), clf_gs.cv_results_[metrics[1]], 'o')
ax[1,0].set_xlabel(params[0]); ax[1,0].set_ylabel(metrics[1]);

ax[1,1].plot(clf_gs.cv_results_[params[1]].tolist(), clf_gs.cv_results_[metrics[1]], 'o')
ax[1,1].set_xlabel(params[1]); ax[1,1].set_ylabel(metrics[1]);


#%% Saving parameters and scores
results = pd.DataFrame(clf_gs.cv_results_).sort_values("rank_test_"+metric)
results.to_csv(path_or_buf = os.path.join(path_audio, "tuning"+metric+".csv"), index=True)

#%% Final evaluation on test data
y_pred = clf_gs.predict(X_test)
score = f1_score(y_test, y_pred)
print(classification_report(y_test, y_pred, labels=[1,0]))
print('Final test metrics:', score)

#%% Saving best model
dump(clf_gs.best_estimator_, os.path.join(path_audio, 'MLP_rain.joblib'))
clf_best = load(os.path.join(r'C:\Users\gabriel.perilla\Documents\Ecoacustica\ANH_RAIN_DATASET\audio', 'MLP_rain.joblib'))

#%% loading new audio data
new_audio = r"C:/Users/gabriel.perilla/Documents/Ecoacustica/migracion/muestreoaleatorio"# directory where the new audio data is located

# csv table, with the names of each new audio file in column "sample_idx"
new_files = r"C:/Users/gabriel.perilla/Documents/Ecoacustica/migracion/muestreoaleatorio/metadata/metadata.csv"

df_new = pd.read_csv(new_files, sep=";")
dfnew_feat = pd.DataFrame()

for idx_row, row in df_new.iterrows():
    full_path_audio = os.path.join(new_audio, row.sample_idx)
    s, fs = sound.load(full_path_audio)
    # resample
    s_trim = sound.trim(s, fs, 30, 40)
    s_resamp = sound.resample(s_trim, fs, target_fs, res_type='kaiser_fast')
    # transform
    mfcc = feature.mfcc(y=s_resamp, sr=target_fs, n_mfcc=20, n_fft=1024,
                        win_length=1024, hop_length=512, htk=True)
    mfcc = np.median(mfcc, axis=1)
    # format dataframe
    idx_names = ['mfcc_' + str(idx).zfill(2) for idx in range(1,mfcc.size+1)]
    row = row.append(pd.Series(mfcc, index=idx_names))
    row.name = idx_row
    dfnew_feat = dfnew_feat.append(row)

#%% Predict new data
Xnew = dfnew_feat.loc[:,dfnew_feat.columns.str.startswith('mfcc')]
ynew = clf_best.predict(Xnew)
prob = clf_best.predict_proba(Xnew)


#%% create csv for error evaluation
df_new['lluvia']= ynew
df['probabilidad no lluvia'], df['probabilidad lluvia']= pro
new_erros = df[['sample_idx', 'lluvia', 'probabilidad no lluvia', 'probabilidad lluvia']]
new_erros.to_csv(path_or_buf=os.path.join(new_audio, "audiosRain.csv"), index=True)