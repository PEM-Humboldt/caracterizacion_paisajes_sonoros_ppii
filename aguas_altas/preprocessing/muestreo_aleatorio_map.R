### Muestreo aleatorio ANH  ###

# Realiza un muestreo aleatorio de 6 grabaciones en un directorio 
# asociado a un punto de muestreo.El muestreo se restringe a cada 
# uno de los picos de actividad acústica al amanecer (05:00-08:00) y 
# atardecer (17:00-20:00) para identificar vocalizaciones de aves 
# y anfibios, y anotar presencia o ausencia de antropofonía, 
# biofonía y geofonía.

path_files = 'Dropbox/Audiolib/ML_datasets/Putumayo_2018/1k_random_samples/'

flist = list.files(path_files, recursive = F, pattern = '.WAV', ignore.case = T)
df = as.data.frame(flist)

# Make new time column
df$date = strptime(substr(df$flist, 7, 7+14), format = "%Y%m%d_%H%M%S")
df$hour = format(df$date, format = "%H")

# Filter dataframe
df_sel = df[is.element(df$hour, c('05', '06', '07', '08','17', '18', '19', '20')),]
rsample = sample(df_sel$flist, 6)

### Muestreo aleatorio ANH  -- Batch ###

# Realiza el muestreo aleatorio para una lista de puntos de muestreo. Se debe tener
# los metadatos de los archivos organizados en un archivo csv.

path_metadata = './audio_metadata/audio_metadata_lluvias.csv'
site_list = read.csv('~/Downloads/flist_sensores_ANH_por_revisar.csv')
df = read.csv(path_metadata)

# Make new time column
df$date_fmt = strptime(df$date, format='%Y-%m-%d %H:%M:%S')
df$hour = format(df$date_fmt, format = "%H")

# Filter dataframe
flist_rsample = vector()
for(sname in site_list$sensor_name){
  df_site = df[df$sensor_name==sname,]
  df_sel = df_site[is.element(df_site$hour, c('05', '06', '07', '08','17', '18', '19', '20')),]
  rsample = sample(df_sel$fname_audio, 6)
  flist_rsample = c(flist_rsample, as.character(rsample))
}

write.csv(flist_rsample, '~/Downloads/flist_rsample_ANH.csv', row.names = FALSE)



