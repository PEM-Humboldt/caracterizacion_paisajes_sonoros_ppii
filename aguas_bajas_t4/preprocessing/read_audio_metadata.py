#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get list of audio files and associated metadata
Author: Juan Sebastián Ulloa (julloa[at]humboldt.org.co)

"""

import pandas as pd
import matplotlib.pyplot as plt
import glob
from maad import util

#%% Set variables
path_audio = '/Volumes/MANGO/anh_aguas_bajas_t3/'
path_save = '../audio_metadata/audio_metadata_aguas_bajas_t3.csv'

#%% Get audio metadata
df = util.get_metadata_dir(path_audio, verbose=True)

#%% Post process

# include site column
df['site'] = df.fname.str.split('_').str[0]

# remove nan values
df = df.loc[~df.sample_rate.isna(),:]


#%% Check dataframe manually
df.head()
df.tail()
df.site.value_counts()  # number of recordings per site

# Verify and detect recordings with errors
df.length.value_counts()

# save dataframe to csv
df.to_csv(path_save, index=False)

#%% Plot sampling
import seaborn as sns
sns.scatterplot(x=df.date, y=df.site)
plt.xticks(rotation=15)
plt.plot(df.site)

