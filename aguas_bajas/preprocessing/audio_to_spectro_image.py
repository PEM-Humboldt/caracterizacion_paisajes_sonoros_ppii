#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Load data from pickle files and save images of spectrogram
The pipeline includes:
    - A low Butterworth pass filter
    - Spectrogram computation
    - A gaussian smoothing of the spectrogram
    - Nomalization of the spectrogram accoring to vmin, vmax values


@author: jsulloa
"""
import numpy as np
import pickle
from maad import sound, util
from personal_utilities import listdir_pattern
from skimage import io
from skimage.filters import gaussian

#%% settings
fs = 192000
opt_spec = {'wl': 4096, 'ovlp': 0.5, 'fcrop': [10,60000], 'db_range': 250}
fpath = '/Volumes/PAPAYA/pkl_data/'
path_save = '/Volumes/PAPAYA/pkl_data/'
fmt = '.png'
tlims = [00,24]  # tiempo en horas
write_wav = True

#%%

im_dict= dict()
# load elements
flist_dir = listdir_pattern(fpath, ends_with='pkl')
for fname_open in flist_dir:
    print('Processing file:', fname_open)
    pickle_in = open(fpath+fname_open,'rb')
    s_dict = pickle.load(pickle_in)
    flist = s_dict['flist']
    # filter flist
    idx_time = (flist.date_fmt.dt.hour >= tlims[0]) & (flist.date_fmt.dt.hour <= tlims[1])
    flist = flist.loc[idx_time,:]
    flist_days = flist.groupby(flist.date_fmt.dt.dayofyear)
        
    # iterate by day    
    for day, flist_day in flist_days:
        date = flist_day.date_fmt.iloc[0].strftime('%y-%m-%d')
        print('Processing date: ', date)
        # concat audio into array
        s_sum = list()
        for index, row in flist_day.iterrows():
            s = s_dict[row.date]['s']
            s_sum.append(s)
        
        # crossfade and high pass filtering
        #s_sum = crossfade_list(s_sum, fs)
        #s_sum = butter_filter(s_sum,cutoff=200, fs=fs, order=2, ftype='high')
        s_sum = np.concatenate(s_sum, axis=0)
        
        # compute spectrogram
        im, dt, df, ext = sound.spectrogram(s_sum, fs, nperseg=opt_spec['wl'],
                                            overlap=opt_spec['ovlp'], flims=opt_spec['fcrop'])
        im = util.power2dB(im, 90) + 90
        # Apply gaussian smoothing
        im = gaussian(im, sigma=0.5, mode='reflect')
        
        # Normalize spectrogram according to sensor model         
        vmin, vmax = 0, 66  # Audiomoth
        im[im<vmin] = vmin
        im[im>vmax] = vmax
        im = (im - im.min())/(im.max() - im.min())
        # save to file
        im = np.flip(im, axis=0)
        key = fname_open[0:-4]+'_'+date
        io.imsave(path_save+key+fmt, im)
        if write_wav:
            sound.write(path_save+key+'.wav', fs, s_sum, bit_depth=16)
        else:
            pass
            
