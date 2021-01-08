library(tidyverse)
library(dplyr)
library(lubridate)
setwd('/Users/qitianhu/Documents/Research/Explore/COVID-19_sosc')
data <- read_csv("Data/276城_3source_by_ct.csv")
data <- read_csv("Data/276城_3source_by_ct_V3.csv")
data %>% filter(prov != '湖北省')
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


f = "~ cumulative_case + prov + age_feb20 + gdp_per_10k + Log_popHR18_all + tertiary_emp_share_total"
f = "~ cumulative_case + age_feb20 + gdp_per_10k + Log_popHR18_all + tertiary_emp_share_total"

summary(lm(paste('bdidx_19m20', f), data))
summary(lm(paste('locked_down', f), data))
summary(lm(paste('xc_lockdown', f), data))

summary(lm(paste('locked_down', "~ is_STEM_major + is_PhD + age_feb20"), data)) 

summary(glm(paste('locked_down', f), data, family=binomial))
summary(glm(paste('xc_lockdown', f), data, family=binomial))

# xc_closed太多了，没多大意义
hist(data$bdidx_19m20)


summary(lm(paste('bdidx_19m20_feb1_10', f), data))
summary(lm(paste('bdidx_19m20', f), data))





summary(lm(locked_down ~ prov + d_cum_confirm + sub_prov_ct + gdp2018 + pdensity + gdp_p + hospital_d + popHR18_all + Log_popHR18_all + gdp_per_10k + primary_ind + second_ind + third_ind + num_hospital_total + num_doctors_total + num_firm_total +  pct_of_non_domestic_firm + non_domestic_firms_total + primary_emp_share_total + secondary_emp_share_total + is_female + age_feb20 + party_age + work_age + tenure + majorchara + firstjobtime + rule_in_native_prov + is_BA + is_MA, data))  
summary(lm(xc_lockdown ~ prov + d_cum_confirm + sub_prov_ct + gdp2018 + pdensity + gdp_p + hospital_d + popHR18_all + Log_popHR18_all + gdp_per_10k + primary_ind + second_ind + third_ind + num_hospital_total + num_doctors_total + num_firm_total +  pct_of_non_domestic_firm + non_domestic_firms_total + primary_emp_share_total + secondary_emp_share_total + is_female + age_feb20 + party_age + work_age + tenure + majorchara + firstjobtime + rule_in_native_prov + is_BA + is_MA, data))  
summary(lm(xc_closed ~ prov + d_cum_confirm + sub_prov_ct + gdp2018 + pdensity + gdp_p + hospital_d + popHR18_all + Log_popHR18_all + gdp_per_10k + primary_ind + second_ind + third_ind + num_hospital_total + num_doctors_total + num_firm_total +  pct_of_non_domestic_firm + non_domestic_firms_total + primary_emp_share_total + secondary_emp_share_total + is_female + age_feb20 + party_age + work_age + tenure + majorchara + firstjobtime + rule_in_native_prov + is_BA + is_MA, data))  
summary(lm(bdidx_19m20 ~ prov + d_cum_confirm + sub_prov_ct + gdp2018 + pdensity + gdp_p + hospital_d + popHR18_all + Log_popHR18_all + gdp_per_10k + primary_ind + second_ind + third_ind + num_hospital_total + num_doctors_total + num_firm_total +  pct_of_non_domestic_firm + non_domestic_firms_total + primary_emp_share_total + secondary_emp_share_total + is_female + age_feb20 + party_age + work_age + tenure + majorchara + firstjobtime + rule_in_native_prov + is_BA + is_MA, data))




# ####### ####### ####### ####### ####### ####### ####### ######
d <- read_csv("Data/276城_3source_by_ct_V3.csv")

c('cumulative_case', 'prov', 'gdp_per_10k', "Log_popHR18_all", "tertiary_emp_share_total", "secondary_emp_share_total", 
  "hospital_d", "num_doctors_total")
'prov_leader_rank'
summary(lm(lockdown_datenum ~ age_feb20 , data = d))
summary(lm(lockdown_datenum ~ cumulative_case +age_feb20, data = d))
summary(lm(lockdown_datenum ~ cumulative_case+prov +age_feb20, data = d))
summary(lm(lockdown_datenum ~ Log_popHR18_all+secondary_emp_share_total +hospital_d+age_feb20, data = d))
summary(lm(lockdown_datenum ~ Log_popHR18_all+secondary_emp_share_total +hospital_d+age_feb20, data = d))



summary(lm(xc_lockdown_datenum ~ age_feb20, data = d))
summary(lm(xc_lockdown_datenum ~ cumulative_case +age_feb20, data = d))
summary(lm(xc_lockdown_datenum ~ cumulative_case+prov +age_feb20, data = d))
summary(lm(xc_lockdown_datenum ~ Log_popHR18_all+secondary_emp_share_total +hospital_d+age_feb20, data = d))


# coxph(Surv(lc_duration, censor) ~ data$"2020-02-15" + data$gdp2018 + data$age_feb20  + data$second_ind + data$third_ind)





# LOGISTIC

