#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 16:26:42 2020

@author: jsulloa
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from maad import sound, util

## Only plot the image from audio
# settings
opt_spec = {'wl': 4096, 'ovlp': 0.5, 'fcrop': [0,30000], 'db_range': 90}
path_audio = '/Volumes/PAPAYA/ANH/pkl_data/G001_21-11-10.wav'
path_save = '../figuras/test.png'

# load
s, fs = sound.load(path_audio)
#s = np.roll(s,3050000)
# compute spectrogram
im, dt, df, ext = sound.spectrogram(s, fs, nperseg=opt_spec['wl'],cmap='viridis', 
                                    overlap=opt_spec['ovlp'], flims=opt_spec['fcrop'])
im = util.power2dB(im, db_range=opt_spec['db_range'])

# Plot
plt.rcParams.update({'font.size': 12, 'font.family': 'Arial'})
plt.close('all')
fig, ax = plt.subplots(1, 1, figsize=(15, 5))
ax.imshow(im, aspect='auto', origin='lower',
          vmin=-90, vmax=-25) # sm3


# ejes
ax.set_xticks([0, im.shape[1]/4, im.shape[1]/2, im.shape[1]/2+im.shape[1]/4, im.shape[1]])
ax.set_xticklabels(['00:00', '06:00', '12:00', '18:00', '23:59'])
ax.set_xlabel('Tiempo (horas)')
ax.set_yticks([0, im.shape[0]/3, im.shape[0]*2/3, im.shape[0]])
ax.set_yticklabels(['0', '10','20', '30'])
ax.set_ylabel('Frecuencia (kHz)')

plt.savefig(path_save, bbox_inches='tight')


# # add annotations
# #insectos
# rect = patches.Rectangle((138,100),11462,290,linewidth=1, edgecolor='white',
#                          facecolor='none',alpha=0.5, ls='--')
# ax.add_patch(rect)
# ax.text(9800, 87, 'Tettogonidos', color='white', alpha=0.8)

# #anuros
# rect = patches.Rectangle((138,400), 4762, 100, linewidth=1, edgecolor='white',
#                          facecolor='none',alpha=0.5, ls='--')
# ax.add_patch(rect)
# ax.text(5000, 448, 'anuros', color='white', alpha=0.8)

# #aves
# rect = patches.Rectangle((11895,250), 4660, 250, linewidth=1, edgecolor='white',
#                          facecolor='none',alpha=0.5, ls='--')
# ax.add_patch(rect)
# ax.text(12500, 240, 'aves', color='white', alpha=0.8)

# #chicharras
# rect = patches.Rectangle((14500,10), 4840, 210, linewidth=1, edgecolor='white',
#                          facecolor='none',alpha=0.5, ls='--')
# ax.add_patch(rect)
# ax.text(17600, 255, 'cicádidos', color='white', alpha=0.8)

# #primates
# rect = patches.Rectangle((24140,433), 700, 75, linewidth=1, edgecolor='white',
#                          facecolor='none',alpha=0.5, ls='--')
# ax.add_patch(rect)
# ax.text(23500, 431, 'primates', color='white', alpha=0.8)

# #viento
# rect = patches.Rectangle((19630,10), 3766, 490, linewidth=1, edgecolor='white',
#                          facecolor='none',alpha=0.5, ls='--')
# ax.add_patch(rect)
# ax.text(19800, 50, 'viento', color='white', alpha=0.8)