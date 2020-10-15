
library(tidyverse)
library(dplyr)
library(lubridate)

data <- read_csv("Data/276城_3source_by_day.csv")


# 先忽略date
summary(lm(locked_down ~ age_feb20, data))


summary(lm(locked_down ~ age_feb20 + pdensity, data))

locked_down + lockdown_date + bdidx_19m20 + xc_lockdown + xc_closed
# not suitable:  + nativeplace + birthmonth + name + inaug_time  + 
# perfect multi-colinearity: tertiary_emp_share_total, is_STEM_major, is_PhD, prov_leader_rankm, partytime
# deleted for other oreason: gdp_p (redundant), firstjobtime (redundant)
f = ' ~ prov + d_cum_confirm + sub_prov_ct + gdp2018 + gdp_per_10k + pdensity + hospital_d + popHR18_all + Log_popHR18_all + 
primary_ind + second_ind + third_ind + num_hospital_total + num_doctors_total + num_firm_total +  pct_of_non_domestic_firm + 
non_domestic_firms_total + primary_emp_share_total + secondary_emp_share_total + 
is_female + age_feb20 + party_age + work_age + tenure + majorchara + rule_in_native_prov + is_BA + is_MA'


# 看哪个age最significant
f = ' ~ prov + d_cum_confirm + sub_prov_ct + gdp2018 + gdp_per_10k + pdensity + hospital_d + popHR18_all + Log_popHR18_all + 
primary_ind + second_ind + third_ind + num_hospital_total + num_doctors_total + num_firm_total +  pct_of_non_domestic_firm + 
non_domestic_firms_total + primary_emp_share_total + secondary_emp_share_total + 
is_female + tenure + majorchara + rule_in_native_prov + is_BA + is_MA +
 party_age'
+ age_feb20 + work_age
summary(lm(paste('locked_down', f), data))
summary(lm(paste('xc_lockdown', f), data))
summary(lm(paste('xc_closed', f), data))
summary(lm(paste('bdidx_19m20', f), data))



summary(lm(locked_down ~ prov + d_cum_confirm + sub_prov_ct + gdp2018 + pdensity + gdp_p + hospital_d + popHR18_all + Log_popHR18_all + gdp_per_10k + primary_ind + second_ind + third_ind + num_hospital_total + num_doctors_total + num_firm_total +  pct_of_non_domestic_firm + non_domestic_firms_total + primary_emp_share_total + secondary_emp_share_total + is_female + age_feb20 + party_age + work_age + tenure + majorchara + firstjobtime + rule_in_native_prov + is_BA + is_MA, data))  
summary(lm(xc_lockdown ~ prov + d_cum_confirm + sub_prov_ct + gdp2018 + pdensity + gdp_p + hospital_d + popHR18_all + Log_popHR18_all + gdp_per_10k + primary_ind + second_ind + third_ind + num_hospital_total + num_doctors_total + num_firm_total +  pct_of_non_domestic_firm + non_domestic_firms_total + primary_emp_share_total + secondary_emp_share_total + is_female + age_feb20 + party_age + work_age + tenure + majorchara + firstjobtime + rule_in_native_prov + is_BA + is_MA, data))  
summary(lm(xc_closed ~ prov + d_cum_confirm + sub_prov_ct + gdp2018 + pdensity + gdp_p + hospital_d + popHR18_all + Log_popHR18_all + gdp_per_10k + primary_ind + second_ind + third_ind + num_hospital_total + num_doctors_total + num_firm_total +  pct_of_non_domestic_firm + non_domestic_firms_total + primary_emp_share_total + secondary_emp_share_total + is_female + age_feb20 + party_age + work_age + tenure + majorchara + firstjobtime + rule_in_native_prov + is_BA + is_MA, data))  
summary(lm(bdidx_19m20 ~ prov + d_cum_confirm + sub_prov_ct + gdp2018 + pdensity + gdp_p + hospital_d + popHR18_all + Log_popHR18_all + gdp_per_10k + primary_ind + second_ind + third_ind + num_hospital_total + num_doctors_total + num_firm_total +  pct_of_non_domestic_firm + non_domestic_firms_total + primary_emp_share_total + secondary_emp_share_total + is_female + age_feb20 + party_age + work_age + tenure + majorchara + firstjobtime + rule_in_native_prov + is_BA + is_MA, data))



