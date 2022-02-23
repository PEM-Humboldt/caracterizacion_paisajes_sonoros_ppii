## COMPUTE MEAN DIEL PATTERN FOR EACH SITE
setwd('/Volumes/lacie_macosx/Dropbox/PostDoc/iavh/ANH-PPII/analisis_fase_2/scripts/acoustic_community_caracterization/acoustic_indices/')
df = read.csv('./dataframes/G010_indices.csv')

df['time'] = factor(substr(df$date, 11,16))
df_mean = aggregate(df$BI, by = list(df$time), FUN=mean)
plot(df_mean)