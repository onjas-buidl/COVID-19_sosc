library(tidyverse)
library(dplyr)
library(AER)

d <- read_csv('/Users/qitianhu/Documents/Research/Explore/COVID-19_sosc/STAT274/IVdata-1.csv')
d$tenure_bi <- as.integer(d$tenure >= 3)



summary(ivreg(xc_lockdown ~ tenure_bi + gdp2018 + gdp_per_10k  | 
                gdp2018+ gdp_per_10k  + xunshi, data = d))

summary(ivreg(xc_lockdown ~ tenure_bi | xunshi, data = d))



# bdidx_19m20, xc_lockdown, xc_closed




library(tidyverse)
library(dplyr)
library(bnlearn)
dataset_with_IV <- read_csv('/Users/qitianhu/Documents/Research/Explore/COVID-19_sosc/STAT274/IVdata-1.csv')

ci.test(x = 'xunshi', y = 'xc_lockdown', z = c('treatment', 'gdp_p'), 
        data = dataset_with_IV['xunshi', "xc_lockdown", 'treatment', 'gdp_p'])
## IV assumption testing

dataset_with_IV['xunshi', "xc_lockdown", 'treatment', 'gdp_p']
dataset_with_IV <- dataset_with_IV %>% mutate('treatment' = ifelse(tenure >= 3, 1, 0))
typeof(dataset_with_IV$xunshi)
typeof(dataset_with_IV$treatment)
ci.test(x = "xunshi", y = "treatment", data = dataset_with_IV)

ci.test(x = dataset_with_IV$xunshi, y = dataset_with_IV$treatment, data = dataset_with_IV)


