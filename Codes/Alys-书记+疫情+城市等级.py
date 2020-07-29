import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from tqdm import tqdm
from collections import Counter
import statsmodels.api as sm


data = pd.read_csv('Data/每日确诊+市委书记信息+副省级+GDP-V1.csv')
dates = ['2020-01-'+str(i) for i in range(24, 32)] + \
        ['2020-02-0'+str(i) for i in range(1, 10)] + ['2020-02-'+str(i) for i in range(10, 30)]

data = data[data.prov != '湖北省']

# %% 病例与lockdown的关系 Fix Date: find lockdown on date & case on date
fix_date = '2020-02-07'
results_case = {}
results_sub_p = {}
significance = {}
for fix_date in dates:
        fix_datetime = pd.to_datetime(fix_date)
        data['locked_on_date'] = data.lockdown_date.apply(lambda x: not(not(isinstance(x, str)) or pd.to_datetime(x) > fix_datetime))
        mod = sm.OLS(data.locked_on_date.apply(int), data[[fix_date, 'sub_prov_ct']])
        res = mod.fit()
        results_case[fix_date] = res.params[0]
        results_sub_p[fix_date] = res.params[1]
        significance[fix_date] = res.f_pvalue

# %% 城市GDP -- pure
mod = sm.OLS(data.locked_on_date.apply(int), data[['gdp2018']])
res = mod.fit()


# %% GDP + COVID + 副省级
fix_date = '2020-02-07'
mod = sm.OLS(data.locked_on_date.apply(int), data[[fix_date, 'sub_prov_ct']])
res = mod.fit()




