#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test acoustic indices

@author: jsulloa
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from maad import sound, util, features
import sox

fpath = '/Volumes/PAPAYA/ANH/G002/G002_20211115_180000.WAV'
fpath = '/Volumes/PAPAYA/ANH/G007/G007_20211109_140000.WAV'
fpath = '/Volumes/PAPAYA/ANH/G017/G017_20211115_140000.WAV'


s, fs = sound.load(fpath)

s = sound.resample(s, fs, target_fs=48000, res_type='kaiser_fast')
Sxx, tn, fn, ext = sound.spectrogram(s, 48000, nperseg = 1024, noverlap=0, mode='amplitude')
Sxx_power = Sxx**2
Sxx_dB = util.amplitude2dB(Sxx, db_range=120)

fig, ax = plt.subplots(figsize=(10,5))
util.plot_spectrogram(Sxx_power, ext, db_range=80, ax=ax)
util.plot_spectrogram(Sxx_dB>-70, ext, ax=ax, log_scale=False)


# Compute acoustic indices
ADI = features.acoustic_diversity_index(
    Sxx, fn, fmin=2000, fmax=24000, bin_step=1000, index='shannon', dB_threshold=-50)
_, _, ACI = features.acoustic_complexity_index(Sxx)
NDSI, xBA, xA, xB = features.soundscape_index(
    Sxx_power, fn, flim_bioPh=(2000, 24000), flim_antroPh=(0, 2000))
Ht = features.temporal_entropy(s)
Hf, _ = features.frequency_entropy(Sxx_power)
H = Hf* Ht
BI = features.bioacoustics_index(Sxx, fn, flim=(2000, 24000))
NP = features.number_of_peaks(Sxx_power, fn, mode='linear', min_peak_val=0, 
                              min_freq_dist=100, slopes=None, prominence=1e-6, display=True)

SC, _, _ = features.spectral_cover(Sxx_dB, fn, dB_threshold=-50, flim_LF=(1000,24000))

# Structure series
df_indices = pd.Series({
    'ADI': ADI,
    'ACI': ACI,
    'NDSI': NDSI,
    'BI': BI,
    'Hf': Hf,
    'Ht': Ht,
    'H': H,
    'NP': int(NP)})
print(df_indices)