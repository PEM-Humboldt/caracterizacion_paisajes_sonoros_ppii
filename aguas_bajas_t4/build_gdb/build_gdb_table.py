#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Geo Database for PaisajesSonorosTB
----------------------------------------

This script compiles output from multiple scripts that should be executed previously:
    - audio_metadata
    - acoustic_indices
    - graphical_soundscapes
    - soundscape_composition
    
Note: For seasons T3 and T4, BIOFONIA, ANTROPOFONIA y GEOFONIA was not computed and hence
has a NaN value.

"""

import numpy as np
import pandas as pd
import glob
import os

#%% Load acoustic indices, graphical soundscapes, and manual annotations to build the GDB
season = 'Aguas bajas T4'
path_metadata = '../audio_metadata/audio_metadata_aguas_bajas_t4_subsample.csv'
path_indices = '../acoustic_community_characterization/acoustic_indices/dataframes/*.csv'
path_graphical_soundscapes = '../acoustic_community_characterization/graphical_soundscapes/dataframes/*.csv'

# Audio metadata
df_metadata = pd.read_csv(path_metadata)

# Acoustic indices
flist = glob.glob(path_indices)
df_indices = pd.DataFrame()
for fname in flist:
    df_indices = df_indices.append(pd.read_csv(fname))
df_indices = df_indices.loc[df_indices.fname.isin(df_metadata.fname),:]  #select only subsample

# Graphical soundscapes
flist = glob.glob(path_graphical_soundscapes)
df_graph = pd.DataFrame()
for fname in flist:
    aux = pd.read_csv(fname)
    aux.drop(columns='hour', inplace=True)
    aux = pd.Series(aux.values.ravel(), name=os.path.basename(fname)[0:-4])
    df_graph = df_graph.append(aux)
    
# Environmental data ANH_to_GXX data
df_eventID = pd.read_csv('../env_data/ANH_to_GXX_Cobertura.csv')[['sensor_name', 'eventID']]

# check consistency between data -- all results should be empty arrays
np.setdiff1d(df_indices.sensor_name.unique(), df_graph.index.unique())


#%% Process dataframes to meet GDB criteria

# Compute metadata per site
df_site_metadata = pd.DataFrame()
for site_idx, site in df_metadata.groupby('site'):
    site_metadata = pd.Series({'sensor_name': site_idx,
                               'TASA_MUEST': site['sample_rate'].unique()[0].astype(int),
                               'RES_BITS': site['bits'].unique()[0].astype(int),
                               'MICROFONO': 'Audiomoth v1.20',
                               'REF_GRAB': 'Audiomoth v1.20',
                               'FECHA_INI': site.date.sort_values().iloc[0][0:10],
                               'FECHA_FIN': site.date.sort_values().iloc[-1][0:10], 
                               'HORA_INI': site.date.sort_values().iloc[0][11:],
                               'HORA_FIN': site.date.sort_values().iloc[-1][11:],
                               'NUM_GRAB': len(site),
                               'TASA_GRAB': '60 segundos cada 1800 segundos',
                               'ESTACIONAL': season,
                               'ALTURA': 1.5
                               })
    df_site_metadata = df_site_metadata.append(site_metadata, ignore_index=True)

# Acoustic indices per site
df_site_indices = pd.DataFrame()
for site_idx, site in df_indices.groupby('sensor_name'):
    site_indices = pd.Series({'sensor_name': site_idx,
                              'ACI_Q25': site.ACI.quantile(q=0.25),
                              'ACI_Q50': site.ACI.quantile(q=0.5),
                              'ACI_Q75': site.ACI.quantile(q=0.75),
                              'ADI_Q25': site.ADI.quantile(q=0.25),
                              'ADI_Q50': site.ADI.quantile(q=0.5),
                              'ADI_Q75': site.ADI.quantile(q=0.75),
                              'NDSI_Q25': site.NDSI.quantile(q=0.25),
                              'NDSI_Q50': site.NDSI.quantile(q=0.5),
                              'NDSI_Q75': site.NDSI.quantile(q=0.75),
                              'BIO_Q25': site.BI.quantile(q=0.25),
                              'BIO_Q50': site.BI.quantile(q=0.5),
                              'BIO_Q75': site.BI.quantile(q=0.75),
                              'AEI_Q25': site.H.quantile(q=0.25),
                              'AEI_Q50': site.H.quantile(q=0.5),
                              'AEI_Q75': site.H.quantile(q=0.75),
                              'NP_Q25': site.NP.quantile(q=0.25),
                              'NP_Q50': site.NP.quantile(q=0.5),
                              'NP_Q75': site.NP.quantile(q=0.75),
                              'SC_Q25': site.SC.quantile(q=0.25),
                              'SC_Q50': site.SC.quantile(q=0.5),
                              'SC_Q75': site.SC.quantile(q=0.75),
                              'HF_Q25': site.Hf.quantile(q=0.25),
                              'HF_Q50': site.Hf.quantile(q=0.5),
                              'HF_Q75': site.Hf.quantile(q=0.75),
                              'HT_Q25': site.Ht.quantile(q=0.25),
                              'HT_Q50': site.Ht.quantile(q=0.5),
                              'HT_Q75': site.Ht.quantile(q=0.75),
                              'ASU': (df_graph.loc[site_idx,:]>0).sum()/df_graph.shape[1]
                              })
    df_site_indices = df_site_indices.append(site_indices, ignore_index=True)

df_eventID.rename(columns={'eventID': 'ID_MUEST_PT'}, inplace=True)

#%% Build GDB
df_gdb = df_eventID.merge(df_site_metadata, on='sensor_name')
df_gdb = df_gdb.merge(df_site_indices, on='sensor_name')

# Note: For seasons T3 and T4, BIOFONIA, ANTROPOFONIA y GEOFONIA was not computed and hence
# has a NaN value.
df_gdb['BIOFONIA'] = np.nan
df_gdb['GEOFONIA'] = np.nan
df_gdb['ANTROPOFONIA'] = np.nan

# save to disk
df_gdb.to_csv('./dataframes/gdb_site.csv', index=False)