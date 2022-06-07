## SOUNDSCAPE CHARACTERIZATION
# References
# Campos‐Cerqueira, M., et al., 2020. How does FSC forest certification affect the acoustically active fauna in Madre de Dios, Peru? Remote Sensing in Ecology and Conservation 6, 274–285. https://doi.org/10.1002/rse2.120
# Furumo, P.R., Aide, T.M., 2019. Using soundscapes to assess biodiversity in Neotropical oil palm landscapes. Landscape Ecology 34, 911–923.
# Campos-Cerqueira, M., Aide, T.M., 2017. Changes in the acoustic structure and composition along a tropical elevational gradient. JEA 1, 1–1. https://doi.org/10.22261/JEA.PNCO7I
source('graph_soundscape_fcns.R')
library(viridis)
library(vegan)

## SET VARIABLES
path_audio_dataset = '/Volumes/PAPAYA/anh_aguas_bajas/'  # location of audio dataset
path_save_gs = './dataframes/'  # location to save the dataframe
path_metadata = '../../audio_metadata/audio_metadata_aguas_bajas.csv'  # location to metadata information
path_save_fig = './figures/'  # location to save the figure
path_rain_data = '../../detection/rain_predictions.csv'

# 1. READ METADATA
df = read.csv(path_metadata)
df$path_audio = paste(path_audio_dataset, df$path_audio, sep='')
df$time = format(strptime(df$date, format = "%Y-%m-%d %H:%M:%S"), format = "%H:%M:%S")
sites = unique(df$site)

## 2. REMOVE RAIN DATA
df_rain = read.csv(path_rain_data)
th_proba = 0.5 # probability threshold to remove rain
df = merge(df, df_rain, by = 'fname_audio')
cat('Total number of files removed:', table(df$proba_rain<th_proba)[1])
cat('Proportion of files removed (in %):', table(df$proba_rain<th_proba)[1]/nrow(df)*100)
df = df[df$proba_rain<th_proba,]  # select recordings with low probability of rain

## 3. COMPUTE GRAPH SOUNDSCAPE FOR EACH RECORDING AND SAVE PLOT
for(site in sites){
    # set dataframe and compute graphical soundscape
    df_site = df[df$site==site,]
    gs = graphical_soundscape(df_site, spec_wl=256, fpeaks_th=50, fpeaks_f=0, verbose=T)
    
    # save graph soundscape
    fname_save_gs = paste(path_save_gs, site, '.csv', sep='')
    write.csv(gs, file=fname_save_gs, row.names = F)
    
    # save fig
    fname_save_fig = paste(path_save_fig, site, '.png', sep='')
    png(fname_save_fig)
    plot_graphical_soundscape(gs)
    dev.off()
    }
