#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

#%%
"""
Merge recorders and site information for Event I2D sheet

"""


# formato instalación
df_inst = pd.read_excel('../../formatos_instalacion/instalación audiomoth fase 2 (lluvias).xlsx',
                   sheet_name='Hoja1')
df_inst['latitud'] = df_inst['Latitud/Longitud (grados decimales)'].str.split(',').str[0]
df_inst['longitud'] = df_inst['Latitud/Longitud (grados decimales)'].str.split(',').str[1]

df_inst = df_inst.drop(columns=['memoria', 'encendido/custom', 'play chime (App)'])
df_inst.rename(columns={'Fecha': 'Fecha instalacion'}, inplace=True)

# formato recogida
df_recogida = pd.read_excel('../../formatos_instalacion/recogida audiomoth fase 2 (lluvias).xlsx',
                   sheet_name='Hoja1')

df_recogida = df_recogida.drop(columns=['Responsable', 
                                'Código del equipo',
                                'Hora',
                                'Quitar Baterías cam', 
                                'Copiar información de SD en carpeta  con el nombre la estación de muestreo',
                                'Limpieza de la Cámara Trampa', 
                                'Quitar Baterías Audiomoth',
                                'Copiar información de SD en carpeta  con el código de la Audiomoth',
                                'Limpieza del Audiomoth'])
df_recogida.rename(columns={'Fecha': 'Fecha recogida'}, inplace=True)

# formato variables ambientales
df_env = pd.read_excel('../../env_data/BDPuntosMuestreoMag1012.xlsx', sheet_name='BDPuntosMuestreoMag')
df_env = df_env.loc[(df_env['GrupoBiolo'] == 'Sensores Pasivos') | (df_env['GrupoBiolo'] == 'Grabadoras'),:]
df_env = df_env[['parentEven', 'Cobertura']]
df_env['Punto de muestreo (ANH)'] = df_env['parentEven'].str.replace('_', ' ')

# Merge and save
df_event = df_inst.merge(df_recogida, on='Punto de muestreo (ANH)')
df_event['eventDate'] = df_event['Fecha instalacion'].astype(str) + '/' + df_event['Fecha recogida'].astype(str)
df_event = df_event.merge(df_env, on='Punto de muestreo (ANH)')
df_event.sort_values('Código grabadora (Gxxx)', inplace=True)
df_event.to_csv('../../formatos_instalacion/instalación audiomoth fase 2 (lluvias).csv', index=False)

#%%
"""
Merge recorders and site information for Grabaciones I2D sheet

"""
path_NAS = 'http://190.25.232.2:780/cgi-bin/Sonidos/Audios_monitoreo_acustico_pasivo/'
df_event = pd.read_csv('../formatos_instalacion/instalación audiomoth fase 2 (lluvias).csv')
df_rec = pd.read_csv('../audio_metadata/audio_metadata_lluvias.csv')

# format event dataframe
df_event.rename(columns={'Código grabadora (Gxxx)': 'sensor_name'}, inplace=True)
df_event.drop(columns=['Fecha instalacion', 'Hora', 'Latitud/Longitud (grados decimales)',
                       'Fecha recogida', 'Estado del Audiomoth',
                       'Descripción de la Estación de Muestreo: cambios significativos en el sitio',
                       'eventDate'], inplace=True)

# format recordings dataframe
df_rec.drop(columns=['path_audio', 'sample.rate', 'channels', 'bits', 'samples', 'fsize',
                     'recorder_model'], inplace=True)
df_rec['eventDate'] = df_rec.date.str[0:10]
df_rec['eventTime'] = df_rec.date.str[11:]
df_rec['csa_link'] = path_NAS + df_rec.sensor_name + '/' + df_rec.fname_audio
# merge and save
df_rec = df_rec.merge(df_event, on='sensor_name')
df_rec.to_csv('../formatos_instalacion/audio_metadata_env.csv', index=False)