#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add prefix to Audacity audio files

@author: jsulloa
"""


import os
import glob

#%%

flist = glob.glob('/Volumes/lacie_exfat/G001/*.WAV')

#%% Double check that names do not have prefix

for fname in flist.copy():
    basename = os.path.basename(fname)
    if len(basename.split('_')) > 2:
        flist.remove(fname)
        print('File removed from list', basename)

    
#%% Loop and change names

for fname in flist:
    prefix = os.path.basename(os.path.dirname(fname))
    fname_new = os.path.join(os.path.dirname(fname), prefix + '_' + os.path.basename(fname))
    os.rename(fname, fname_new)