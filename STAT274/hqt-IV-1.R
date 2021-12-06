library(tidyverse)
library(dplyr)


d <- read_csv('/Users/qitianhu/Documents/Research/Explore/COVID-19_sosc/STAT274/IVdata-1.csv')
d$tenure_bi <- as.integer(d$tenure >= 3)
d$age_bi <- as.numeric(d$age_feb20 >= 57)



summary(lm(xc_lockdown ~ sub_prov_ct+gdp_per_10k+primary_emp_share_total+tenure, d))

iv1 <- ivreg(xc_lockdown ~ tenure_bi + sub_prov_ct + gdp_per_10k + primary_emp_share_total  | 
               + sub_prov_ct + gdp_per_10k + primary_emp_share_total  + xunshi, data = d)
summary(iv1)

texreg(iv1)


summary(ivreg(xc_lockdown ~ age_bi + sub_prov_ct + gdp_per_10k + primary_emp_share_total  | 
                + sub_prov_ct + gdp_per_10k + primary_emp_share_total  + xunshi, data = d))

# Placebo test using age 
ci.test(d$age_feb20, d$xunshi)

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






# 遍历 - 看看哪个 combination 比较 significant 
{
  "lockdown":["locked_down", "lockdown_date", "bdidx_19m20", "xc_lockdown", "xc_closed"],
  "economic": ["sub_prov_ct", "gdp2018", 
               "pdensity", "gdp_p", "hospital_d", "popHR18_all", "Log_popHR18_all",
               "gdp_per_10k", "primary_ind", "second_ind", "third_ind",
               "prov_leader_rank", "num_hospital_total", "num_doctors_total","pct_of_non_domestic_firm", "primary_emp_share_total",
               "secondary_emp_share_total", "tertiary_emp_share_total"],
  "personal": ["inaug_time",
               "birthmonth", "is_female", "age_feb20", "party_age", "work_age",
               "tenure", "majorchara", "is_STEM_major", "rule_in_native_prov", "is_BA",
               "is_MA", "is_PhD"],
  "covid": ["cumulative_case", "log_cumulative_case"]
}






econ_l = list("sub_prov_ct", "gdp2018",   "pdensity", "gdp_p", "hospital_d", "popHR18_all", "Log_popHR18_all",  "gdp_per_10k", "primary_ind", "second_ind", "third_ind",  "prov_leader_rank", "num_hospital_total", "num_doctors_total","pct_of_non_domestic_firm", "primary_emp_share_total",  "secondary_emp_share_total", "tertiary_emp_share_total")

for (ctr1 in econ_l) {
  for (ctr2 in econ_l) {
    for (ctr3 in econ_l){
      if ((ctr1 != ctr2) and (ctr2 != ctr3) and  (ctr1 != ctr3)) {
        lm(xc_lockdown ~ tenure + ctr1 + ctr2 + ctr3 ,d)}
    }
  }
}




















