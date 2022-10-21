#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TODO: 
    - Ajustar audio metadata: G014 hace parte de T3 pero figura en T4
    - Ajustar grabaciones que están duplicadas en T3 y T4 (G037, G044)

"""

import numpy as np


df_t3 = pd.read_csv('aguas_bajas_t3/audio_metadata/audio_metadata_aguas_bajas_t3.csv')
df_t4 = pd.read_csv('aguas_bajas_t4/audio_metadata/audio_metadata_aguas_bajas_t4.csv')
df = pd.read_csv('aguas_bajas_t4/audio_metadata/audio_metadata_aguas_bajas_t4.csv')

