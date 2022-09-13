library(lme4)
library(MuMIn)

df = read.csv('./dataframes/allsites_acoustic_indices_env.csv', sep=',')

# prepare data
# testing purposes --------- keep only more different and representative groups 'Palma' and 'Bosque Ripario'
df['period'] = 'day'
df$period[(df$time<6) | (df$time>18)] = 'night'
df$time = factor(df$time)
df$period = factor(df$period)
df['day'] = factor(substr(df$date, 0, 10))
df = df[is.element(df$Cobertura, c('Palma', 'Bosque Ripario')),]
df$Cobertura = factor(df$Cobertura)
df = df[df$proba_rain<0.5,]

# modelo
options(na.action = "na.omit")
all.mixed.gb=lmer(BI ~ (1|sensor_name) + time + Cobertura, data = df, REML = F)
options(na.action = "na.fail")
all.mixed.gb.dredge=dredge(all.mixed.gb)
all.mixed.gb.dredge  # el mejor modelo incluye class, year, class:year y está a más de 4 deltas del segundo mejor modelo. Y tiene un peso muy cerca a 1. Es un buen modelo y nos podemos quedar con el

# Si  el modelo full es mucho mejor (delta > 4) corremos el modelo
res.lmer = lmer(BI ~ (1|sensor_name) + time + Cobertura, data = df, REML = F)

## 2 - Diagnósticos
plot(res.lmer)
qqnorm(resid(res.lmer))

## 3 - revisar intervalos de confianza
summary(res.lmer)
confint(res.lmer)

# Si el modelo nulo es mejor que el full (delta < 4)
res.lmer.avg = model.avg(all.mixed.gb.dredge, subset = delta < 4)  # model averga si un sólo mdelo no está a más de 4 deltas
summary(res.lmer.avg) # verificar si la variable es significativa
confint(res.lmer.avg)
