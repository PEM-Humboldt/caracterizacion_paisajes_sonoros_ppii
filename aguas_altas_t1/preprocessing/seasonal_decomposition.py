#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Use a seasonal decomposition to evaluate if the data has trends. This analysis
helps to identify sensor or microphone failure in time.

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import

#%%
fpath_save = '../acoustic_community_caracterization/acoustic_indices/figures/seasonal_trend/'
flist = glob.glob('../acoustic_community_caracterization/acoustic_indices/dataframes/per_site/*.csv')

for fname in flist:
    df_site = pd.read_csv(fname)
    fig, ax = plt.subplots(figsize=(14,8))
    ax.plot(df_site['BI'])
    ax.set_title(fname[-16:-12])
    ax.set_ylabel('BI')
    plt.savefig(fpath_save + fname[-16:-12] + '.png')
    plt.close()