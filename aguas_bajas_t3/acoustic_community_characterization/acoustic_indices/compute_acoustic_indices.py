#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compute acoustic indices on a list of files.

The audio file is first resampled to 48 kHz.
Acoustic indices computed include:
    - Acoustic Diversity Index (ADI)
    - Acoustic Complexity Index (ACI)
    - Acoustic Space Used (ASU)
    - Normalized Difference Soundscape Index (NDSI)
    - Bioacoustic Index (BI)
    - Acoustic Entropy Index (H)
    - Number of peaks (NP)
    - Spectral cover (SC)

"""

import numpy as np
import pandas as pd
import pickle
from maad import sound, features, util
import os
from concurrent import futures
import time

def compute_acoustic_indices(s, Sxx, tn, fn):
    """
    Parameters
    ----------
    s : 1d numpy array
        acoustic data
    Sxx : 2d numpy array of floats
        Amplitude spectrogram computed with maad.sound.spectrogram mode='amplitude'
    tn : 1d ndarray of floats
        time vector with temporal indices of spectrogram.
    fn : 1d ndarray of floats
        frequency vector with temporal indices of spectrogram..

    Returns
    -------
    df_indices : pd.DataFrame
        Acoustic indices
    """
    
    # Set spectro as power (PSD) and dB scales.
    Sxx_power = Sxx**2
    Sxx_dB = util.amplitude2dB(Sxx)

    # Compute acoustic indices
    ADI = features.acoustic_diversity_index(
        Sxx, fn, fmin=2000, fmax=24000, bin_step=1000, index='shannon', dB_threshold=-70)
    _, _, ACI = features.acoustic_complexity_index(Sxx)
    NDSI, xBA, xA, xB = features.soundscape_index(
        Sxx_power, fn, flim_bioPh=(2000, 20000), flim_antroPh=(0, 2000))
    Ht = features.temporal_entropy(s)
    Hf, _ = features.frequency_entropy(Sxx_power)
    H = Hf * Ht
    BI = features.bioacoustics_index(Sxx, fn, flim=(2000, 11000))
    NP = features.number_of_peaks(Sxx_power, fn, mode='linear', min_peak_val=0, 
                                  min_freq_dist=100, slopes=None, prominence=1e-6)
    SC, _, _ = features.spectral_cover(Sxx_dB, fn, dB_threshold=-50, flim_LF=(1000,20000))
    
    # Structure data into a pandas series
    df_indices = pd.Series({
        'ADI': ADI,
        'ACI': ACI,
        'NDSI': NDSI,
        'BI': BI,
        'Hf': Hf,
        'Ht': Ht,
        'H': H,
        'SC': SC,
        'NP': int(NP)})

    return df_indices

def compute_acoustic_indices_signle_file(path_audio):
    s, fs = sound.load(path_audio)    
    s = sound.resample(s, fs, target_fs, res_type='kaiser_fast')

    # Compute the amplitude spectrogram and acoustic indices
    Sxx, tn, fn, ext = sound.spectrogram(
        s, target_fs, nperseg = 1024, noverlap=0, mode='amplitude')
    df_indices_file = compute_acoustic_indices(s, Sxx, tn, fn)
    df_indices_file['fname'] = os.path.basename(path_audio)
    return df_indices_file

#%% Set variables
path_save_df = './dataframes/'
target_fs = 48000  # all samples have been previously normalized to 22050 Hz
path_flist_sel = '../../audio_metadata/audio_metadata_aguas_bajas_t3_subsample.csv'
nb_cpu = os.cpu_count()

#%% Load data and flist of selected files
flist = pd.read_csv(path_flist_sel)
sensor_list = flist.sensor_name.unique()

#%% Loop through sites
for sensor_name in sensor_list:
    flist_sel = flist.loc[flist.sensor_name==sensor_name,:]
    tic = time.perf_counter()
    df_indices = pd.DataFrame()
    with futures.ProcessPoolExecutor(max_workers=nb_cpu) as pool:
        # give the function to map on several CPUs as well its arguments as 
        # as list
        for df_indices_file in pool.map(
            compute_acoustic_indices_signle_file, 
            flist_sel['path_audio'].to_list(), 
        ):
    
            # add file information to dataframes
            #add_info = row[['fname', 'sensor_name', 'date']]
            #df_indices_file = pd.concat([add_info, df_indices_file])
            
            # append to dataframe
            df_indices = df_indices.append(df_indices_file, ignore_index=True)
            print(df_indices_file.fname, '- done')
    
    # Add date and site information
    df_indices = df_indices.merge(flist_sel.loc[:,['fname', 'sensor_name', 'date']], on='fname')
    # Save dataframes
    df_indices.to_csv(path_save_df+sensor_name+'_indices.csv', index=False)
    toc = time.perf_counter()
    print('Site completed:', toc-tic, 's')

#%% Plot indices to check consistency
import matplotlib.pyplot as plt

fig, ax = plt.subplots(nrows=7, ncols=1, figsize=(15,10))
ax[0].plot(df_indices.ADI); ax[0].set_ylabel('ADI')
ax[1].plot(df_indices.ACI); ax[1].set_ylabel('ACI')
ax[2].plot(df_indices.BI); ax[2].set_ylabel('BI')
ax[3].plot(df_indices.NDSI); ax[3].set_ylabel('NDSI')
ax[4].plot(df_indices.H); ax[4].set_ylabel('H')
ax[5].plot(df_indices.NP); ax[5].set_ylabel('NP')
ax[6].plot(df_indices.SC); ax[6].set_ylabel('SC')

