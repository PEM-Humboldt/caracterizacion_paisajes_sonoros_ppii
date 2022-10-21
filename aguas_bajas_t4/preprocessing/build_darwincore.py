#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


#%% Set variables and load data
path_sensor_deployment = '../sensor_deployment/sensor_deployment_t4.xlsx'
path_audio_metadata = '../audio_metadata/audio_metadata_aguas_bajas_t4.csv'
path_env_data = '../env_data/ANH_to_GXX_Cobertura.csv'
path_save = '../audio_metadata/I2D-BIO_aguas_bajas_t4.xlsx'

# load data
df_sensor_deployment = pd.read_excel(path_sensor_deployment)
df_audio_metadata = pd.read_csv(path_audio_metadata)
df_env = pd.read_csv(path_env_data)

# check consistency between data -- all results should be empty arrays
np.setdiff1d(df_audio_metadata.sensor_name.unique(), df_sensor_deployment.sensor_name.unique())
np.setdiff1d(df_sensor_deployment.sensor_name.unique(), df_env.sensor_name.unique())
np.setdiff1d(df_audio_metadata.sensor_name.unique(), df_env.sensor_name.unique())

#%% 
"""
--------------------------------- Build sheet Eventos ---------------------------
"""
# Step 1. Set the fixed values
# Some columns from the DarwinCore format have the same values.



fixed_value = {
    'sampleSizeValue': 1,
    'sampleSizeUnit': 'grabadora',
    'samplingProtocol': 'Muestreo Acústico Pasivo - Grabadora automática Audiomoth',
    'samplingEffort': '1 minuto de grabación cada 30 minutos',
    'eventRemarks': 'Aguas bajas T4 | Buena',
    'continent': 'SA',
    'country': 'Colombia',
    'countryCode': 'CO',
    'stateProvince': 'Santander',
    'county': 'Puerto Wilches',
    'verbatimCoordinateSystem': 'Grados decimales',
    'verbatimSRS': 'WGS84',
    'geodeticDatum': 'WGS84',
    'coordinateUncertainty': 50,
    'minimumElevationInMeters': 50,
    'maximumElevationInMeters': 150,
    'institutionCode': 'Instituto de Investigación de Recursos Biológicos Alexander von Humboldt (IAvH)',
    'measurementType (Tipo de configuración)': 'Tipo de configuración',
    'measurementValue (Tipo de configuración)': 'Audible y ultrasonido',
    'measurementType (Altura del sensor del suelo)': 'Altura del sensor del suelo',
    'measurementValue (Altura del sensor del suelo)': '150',
    'measurementUnit (Altura del sensor del suelo)': 'cm',
    'measurementType (Presión sonora N)': 'Presión sonora N',
    'measurementUnit (Presión sonora N)': 'dBA',    
    'measurementType (Presión sonora S)': 'Presión sonora S',
    'measurementUnit (Presión sonora S)': 'dBA',
    'measurementType (Presión sonora E)': 'Presión sonora E',
    'measurementUnit (Presión sonora E)': 'dBA',
    'measurementType (Presión sonora W)': 'Presión sonora W',
    'measurementUnit (Presión sonora W)': 'dBA',
    'measurementType (Frecuencia de muestreo)': 'Frecuencia de muestreo',
    'measurementUnit (Frecuencia de muestreo)': 'kHz',
    'measurementType (Profundidad en bits)': 'Profundidad en bits',
    'measurementValue (Profundidad en bits)': 16,
    'measurementUnit (Profundidad en bits)': 'bits',
    }


#%% Step 2. Set Variable values
# Merge metadata and sensor deployment information


# get start-end dates
df_dates = pd.DataFrame()
for sensor_name, df_sensor in df_audio_metadata.groupby('sensor_name'):
    df_sensor.sort_values('date', inplace=True)
    df_dates = df_dates.append({
        'sensor_name': sensor_name,
        'sample_rate': int(df_sensor.sample_rate.iloc[0]),
        'bit_depth': int(df_sensor.bits.iloc[0]),
        'date_ini': df_sensor.date.iloc[0][0:10],
        'date_end': df_sensor.date.iloc[-1][0:10],
        'time_ini': df_sensor.date.iloc[0][11:19],
        'time_end': df_sensor.date.iloc[-1][11:19]
        }, ignore_index=True)

# merge dataframes
df_merge = df_env.merge(df_sensor_deployment, on='sensor_name')
df_merge = df_merge.merge(df_dates, on='sensor_name')

# format audio_metadata for event sheet
variable_value = pd.DataFrame({
    'eventID1': df_merge['sensor_name'],
    'parentEventID': df_merge['eventID_x'],
    'eventDate': df_merge['date_ini'] + '/' + df_merge['date_end'],
    'eventTime': df_merge['time_ini'] + '/' + df_merge['time_end'],
    'habitat': df_merge['Cobertura'],
    'verbatimLatitude': df_merge['decimalLat'],
    'verbatimLongitude': df_merge['decimalLon'],
    'decimalLatitude': df_merge['decimalLat'],
    'decimalLongitude': df_merge['decimalLon'],
    'locality': df_merge['Plataf'],
    'measurementValue (Frecuencia de muestreo)': df_merge.sample_rate.astype(int),
    'measurementValue (Profundidad en bits)': df_merge.bit_depth.astype(int),
    'measurementValue (Presión sonora N)': df_merge['Ruido 1'],
    'measurementValue (Presión sonora S)': df_merge['Ruido 2'],
    'measurementValue (Presión sonora E)': df_merge['Ruido 3'],
    'measurementValue (Presión sonora W)': df_merge['Ruido 4']
    })

#%% Step 3. Merge fixed and variable values into an excel sheet

eventos = pd.DataFrame({
('ID grabadora', 'eventID1'): variable_value['eventID1']+'_T4',
('Unidad de muestreo', 'parentEventID'): variable_value['parentEventID'],
(' ', 'sampleSizeValue'): fixed_value['sampleSizeValue'],
(' ', 'sampleSizeUnit'): fixed_value['sampleSizeUnit'],
(' ', 'samplingProtocol'): fixed_value['samplingProtocol'],
(' ', 'samplingEffort'): fixed_value['samplingEffort'],
('Fecha', 'eventDate'): variable_value['eventDate'],
('Hora', 'eventTime'):  variable_value['eventTime'],
('Cobertura vegetal', 'habitat'):  variable_value['habitat'],
(' ', 'eventRemarks'):  fixed_value['eventRemarks'],
(' ', 'continent'): fixed_value['continent'],
(' ', 'country'):  fixed_value['country'],
(' ', 'countryCode'): fixed_value['countryCode'],
(' ', 'stateProvince'): fixed_value['stateProvince'],
(' ', 'county'): fixed_value['county'],
('Localidad', 'locality'): variable_value['locality'], 
(' ', 'minimumElevationInMeters'): fixed_value['minimumElevationInMeters'],
(' ', 'maximumElevationInMeters'): fixed_value['maximumElevationInMeters'],
('Latitud', 'verbatimLatitude'): variable_value['verbatimLatitude'],
('Longitud', 'verbatimLongitude'): variable_value['verbatimLongitude'],
(' ', 'verbatimCoordinateSystem'): fixed_value['verbatimCoordinateSystem'],
(' ', 'verbatimSRS'): fixed_value['verbatimSRS'],
(' ', 'decimalLatitude'): variable_value['verbatimLatitude'],
(' ', 'decimalLongitude'): variable_value['verbatimLongitude'],
(' ', 'geodeticDatum'): fixed_value['geodeticDatum'],
(' ', 'coordinateUncertainty'): fixed_value['coordinateUncertainty'],
(' ', 'institutionCode'): fixed_value['institutionCode'],
(' ', 'measurementType (Tipo de configuración)'): fixed_value['measurementType (Tipo de configuración)'],
('Configuración', 'measurementValue (Tipo de configuración)'): fixed_value['measurementValue (Tipo de configuración)'],
(' ', 'measurementType (Altura del sensor del suelo)'): fixed_value['measurementType (Altura del sensor del suelo)'],
('Altura del sensor del suelo', 'measurementValue (Altura del sensor del suelo)'): fixed_value['measurementValue (Altura del sensor del suelo)'],
(' ', 'measurementUnit (Altura del sensor del suelo)'): fixed_value['measurementUnit (Altura del sensor del suelo)'],
(' ', 'measurementType (Presión sonora N)'): fixed_value['measurementType (Presión sonora N)'],
(' ', 'measurementValue (Presión sonora N)'): variable_value['measurementValue (Presión sonora N)'],
(' ', 'measurementUnit (Presión sonora N)'): fixed_value['measurementUnit (Presión sonora N)'],
(' ', 'measurementType (Presión sonora S)'): fixed_value['measurementType (Presión sonora S)'],
(' ', 'measurementValue (Presión sonora S)'): variable_value['measurementValue (Presión sonora S)'],
(' ', 'measurementUnit (Presión sonora S)'): fixed_value['measurementUnit (Presión sonora S)'],
(' ', 'measurementType (Presión sonora E)'): fixed_value['measurementType (Presión sonora E)'],
(' ', 'measurementValue (Presión sonora E)'): variable_value['measurementValue (Presión sonora E)'],
(' ', 'measurementUnit (Presión sonora E)'): fixed_value['measurementUnit (Presión sonora E)'],
(' ', 'measurementType (Presión sonora W)'): fixed_value['measurementType (Presión sonora W)'],
(' ', 'measurementValue (Presión sonora W)'): variable_value['measurementValue (Presión sonora W)'],
(' ', 'measurementUnit (Presión sonora W)'): fixed_value['measurementUnit (Presión sonora W)'],
(' ', 'measurementType (Frecuencia de muestreo)'): fixed_value['measurementType (Frecuencia de muestreo)'],
(' ', 'measurementValue (Frecuencia de muestreo)'): variable_value['measurementValue (Frecuencia de muestreo)'],
(' ', 'measurementUnit (Frecuencia de muestreo)'): fixed_value['measurementUnit (Frecuencia de muestreo)'],
(' ', 'measurementType (Profundidad en bits)'): fixed_value['measurementType (Profundidad en bits)'],
(' ', 'measurementValue (Profundidad en bits)'): variable_value['measurementValue (Profundidad en bits)'],
(' ', 'measurementUnit (Profundidad en bits)'): fixed_value['measurementUnit (Profundidad en bits)']
                                                   }).drop_duplicates().fillna("noData")


#%% 
"""
----------------------------- Build sheet registros --------------------------------
"""

#% Step 1. Set fixed values (see above)

#%% Step 2. Set variable values
df_registros = df_audio_metadata.merge(df_env, on='sensor_name')

# change local file location by NAS location
df_registros['path_audio'] = df_registros['path_audio'].str.replace(
        '/Volumes/Humboldt/',
        'http://190.25.232.2:780/cgi-bin/Sonidos/Aguas bajas T4/audios_monitoreo_acustico_pasivo/')

df_registros['path_audio'] = df_registros['path_audio'].str.replace(
        '/Volumes/Humboldt/',
        'http://190.25.232.2:780/cgi-bin/Sonidos/Aguas bajas T4/audios_monitoreo_acustico_pasivo/')


#%%
registros = pd.DataFrame({
('ID grabadora', 'eventID1'):  df_registros['sensor_name']+'_T4',
('Nombre del archivo', 'eventID'):  df_registros['fname'],
('Unidad de muestreo', 'parentEventID'):  df_registros['eventID'],
('Sonido', 'type'):  'Sonido',
('Duración', 'sampleSizeValue'):  df_registros['length'],
('Duración unidades', 'sampleSizeUnit'):  'segundos',
('Tipo de muestreo y marca de la grabadora', 'samplingProtocol'): fixed_value['samplingProtocol'],
('Programación grabadora', 'samplingEffort'): fixed_value['samplingEffort'],
('Fecha', 'eventDate'):  df_registros.date.str[0:10],
('Hora', 'eventTime'): df_registros.date.str[11:19],
('Habitat', 'habitat'): df_registros['Cobertura'],
('Nombre coordinador(a)', 'eventRemarks'): 'Muestreo coordinado por: Daniela Martínez y Juan Sebastián Ulloa',
('Continente', 'continent'):  fixed_value['continent'],
('País','country'):  fixed_value['country'],
('País código', 'countryCode'):  fixed_value['countryCode'],
('Departamento', 'stateProvince'): fixed_value['stateProvince'],
('Municipio', 'county'):  fixed_value['county'],
('Nombre completo del punto de muestreo', 'locality'):  df_registros['Plataf'],
(' ', 'minimumElevationInMeters'):  fixed_value['minimumElevationInMeters'],
(' ', 'maximumElevationInMeters'):  fixed_value['maximumElevationInMeters'],
('Latitud', 'verbatimLatitude'):  df_registros['decimalLat'],
('Longitud', 'verbatimLongitude'):  df_registros['decimalLon'],
('Unidades (grados decimales)', 'verbatimCoordinateSystem'):  fixed_value['verbatimCoordinateSystem'],
('WGS84', 'verbatimSRS'):  fixed_value['verbatimSRS'],
('??', 'decimalLatitude'):  df_registros['decimalLat'],
('??', 'decimalLongitude'):  df_registros['decimalLon'],
('??', 'geodeticDatum'):  fixed_value['verbatimSRS'],
(' ', 'coordinateUncertaintyInMeters'):  fixed_value['coordinateUncertainty'],
('Instituto de Investigación de Recursos Biológicos Alexander von Humboldt (IAvH)', 'institutionCode')  :"Instituto de Investigación de Recursos Biológicos Alexander von Humboldt (IAvH)",
(' ', 'title')                                                                      :df_registros['fname'],
('Formato archivo', 'format'): '.wav',
('Enlace a Colección', 'identifier'):  df_registros['path_audio'],
('Fecha creación', 'created'):  df_registros['date'],
('Persona que colectó el dato', 'creator'):  'Hoover Pantoja',
(' ', 'measurementType (Tipo de configuración)'):  "Tipo de configuración",
('Configuración', 'measurementValue (Tipo de configuración)'):  fixed_value['measurementValue (Tipo de configuración)'],
(' ', 'measurementType (Altura del sensor del suelo)'):  "Altura del Suelo",
('Altura del sensor del suelo', 'measurementValue (Altura del sensor del suelo)'):  "150",
(' ', 'measurementUnit (Altura del sensor del suelo)'):  "cm",
(' ', 'measurementType (Frecuencia de muestreo)'):  "Frecuencia de muestreo",
(' ', 'measurementValue (Frecuencia de muestreo)'):  df_registros['sample_rate'].astype(int),
(' ', 'measurementUnit (Frecuencia de muestreo)'):  "Hz",
(' ', 'measurementType (Profundidad en bits)'):  "Profundidad en bits",
(' ', 'measurementValue (Profundidad en bits)'):  df_registros['bits'].astype(int),
(' ', 'measurementUnit (Profundidad en bits)'):'bits'
}).drop_duplicates().dropna(subset=[('Nombre del archivo', 'eventID')])


#%% Write to excel file
with pd.ExcelWriter(path_save) as writer:
    eventos.to_excel(writer, sheet_name='Eventos')
    registros.to_excel(writer, sheet_name='Registros')


