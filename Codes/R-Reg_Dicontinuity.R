library(tidyverse)
library(broom)
library(dplyr)
library(lubridate)

setwd('/Users/qitianhu/Documents/Research/Explore/COVID-19_sosc/')
d <- read_csv("Data/276城_3source_by_ct_V3.csv")

d %>% 
  ggplot(aes(x = age_feb20, y = lockdown_datenum)) + 
  geom_jitter() +
  geom_vline(xintercept = 58) + 
  labs(y = "lockdown date number", x = "Age of city secretary") +
  ylim(-10,31)



# RDD
library(rddtools)
rdd_data(xc_closed_datenum, age_feb20 ,covar = d$cumulative_case,cutpoint = 57, data=d) %>% 
  rdd_reg_lm(slope = "separate") %>%
  summary()


plot(rdd_data(xc_closed_datenum, age_feb20 ,covar = d$cumulative_case,cutpoint = 57.5, data=d))
plot(rdd_data(xc_lockdown_datenum, age_feb20 ,covar = d$cumulative_case,cutpoint = 57.5, data=d))
plot(rdd_data(lockdown_datenum, age_feb20 ,covar = d$cumulative_case,cutpoint = 59, data=d))



## Step 0: prepare data 
data(house) 
house_rdd <- rdd_data(y=house$y, x=house$x, cutpoint=0) 
## Step 2: regression 
# Simple polynomial of order 1:
reg_para <- rdd_reg_lm(rdd_object=house_rdd) 
print(reg_para) 
plot(reg_para)


rdd_data(residual, age_feb20 ,covar = d$cumulative_case,cutpoint = 57.5, data=d) %>% 
  rdd_reg_lm(slope = 'separate') %>% 
  summary()



# USE RESIDUAL AS RD
summary(basic_lm)

plot_resid_rd <- function(dep_var, f, want_plot = TRUE, want_print = TRUE) {
  basic_lm = lm(paste(dep_var, f), data = d); d$residual <- resid(basic_lm)
  rd_dat <- rdd_data(residual, age_feb20 ,covar = d$cumulative_case,cutpoint = 57.5, data=d)
  rd_lm <- rdd_reg_lm(rd_dat)
  if (want_print) {print(summary(rd_lm))}
  if (want_plot) {plot(rd_dat)}
  return(summary(rd_lm)$coef[,4][[2]])
}

f = "~ cumulative_case + prov + gdp_per_10k + Log_popHR18_all + tertiary_emp_share_total"
f = "~ cumulative_case + gdp_per_10k + Log_popHR18_all + tertiary_emp_share_total"
f = "~ cumulative_case + gdp_per_10k + Log_popHR18_all + secondary_emp_share_total"
f <-  "~ gdp_p + log_cumulative_case + hospital_d + secondary_emp_share_total"
f <-  "~ gdp2018 + log_cumulative_case + hospital_d + secondary_emp_share_total"
f <-  "~ gdp2018 + num_doctors_total + prov"
f <- "~ prov"

plot_resid_rd("lockdown_datenum", f)
plot_resid_rd("xc_lockdown_datenum", f)
plot_resid_rd("xc_closed_datenum", f)
plot_resid_rd("bdidx_19m20_feb1_10", f)
plot_resid_rd("bdidx_19m20", f)

# f <- "~ gdp_p + log_cumulative_case + hospital_d + secondary_emp_share_total"
# basic_lm = lm(paste("lockdown_datenum", f), data = d); d$residual <- resid(basic_lm)
# plot(rdd_data(residual, age_feb20 ,covar = d$cumulative_case,cutpoint = 57.5, data=d))
# 
# basic_lm = lm(paste("xc_lockdown_datenum", f), data = d); d$residual <- resid(basic_lm)
# plot(rdd_data(residual, age_feb20 ,covar = d$cumulative_case,cutpoint = 57.5, data=d))
# 
# basic_lm = lm(paste("xc_closed_datenum", f), data = d); d$residual <- resid(basic_lm)
# plot(rdd_data(residual, age_feb20 ,covar = d$cumulative_case,cutpoint = 57.5, data=d))
# 
# basic_lm = lm(paste("bdidx_19m20_feb1_10", f), data = d); d$residual <- resid(basic_lm)
# plot(rdd_data(residual, age_feb20 ,covar = d$cumulative_case,cutpoint = 57.5, data=d))

plot_resid_rd <- function(dep_var, f, want_plot = TRUE, want_print = TRUE) {
  basic_lm = lm(paste(dep_var, f), data = d); d$residual <- resid(basic_lm)
  rd_dat <- rdd_data(residual, age_feb20 ,covar = d$cumulative_case,cutpoint = 57.5, data=d)
  rd_lm <- rdd_reg_lm(rd_dat)
  if (want_print) {print(summary(rd_lm))}
  if (want_plot) {plot(rd_dat)}
  return(summary(rd_lm)$coef[,4][[2]])
}

# 用combination暴力穷举找到significance
all_dep_vars <-  c("lockdown_datenum","xc_lockdown_datenum","xc_closed_datenum","bdidx_19m20_feb1_10","bdidx_19m20", "lockdown_datenum<30","xc_lockdown_datenum<30","xc_closed_datenum<30")
indep_var_save <- list()
for (j in c(1:8)) {
  

comb_matrix <- combn(c('cumulative_case', 'prov', 'gdp_per_10k', "Log_popHR18_all", "tertiary_emp_share_total", "secondary_emp_share_total", 
                       "hospital_d", "num_doctors_total"), j)

ncol(comb_matrix)
for (i in c(1:ncol(comb_matrix))) {
  indep_vars <- comb_matrix[,i]
  f <- paste(" ~ ",  paste(indep_vars, collapse=" + "))
  c <- 0#; print(999999999)
  for (dep_var in all_dep_vars) {
    if (plot_resid_rd(dep_var, f, want_print = FALSE, want_plot = FALSE) < .1 ) {
      c <- c+1}#; print(c); print(dep_var)
    if (c > 2) {indep_var_save <- append(indep_var_save, paste(dep_var, f))}
    }
}
}
indep_var_save

