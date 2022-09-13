#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rename files that have a delay of some hours in a recording.
Usually is due to an issue when configuring the sensors.

"""
import pandas as pd
import os
import glob

#%% Set variables
path_dir = '/Volumes/PAPAYA/ANH/G095/'
delay_hours = 5

flist = glob.glob(os.path.join(path_dir, '*.WAV'))

#%% Apply to all files in directory
for fname in flist:
    fname_orig = os.path.basename(fname)
    date_orig = pd.to_datetime(fname_orig[5:-4], format='%Y%m%d_%H%M%S')
    
    date_fixed = date_orig - pd.Timedelta(hours=delay_hours)
    fname_fixed = fname_orig[0:5] + date_fixed.strftime('%Y%m%d_%H%M%S') + fname_orig[-4:]
    
    os.rename(src=fname, 
              dst=os.path.join(os.path.dirname(fname), fname_fixed))
