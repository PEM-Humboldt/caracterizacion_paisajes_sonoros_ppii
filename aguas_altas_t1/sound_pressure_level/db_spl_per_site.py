#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La variable de SPL depende de la hora a la cual se tomó la medida y por lo tanto
no es muy fiable.

@author: jsulloa
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#%% Load data from pam instlation
df_pam = pd.read_csv('../datos_instalacion/datos_instalacion_lluvias.csv', decimal=',')
sel_cols = ['Presión sonora 1', 'Presión sonora 2', 
            'Presión sonora 3', 'Presión sonora 4',
            'Hora']

df_pam.index = df_pam['Punto de muestreo (ANH)'].str.replace('ANH', 'ANH_')
df_pam.index.name = 'eventID'
df_pam = df_pam.loc[:,sel_cols]
df_pam['spl'] = df_pam.mean(axis=1)


#%% Load data from environmental
df_env = pd.read_excel('../BDPuntosMuestreoMag2711.xlsx', sheet_name='BDPuntosMuestreoMag')
df_env = df_env.loc[df_env['GrupoBiolo'] == 'Camaras',:]
df_env.index = df_env['eventID']

#%% merge
df = df_env.merge(df_pam, on='eventID')
env_cols = ['Dis_CP', 'Dis_Oleodu', 'Dis_Pozo', 'Dis_Pozact', 'Dis_ViaPri', 'Dia_ViaSec',
            'Dis_Ferroc', 'Dis_Kale', 'Dis_Plater', 'Tam_Parche', 'Dis_PlatEf',
            'DisBosque', 'Dis_CobNat', 'Dis_Cienag', 'Dis_MGSG', 'Dis_Dre345', 'spl']

# Compute the correlation matrix
corr = df.loc[:,env_cols].corr()

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})