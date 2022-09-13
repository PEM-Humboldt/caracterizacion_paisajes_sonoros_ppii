# Evaluate dispersion differences between covers
df_disp = read.csv('./nmds_data/nmds_data_centroids.csv')
df_disp$Cobertura = factor(df_disp$Cobertura)
fit_disp = aov(dist_centroid ~ Cobertura, data=df_disp)
plot(fit_disp$residuals)
summary(fit_disp)

# Post hoc tuckey to assess where the difference is
posthoc <- TukeyHSD(x=fit_disp, 'Cobertura', conf.level=0.95)
plot(posthoc)

# Evaluate which environmental variable has more effect in the graphical soundscape.
df = read.csv('./nmds_data/nmds_data.csv')
df_env = read.csv('../../env_data/ANH_to_GXX.csv')
df = merge(df, env, by.x = 'sensor_name', by.y='sensor_name')

colnames(df)
env_var = c('Dis_CP', 'Dis_Oleodu', 'Dis_Pozo', 'Dis_ViaPri', 'Dis_MGSG', 'Dis_CobNat')
acoustic_var = c('NMDS1', 'NMDS2')
plot(df[c(env_var, acoustic_var)])
