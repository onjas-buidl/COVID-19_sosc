import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from tqdm import tqdm
import seaborn as sns

d = pd.read_stata('Data/Xi_Chen_data/2019-nCoV.dta')
data = pd.read_stata('Data/Xi_Chen_data/2019-nCoV.dta', iterator=True)
l = data.variable_labels()

d.groupby('date').sum().lockdown
d.groupby('date').sum().closed


# %% 探索数据集：两个policy的城市区别

closed = d.groupby('city').sum()['closed']
closed = closed[closed > 0].index.to_list()
# closed management of communities
# 241


locked = d.groupby('city').sum()['lockdown']
locked = locked[locked > 0].index.to_list()
# Family outdoor restrictions
# 123

n = 0
for c in locked:
	n += int(c in closed)
# locked的城市是closed的子集

d[['city', 'province', 'date', 'd_cum_confirm', 'lockdown','lockdown_w1', 'lockdown_w2', 'closed', 'closed_w1', 'closed_w2', 'pdensity', 'gdp_p','hospital_d', 'cityw']]