library(survival)
library(tidyverse)
library(dplyr)
library(lubridate)

data <- read_csv("Data/291城信息汇总-V1.csv")
start_dates <- rep("2020-1-24", 296) 
start_date <- "2020-1-24"
lc_date <- data$lockdown_date %>% 
  replace_na("2020-02-21 00:00:00 UTC") 

# lc_duration <- as.duration(lc_date %--% "2020-2-21") / ddays(1)
lc_duration <- as.duration("2020-1-24" %--% lc_date ) / ddays(1)

censor <- as.integer(! is.na(data$lockdown_date))




# 1 - fit survival function 
# product-limit estimator OR Kaplan-Meier estimator
result.km <- survfit(Surv(lc_duration, censor) ~ 1, conf.type="log-log")
plot(result.km, conf.int = T, mark = "|", xlab="time in day", ylab = "survival prob", 
     main= "Non-lockdown Probability with Kaplan-Meier\n Jan 24 - Feb 21")

# Nelson-Altschuer 
result.fh <- survfit(Surv(lc_duration, censor)~1, conf.type="log-log", type="fh")
plot(result.fh, conf.int = T, mark = "|", xlab="time in day", ylab = "survival prob",
     main= "Non-lockdown Probability with Nelson-Altschuer\n Jan 24 - Feb 21")


# Fit the Cox proportional hazards model
res.cox <-  coxph(Surv(lc_duration, censor) ~ data$"2020-02-15" + data$gdp2018 + data$age_feb20  + data$second_ind + data$third_ind)
summary(res.cox)


