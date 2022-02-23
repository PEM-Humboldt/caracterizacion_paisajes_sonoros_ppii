# COMPUTE NMDS AND PLOT RESULT
library(vegan)
library(ade4)
library(RColorBrewer)
path_gs = './dataframes/'
sites = list.files(path_gs, pattern='*.csv')

# load data and organize as a community matrix (sites as rows, soundscape component (species) as columns)
tf_bins = list()
for(site in sites){
  gs = read.csv(paste(path_gs,site,sep=''))
  tf_bins[[site]] = as.vector(t(gs[,-1]))
}

# load environmental data
env = read.csv('../../env_data/ANH_to_GXX.csv')

# list to dataframe
tf_bins = as.data.frame(do.call(rbind, tf_bins))

# Compute NMDS
tf_bins_nmds = metaMDS(tf_bins, distance = 'bray', trymax = 500)
stressplot(tf_bins_nmds)  # validate model fit
tf_bins_nmds$stress

# Plot results in 2D space
colors = RColorBrewer::brewer.pal(6, 'Dark2')
plt_data = as.data.frame(tf_bins_nmds$points)
plt_data['sensor_name'] = substr(row.names(plt_data), 1, 4) 
plt_data = merge(plt_data, env, by.x = 'sensor_name', by.y='sensor_name')

plot(plt_data[c('MDS1', 'MDS2')], col='gray', pch=16, bty='n',xlab='NMDS 1', ylab='NMDS 2', cex=0.5, cex.lab=1)
abline(v=0,col='gray',lty=2);abline(h=0,col='gray',lty=2)
s.class(plt_data[c('MDS1', 'MDS2')], fac=factor(plt_data$Cobertura), col = colors, add.plot = T)

# Use a non parametric test to evaluate significance of the groups
xdata = data.frame(x=tf_bins_nmds$points[,1], y=tf_bins_nmds$points[,2], region=factor(plt_data$Cobertura))
dist = vegdist(tf_bins, 'bray')
adonis(dist~xdata$region, permutations = 1000)

## -- Find Indicator Bins -- ##
# combine data frames with environmental data
tf_bins_df = as.data.frame(tf_bins_nmds$points)
tf_bins_df['sensor_name'] = substr(row.names(tf_bins_df), 1, 4) 
tf_bins_df = merge(tf_bins_df, env, by.x = 'sensor_name', by.y='sensor_name')
tf_bins_presence = tf_bins[,colSums(tf_bins)>0]  # select only columns with no zeros

# Determine de groups
cover = tf_bins_df$Cobertura
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
write.csv(fidg, './indicator_species_data/indval.csv', row.names = FALSE)
