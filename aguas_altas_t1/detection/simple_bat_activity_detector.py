#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detect Bat Activity - simple detector

@author: jsulloa
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from maad import sound, util, rois

#%%
fname = '../fonografias/G081_20211110_223000.WAV'
fname = '/Users/jsulloa/Downloads/G081_20211110_183000.WAV'
s, fs = sound.load(fname)

plt.close('all')
rois.find_rois_cwt(s,fs, flims=(15000, 80000), tlen=0.08, th=0.001, display=True)