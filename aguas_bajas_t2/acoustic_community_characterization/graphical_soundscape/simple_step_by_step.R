# Simple step by step
## Load libraries
library(viridis)
library(tuneR)
library(seewave)
source('graph_soundscape_fcns.R')

# Set variables 
path_audio_dataset = '/Volumes/PAPAYA/ANH/'  # location of audio dataset
path_save_gs = './dataframes/G001.csv'  # location to save the dataframe
path_metadata = '../../../audio_metadata/audio_metadata_lluvias.csv'  # location to metadata information
path_save_fig = './figures/G001.png'  # location to save the figure
# -----------------

# Read metadata
df = read.csv(path_metadata)
df$path_audio = paste(path_audio_dataset, df$path_audio, sep='')
df$time = format(strptime(df$date, format = "%Y-%m-%d %H:%M:%S"), format = "%H:%M:%S")
## --- testing purposes -- #
df = df[df$sensor_name=='G006',]
df = df[1:(48*5),]

# Set threshold for graphical soundscape
s = readWave(df$path_audio[31])
s = resamp(s, g=48000, output = 'Wave')
mspec = meanspec(s, wl = 256, wn = 'hanning', norm = F, plot=T)
peaks = fpeaks(mspec, threshold = 50, freq = 0, plot=T)

# Compute graphical soundscape
gs = graphical_soundscape(df, spec_wl=256, fpeaks_th=50, fpeaks_f=0, verbose=T)
plot_graphical_soundscape(gs)

# Save dataframe and plot
write.csv(gs, file=path_save_gs, row.names = F)
png(path_save_fig)
plot_graphical_soundscape_v2(gs)
dev.off()