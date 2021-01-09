library(tidyverse)
library(dplyr)
library(lubridate)
library(ggplot2)
setwd('/Users/qitianhu/Documents/Research/Explore/COVID-19_sosc')
data <- read_csv("Data/276城_3source_by_ct_V3.csv")
data <- data %>% filter(prov != '湖北省')


ggplot(data = data) + 
  geom_bar(mapping = aes(x = age_feb20))





