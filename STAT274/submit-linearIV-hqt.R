library(tidyverse)
library(dplyr)
library(AER)
library(texreg)
library(bnlearn)

d <- read_csv('/Users/qitianhu/Documents/Research/Explore/COVID-19_sosc/STAT274/IVdata-1.csv')
d$tenure_bi <- as.numeric(d$tenure >= 3)
d$age_bi <- as.numeric(d$age_feb20 >= 57)



iv1 <- ivreg(xc_lockdown ~ tenure_bi + sub_prov_ct + gdp_per_10k + primary_emp_share_total  | 
               + sub_prov_ct + gdp_per_10k + primary_emp_share_total  + xunshi, data = d)
summary(iv1)
texreg(iv1)



# Placebo test using age 
ci.test(d$age_feb20, d$xunshi)

iv2 <- ivreg(xc_lockdown ~ age_bi + sub_prov_ct + gdp_per_10k + primary_emp_share_total  | 
               + sub_prov_ct + gdp_per_10k + primary_emp_share_total  + xunshi, data = d)
summary(iv2)
texreg(iv2)


# quick check at last 
cor(d$xunshi, d$xc_lockdown)

cor(d$xunshi, d$tenure_bi)

# summary(lm(xc_lockdown ~ tenure_bi + sub_prov_ct + gdp_per_10k + primary_emp_share_total, d))










