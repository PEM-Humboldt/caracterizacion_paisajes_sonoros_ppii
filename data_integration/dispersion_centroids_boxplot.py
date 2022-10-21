#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 10:03:18 2022

@author: jsulloa
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial import distance

df = pd.read_csv('./dataframes/nmds_data_t1_t2_t3_t4.csv')

# Compute centroid for each cover type
covers = ['Bosque Ripario', 'Palma', 'Herbazales', 'Pastos', 'Bosque Denso']
centroids = pd.DataFrame({'Cobertura': covers, 
                          'centroid_x': np.repeat(0,5),
                          'centroid_y': np.repeat(0,5)})
for cover in covers:
    df_cover = df.loc[df.Cobertura==cover,:]
    centroids.loc[centroids.Cobertura==cover, 'centroid_x'] = df_cover.NMDS1.mean()
    centroids.loc[centroids.Cobertura==cover, 'centroid_y'] = df_cover.NMDS2.mean()
    
df = df.merge(centroids, on='Cobertura')

#%% Compute distance for each observation
df['dist_centroid'] = np.nan
for idx, row in df.iterrows():
    u = row[['NMDS1','NMDS2']].values
    v = row[['centroid_x','centroid_y']].values
    df.loc[idx,'dist_centroid'] = distance.euclidean(u,v)
df.to_csv('./nmds_data/nmds_data_centroids.csv', index=False)

#%% Statistical evaluation
import statsmodels.api as sm
from statsmodels.formula.api import ols
# Ordinary Least Squares (OLS) model
model = ols('dist_centroid ~ C(Cobertura)', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
anova_table
# The p value obtained from ANOVA analysis is significant (p < 0.05), and therefore, we conclude that there are significant differences among treatments.
#%% Plot
colors = {'Palma': '#66A61E',
          'Herbazales': '#E7298A',
          'Bosque Ripario': '#7570B3',
          'Pastos': '#E6AB02',
          'Bosque Denso': '#D95F02',
          'Bosque Abierto': '#1B9E77'}

fig, ax = plt.subplots(figsize=(8,5))
sns.boxplot(x='Cobertura', y='dist_centroid', data=df,
            order=['Bosque Denso', 'Bosque Ripario', 'Herbazales', 'Palma', 'Pastos'],
            palette=colors, boxprops=dict(alpha=.5),
            fliersize=0,
            ax=ax)
ax.set_ylabel('Distancia a centroide de grupo')
sns.swarmplot(x='Cobertura', y='dist_centroid', data=df, color='gray', alpha=0.5, ax=ax,
              order=['Bosque Denso', 'Bosque Ripario', 'Herbazales', 'Palma', 'Pastos'])
sns.despine(trim=True)

# statistical annotation
x1, x2 = 1, 3   # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
y, h, col = df['dist_centroid'].max() + 0.07, 0.07, 'dimgrey'
ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
ax.text((x1+x2)*.5, y+h, '*', ha='center', va='bottom', color=col)