#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build dataset using manual annotations on Audacity
"""

import numpy as np
import pandas as pd
from maad import sound, util
from utils import roi2windowed, find_file, read_annotation_dir
import os
import glob

# Set main variables
target_fs = 24000  # target fs of project
wl = 5  # Window length for formated rois

#%%
"""
----------------------
Preprocess anntoations
----------------------

Read annotations performed on long soundscapes and match them with original files

"""
# Set variables for positive samples
path_annot = '../../anotaciones_manuales/anotaciones_pkl/'
path_save = '../../anotaciones_manuales/anotaciones_pkl_consolidado.csv'

# 
df = read_annotation_dir(path_annot)
df.rename(columns={'fname':'fname_pkl'}, inplace=True)

# set date vector
date = pd.to_datetime(df.fname_pkl.str[5:13], format='%y-%m-%d')

# set time vector
time_vec = pd.date_range("2021-11-05", periods=48, freq="0.5H")
idx_time = np.floor(np.round(df.min_t)/5).astype(int)

df['fname'] = (df.fname_pkl.str[0:5] + 
               date.dt.strftime('%Y%m%d_') + 
               time_vec[idx_time].strftime('%H%M%S') + '.WAV')

df['length'] = round(df.max_t - df.min_t,1)
df.min_t = round(df.min_t%5,1)
df.max_t = df.min_t + df.length

df.to_csv(path_save, index=False)



