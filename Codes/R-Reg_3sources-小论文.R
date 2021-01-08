library(tidyverse)
library(dplyr)
library(lubridate)
library(texreg)
setwd('/Users/qitianhu/Documents/Research/Explore/COVID-19_sosc')
# data <- read_csv("Data/276城_3source_by_ct.csv")
data <- read_csv("Data/276城_3source_by_ct_V3.csv")
data <- data %>% filter(prov != '湖北省')
####################################################################

locked_down + lockdown_date + bdidx_19m20 + xc_lockdown + xc_closed # 四个dep var
# not suitable:  + nativeplace + birthmonth + name + inaug_time  + 
# perfect multi-colinearity: tertiary_emp_share_total, is_STEM_major, is_PhD, prov_leader_rankm, partytime
# deleted for other oreason: gdp_p (redundant), firstjobtime (redundant)
f = ' ~ cumulative_case + sub_prov_ct + gdp2018 + gdp_per_10k + pdensity + hospital_d + popHR18_all + Log_popHR18_all + 
primary_ind + second_ind + third_ind + num_hospital_total + num_doctors_total + num_firm_total +  pct_of_non_domestic_firm + 
non_domestic_firms_total + primary_emp_share_total + secondary_emp_share_total + 
is_female + age_feb20 + party_age + work_age + tenure + majorchara + rule_in_native_prov + is_BA + is_MA'
# 这是全部的 


####################################################################

# 分组：COVID, Econ 总量, Econ structure , political, cs: age, edu 


# f = "~ cumulative_case + prov + age_feb20 + gdp_per_10k + Log_popHR18_all + tertiary_emp_share_total"
# f = "~ cumulative_case + age_feb20 + gdp_per_10k + Log_popHR18_all + tertiary_emp_share_total"

summary(glm(paste('locked_down', f), data, family=binomial))
summary(glm(paste('xc_lockdown', f), data, family=binomial))

m1 <- glm(locked_down ~ work_age , data, family=binomial)
m2 <- glm(locked_down ~ work_age+cumulative_case, data, family=binomial)
m3 <- glm(locked_down ~ work_age+cumulative_case+prov, data, family=binomial)
m4 <- glm(locked_down ~ work_age+cumulative_case+Log_popHR18_all+gdp_per_10k+pdensity+secondary_emp_share_total +hospital_d, data, family=binomial)

m5 <- glm(xc_lockdown ~ work_age , data, family=binomial)
m6 <- glm(xc_lockdown ~ work_age+cumulative_case, data, family=binomial)
m7 <- glm(xc_lockdown ~ work_age+cumulative_case+prov, data, family=binomial)
m8 <- glm(xc_lockdown ~ work_age+cumulative_case+Log_popHR18_all+gdp_per_10k+pdensity+secondary_emp_share_total +hospital_d, data, family=binomial)

texreg(list(m1,m2,m3,m4,m5,m6,m7,m8),  label="Table 1", 
       caption="logistic regression on two policy measures", float.pos="H",stars = c(0.01,0.05,0.1),caption.above=TRUE,
       custom.coef.map = list("age_feb20"="secretary age", 'cumulative_case'='COVID case', 'tenure' = NA, 'party_age' = NA, 'work_age' = NA),
       omit.coef = "prov", custom.model.names = c('1a','1b','1c','1d','2a','2b','2c','2d'))

# scatterplot(data$work_age, data$age_feb20)

summary(m1)
summary(m2)
summary(m3)
summary(m4)

summary(m5)
summary(m6)
summary(m7)
summary(m8)


# Linear Regression 
m1 <- lm(locked_down ~ work_age , data)
m2 <- lm(locked_down ~ work_age+cumulative_case, data)
m3 <- lm(locked_down ~ work_age+cumulative_case+prov, data)
m4 <- lm(locked_down ~ work_age+cumulative_case+Log_popHR18_all+gdp_per_10k+pdensity+secondary_emp_share_total +hospital_d, data)

m5 <- lm(xc_lockdown ~ work_age , data)
m6 <- lm(xc_lockdown ~ work_age+cumulative_case, data)
m7 <- lm(xc_lockdown ~ work_age+cumulative_case+prov, data)
m8 <- lm(xc_lockdown ~ work_age+cumulative_case+Log_popHR18_all+gdp_per_10k+pdensity+secondary_emp_share_total +hospital_d, data)

# texreg(list(m1,m2,m3,m4,m5,m6,m7,m8),  label="Table 1 - appendix", 
#        caption="linear regression on two policy measures", float.pos="H",stars = c(0.01,0.05,0.1),caption.above=TRUE,
#        custom.coef.map = list("age_feb20"="secretary age", 'cumulative_case'='COVID case'),
#        omit.coef = "prov", custom.model.names = c('1a','1b','1c','1d','2a','2b','2c','2d'))


texreg(list(m1,m2,m3,m4,m5,m6,m7,m8),  label="Table 1", 
       caption="linear regression on two policy measures", float.pos="H",stars = c(0.01,0.05,0.1),caption.above=TRUE,
       custom.coef.map = list("age_feb20"="secretary age", 'cumulative_case'='COVID case', 'tenure' = NA, 'party_age' = NA, 'work_age' = NA),
       omit.coef = "prov", custom.model.names = c('1a','1b','1c','1d','2a','2b','2c','2d'))





############################# Survival Analysis ############################






