#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
During this period (t3), recorders where left for a longer period (50-60 days). 
Other sampling periods (t1, t2, t4) had between 18 and 20  days.
In order to compmare the results, we will take a subsample of 20 days per site.
"""

import pandas as pd

num_rec_perday = 48
num_days = 20
flist_full = pd.read_csv('../audio_metadata/audio_metadata_aguas_bajas_t2.csv')
flist_full['date_fmt'] = pd.to_datetime(flist_full.date,  format='%Y-%m-%d %H:%M:%S')

# select sites
sites = flist_full.site.unique().tolist()
#remove sites with triggered recordings and less than 10 days of recordings

rm_sites = {'G6611', 'G6594', 'G6585', 'G6611', 'G6597', 'G6594', 'G6598', 'G030'}  
sites = [e for e in sites if e not in rm_sites]

# Loop through sites
flist_subsample = pd.DataFrame()
for site in sites:
    flist = flist_full.loc[flist_full.site==site,:]
    flist = flist.sort_values('date_fmt')
    flist = flist.groupby(flist.date_fmt.dt.dayofyear).filter(lambda x:len(x)==num_rec_perday)
    flist = flist.iloc[0:num_days*num_rec_perday,:]
    flist_subsample = flist_subsample.append(flist)

#%% Validate output
import seaborn as sns
import matplotlib.pyplot as plt
plt.close('all')
sns.scatterplot(x=flist_subsample.site.value_counts(), y=flist_subsample.site.value_counts().index)
sns.scatterplot(x=flist_subsample.date_fmt.dt.dayofyear, y=flist_subsample.site, alpha=0.8)

# length between first and last sample
for site in sites:
    flist = flist_subsample.loc[flist_full.site==site,:]
    flist = flist.sort_values('date_fmt')
    print(flist.date_fmt.iloc[-1]-flist.date_fmt.iloc[0])

#%% save
flist_subsample.to_csv('../audio_metadata/audio_metadata_aguas_bajas_t2_subsample.csv', index=False)