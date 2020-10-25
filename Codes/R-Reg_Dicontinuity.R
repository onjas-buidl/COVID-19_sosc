library(tidyverse)
library(broom)
library(dplyr)
library(lubridate)


d <- read_csv("Data/276城_3source_by_ct_V3.csv")

d %>% 
  ggplot(aes(x = age_feb20, y = lockdown_datenum)) + 
  geom_jitter() +
  geom_vline(xintercept = 58) + 
  labs(y = "lockdown date number", x = "Age of city secretary") +
  ylim(-10,31)

d %>% 
  ggplot(aes(x = age_feb20, y = xc_lockdown_datenum)) + 
  geom_jitter() +
  geom_vline(xintercept = 58) + 
  labs(y = "lockdown date number", x = "Age of city secretary") +
  ylim(-10,31)

d %>% 
  ggplot(aes(x = age_feb20, y = xc_closed_datenum)) + 
  geom_jitter() +
  geom_vline(xintercept = 58) + 
  labs(y = "lockdown date number", x = "Age of city secretary") +
  ylim(-10,31)




# RDD
library(rddtools)
rdd_data(xc_closed_datenum, age_feb20 ,covar = d$cumulative_case,cutpoint = 57.5, data=d) %>% 
  rdd_reg_lm(slope = "separate") %>%
  summary()



plot(rdd_data(xc_closed_datenum, age_feb20 ,covar = d$cumulative_case,cutpoint = 57.5, data=d))
plot(rdd_data(xc_lockdown_datenum, age_feb20 ,covar = d$cumulative_case,cutpoint = 57.5, data=d))
plot(rdd_data(lockdown_datenum, age_feb20 ,covar = d$cumulative_case,cutpoint = 57.5, data=d))



## Step 0: prepare data 
data(house) 
house_rdd <- rdd_data(y=house$y, x=house$x, cutpoint=0) 
## Step 2: regression 
# Simple polynomial of order 1:
reg_para <- rdd_reg_lm(rdd_object=house_rdd) 
print(reg_para) 
plot(reg_para)

