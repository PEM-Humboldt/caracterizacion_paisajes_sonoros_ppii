#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sample data from acoustic monitoring taking a sample of few seconds from each file.
The data is organized into a dictionary and saved as pickle format.

@author: jsulloa
"""

import pandas as pd
import numpy as np
from librosa.core import load
from preprocessing_utils import search_files
import pickle

#%% Set variables 
path_dir = '/Volumes/PAPAYA/anh_aguas_bajas/'
path_save = '/Volumes/PAPAYA/pkl_data/'
fname_csv = '../audio_metadata/audio_metadata_aguas_bajas.csv'
date_range = ['2019-01-01 00:00:00','2022-12-01 23:50:00']
num_days = 5  # number of days to sample
num_rec_perday = 48  # number of recordings per day
t_window = 5 # window of audio per file in seconds
fs = 192000 # homogeneous sampling frequency
save_pickle = True

#%%

flist_full = pd.read_csv(fname_csv)
flist_full['date_fmt'] = pd.to_datetime(flist_full.date,  format='%Y-%m-%d %H:%M:%S')

sensor_name_list = flist_full.sensor_name.unique()[89:]  # to process in small batches.
#sensor_name_list = flist_full.sensor_name.unique()  # to process all the data in one batch

#%% Loop by sensor
for sensor_name in sensor_name_list:
    print('Processing sensor: ', sensor_name)
    # filter, and format flist
    idx_dates = (flist_full['date_fmt'] > date_range[0]) & (flist_full['date_fmt'] <= date_range[1])
    idx_sensor = (flist_full.sensor_name==sensor_name)
    flist = flist_full.loc[idx_dates & idx_sensor,:]
    flist = flist.groupby(flist.date_fmt.dt.dayofyear).filter(lambda x:len(x)==num_rec_perday)
    flist = flist.iloc[0:num_days*num_rec_perday,:]
    # select days with 48 samples per day

    flist_days = flist.groupby(flist.date_fmt.dt.dayofyear)    
    s_dict = dict()
    for idx_global, (day, flist_spectro) in enumerate(flist_days):
        date = flist_spectro.date_fmt.iloc[0].strftime('%y-%m-%d')
        print('Processing date: ', date)
        # list trough each file
        
        # iterate by day    
        for idx, (index, flist_row) in enumerate(flist_spectro.iterrows()):
            fname = flist_row['fname']
            date_str = flist_row['date']
            flist_row['fs'] = fs
            flist_row['t_window'] = t_window
            #print('day', idx_global+1,'/',len(flist_days), ': file', idx+1, '/', len(flist_spectro), fname)
            fname_path = search_files(path_dir, fname)
            s, fs = load(fname_path, sr=fs, duration=t_window)
            s_dict[date_str] = {'s' : s,
                               'audio_metadata': flist_row}
    
    if save_pickle:
        fname_save = path_save + sensor_name + '.pkl'
        s_dict['flist'] = flist
        pickle_out = open(fname_save, 'wb')
        pickle.dump(s_dict, pickle_out)
        pickle_out.close()  
        s_dict= dict()
        
