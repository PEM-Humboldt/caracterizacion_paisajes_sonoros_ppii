# COMPUTE NMDS AND PLOT RESULT
library(vegan)
library(ade4)
library(RColorBrewer)
library(ggplot2)

## ----------- CHECK AND PLOT FOR A SINGLE SEASON -------------  ##
# Load data
df = read.csv('./dataframes/tfbins_aguas_bajas_t4.csv')
#rm_sites = c('G003', 'G060', 'G068', 'G098')  # aguas bajas t2
#rm_sites = c('G012', 'G021', 'G051', 'G068', 'G083')  # aguas bajas t3
rm_sites =  c('G005','G012','G068', 'G083', 'G024') # aguas bajas t4

df = df[!(df$sensor_name) %in% (rm_sites),]

tfbins = df[paste('X', 0:3071, sep='')]
# Compute NMDS
tfbins_nmds = metaMDS(tfbins, distance = 'bray', trymax = 500)
stressplot(tfbins_nmds)  # validate model fit
tfbins_nmds$stress

# Plot results in 2D space
colors = RColorBrewer::brewer.pal(6, 'Dark2')
plt_data = as.data.frame(tfbins_nmds$points)
plt_data['sensor_name'] = df$sensor_name
plt_data['Cobertura'] = df$Cobertura
plot(plt_data[c('MDS1', 'MDS2')], col='gray', pch=16, bty='n',xlab='NMDS 1', ylab='NMDS 2', cex=0.5, cex.lab=1)
text(plt_data$MDS1, plt_data$MDS2, labels = plt_data$sensor_name, cex=0.8, col='gray50')
abline(v=0,col='gray',lty=2);abline(h=0,col='gray',lty=2)
s.class(plt_data[c('MDS1', 'MDS2')], fac=factor(plt_data$Cobertura), col = colors, add.plot = T)

## -------- CHECK AND PLOT FOR SEASONS T1 AND T2 -------------  ##

# Load data
df_t1 = read.csv('./dataframes/tfbins_aguas_altas_t1.csv')
df_t1['temporada'] = 'T1'
df_t1 = df_t1[!(df_t1$sensor_name) %in% c('G005'),]

df_t2 = read.csv('./dataframes/tfbins_aguas_bajas_t2.csv')
df_t2['temporada'] = 'T2'
df_t2 = df_t2[!(df_t2$sensor_name) %in% c('G003', 'G060', 'G068', 'G098'),]


df = rbind(df_t1, df_t2)
tfbins = df[paste('X', 0:3071, sep='')]
# Compute NMDS
tfbins_nmds = metaMDS(tfbins, distance = 'bray', trymax = 500)
stressplot(tfbins_nmds)  # validate model fit
tfbins_nmds$stress

nmds_data = as.data.frame(tfbins_nmds$points)
nmds_data['sensor_name'] = df$sensor_name
nmds_data['Cobertura'] = df$Cobertura
nmds_data['temporada'] = df$temporada
nmds_data['eventID'] = df$eventID

# save nmds data
write.csv(nmds_data, './dataframes/nmds_data_t1_t2.csv', row.names=FALSE)

# Use a non parametric test to evaluate significance of the groups
dist = vegdist(nmds_data[c('MDS1', 'MDS2')], 'euclidean') # using 2D data
adonis(dist~nmds_data$Cobertura, permutations = 1000)
adonis(dist~nmds_data$temporada, permutations = 1000)

## -- Find Indicator Bins -- ##
# combine data frames with environmental data
#tf_bins_df = as.data.frame(tf_bins_nmds$points)
#tf_bins_df['sensor_name'] = substr(row.names(tf_bins_df), 1, 4) 
#tf_bins_df = merge(tf_bins_df, env, by.x = 'sensor_name', by.y='sensor_name')
tf_bins_presence = tfbins[,colSums(tfbins)>0]  # select only columns with no zeros

# Determine de groups
cover = nmds_data$Cobertura
idx_keep = is.element(cover, c('Bosque Ripario', 'Herbazales', 'Palma'))
tf_bins_presence = tf_bins_presence[idx_keep,]
cover = factor(cover[idx_keep])

# Compute indicator species index
library(labdsv)
iva = indval(tf_bins_presence, as.numeric(cover))

gr = iva$maxcls[iva$pval<=0.05]
gr = levels(cover)[gr]
iv = iva$indcls[iva$pval<=0.05]
pv = iva$pval[iva$pval<=0.05]
fr = apply(tf_bins_presence>0, 2, sum)[iva$pval<=0.05]
fidg = data.frame(group=gr, indval=iv, pvalue=pv, freq=fr)
fidg = fidg[order(fidg$group, -fidg$indval),]
fidg['tf_bin'] = row.names(fidg)
write.csv(fidg, './dataframes/indicator_species_indval_t1_t2.csv', row.names = FALSE)


# ------------------------- PLOT RESULTS --------------- #
# Plot results in 2D space
colors = RColorBrewer::brewer.pal(6, 'Dark2')
plt_data = nmds_data

# puntos de muestreo
plot(plt_data[c('MDS1', 'MDS2')], col='gray', pch=16, bty='n',xlab='NMDS 1', ylab='NMDS 2', cex=0.9, cex.lab=1)
abline(v=0,col='gray',lty=2);abline(h=0,col='gray',lty=2)
text(plt_data$MDS1, plt_data$MDS2, labels = plt_data$sensor_name, cex=0.8, col='gray50')

ggplot(plt_data, aes(x=MDS1, y=MDS2) ) +
  geom_point(colour='gray') +
  geom_density_2d() +
  xlab('NMDS1') +
  ylab('NMDS1')


# cobertura
plot(plt_data[c('MDS1', 'MDS2')], col='gray', pch=16, bty='n',xlab='NMDS 1', ylab='NMDS 2', cex=0.5, cex.lab=1)
abline(v=0,col='gray',lty=2);abline(h=0,col='gray',lty=2)
s.class(plt_data[c('MDS1', 'MDS2')], fac=factor(plt_data$Cobertura), col = colors, add.plot = T)

# temparada
plot(plt_data[c('MDS1', 'MDS2')], col='gray', pch=16, bty='n',xlab='NMDS 1', ylab='NMDS 2', cex=0.5, cex.lab=1)
abline(v=0,col='gray',lty=2);abline(h=0,col='gray',lty=2)
s.class(plt_data[c('MDS1', 'MDS2')], fac=factor(plt_data$temporada), col = colors, add.plot = T)

# Cobertura y temparada
for(cobertura_sel in unique(plt_data$Cobertura)){
  #cobertura_sel = 'Bosque Abierto'
  plot(plt_data[c('MDS1', 'MDS2')], col='gray', pch=16, bty='n',xlab='NMDS 1', ylab='NMDS 2', cex=0.5, cex.lab=1)
  abline(v=0,col='gray',lty=2);abline(h=0,col='gray',lty=2)
  s.class(plt_data[plt_data$Cobertura==cobertura_sel, c('MDS1', 'MDS2')], 
          fac=factor(plt_data$temporada[plt_data$Cobertura==cobertura_sel]), 
          col = colors, add.plot = T)
  title(main=cobertura_sel)
}


## -------- CHECK AND PLOT FOR SEASONS T1-T2-T3-T4 -------------  ##

# Load data
df_t1 = read.csv('./dataframes/tfbins_aguas_altas_t1.csv')
df_t1['temporada'] = 'T1'
df_t1 = df_t1[!(df_t1$sensor_name) %in% c('G005'),]

df_t2 = read.csv('./dataframes/tfbins_aguas_bajas_t2.csv')
df_t2['temporada'] = 'T2'
df_t2 = df_t2[!(df_t2$sensor_name) %in% c('G003', 'G060', 'G068', 'G098'),]

df_t3 = read.csv('./dataframes/tfbins_aguas_bajas_t3.csv')
df_t3['temporada'] = 'T3'
df_t3 = df_t3[!(df_t3$sensor_name) %in% c('G012', 'G021', 'G051', 'G068', 'G083'),]

df_t4 = read.csv('./dataframes/tfbins_aguas_bajas_t4.csv')
df_t4['temporada'] = 'T4'
df_t4 = df_t4[!(df_t4$sensor_name) %in% c('G005','G012','G068', 'G083', 'G024'),]


df = rbind(df_t1, df_t2, df_t3, df_t4)
tfbins = df[paste('X', 0:3071, sep='')]
# Compute NMDS
tfbins_nmds = metaMDS(tfbins, distance = 'bray', trymax = 500)
stressplot(tfbins_nmds)  # validate model fit
tfbins_nmds$stress

nmds_data = as.data.frame(tfbins_nmds$points)
nmds_data['sensor_name'] = df$sensor_name
nmds_data['Cobertura'] = df$Cobertura
nmds_data['temporada'] = df$temporada
nmds_data['eventID'] = df$eventID

# save nmds data
write.csv(nmds_data, './dataframes/nmds_data_t1_t2_t3_t4.csv', row.names=FALSE)

# Use a non parametric test to evaluate significance of the groups
dist = vegdist(nmds_data[c('MDS1', 'MDS2')], 'euclidean') # using 2D data
adonis(dist~nmds_data$Cobertura, permutations = 1000)
adonis(dist~nmds_data$temporada, permutations = 1000)

# Plot results in 2D space
colors = RColorBrewer::brewer.pal(6, 'Dark2')
plt_data = nmds_data

# puntos de muestreo
plot(plt_data[c('MDS1', 'MDS2')], col='gray', pch=16, bty='n',xlab='NMDS 1', ylab='NMDS 2', cex=0.9, cex.lab=1)
abline(v=0,col='gray',lty=2);abline(h=0,col='gray',lty=2)
text(plt_data$MDS1, plt_data$MDS2, labels = plt_data$sensor_name, cex=0.8, col='gray50')

ggplot(plt_data, aes(x=MDS1, y=MDS2) ) +
  geom_point(colour='gray') +
  geom_density_2d() +
  xlab('NMDS1') +
  ylab('NMDS1')


# cobertura
plot(plt_data[c('MDS1', 'MDS2')], col='gray', pch=16, bty='n',xlab='NMDS 1', ylab='NMDS 2', cex=0.5, cex.lab=1)
abline(v=0,col='gray',lty=2);abline(h=0,col='gray',lty=2)
s.class(plt_data[c('MDS1', 'MDS2')], fac=factor(plt_data$Cobertura), col = colors, add.plot = T)

# temparada
plot(plt_data[c('MDS1', 'MDS2')], col='gray', pch=16, bty='n',xlab='NMDS 1', ylab='NMDS 2', cex=0.5, cex.lab=1)
abline(v=0,col='gray',lty=2);abline(h=0,col='gray',lty=2)
s.class(plt_data[c('MDS1', 'MDS2')], fac=factor(plt_data$temporada), col = colors, add.plot = T)

# Cobertura y temparada
for(cobertura_sel in unique(plt_data$Cobertura)){
  #cobertura_sel = 'Bosque Abierto'
  plot(plt_data[c('MDS1', 'MDS2')], col='gray', pch=16, bty='n',xlab='NMDS 1', ylab='NMDS 2', cex=0.5, cex.lab=1)
  abline(v=0,col='gray',lty=2);abline(h=0,col='gray',lty=2)
  s.class(plt_data[plt_data$Cobertura==cobertura_sel, c('MDS1', 'MDS2')], 
          fac=factor(plt_data$temporada[plt_data$Cobertura==cobertura_sel]), 
          col = colors, add.plot = T)
  title(main=cobertura_sel)
}

