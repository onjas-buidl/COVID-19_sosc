import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from tqdm import tqdm
from collections import Counter
import statsmodels.api as sm
import seaborn as sns; sns.set(color_codes=True)


data = pd.read_csv('Data/每日确诊+市委书记信息+副省级+GDP+pop+产业结构-V1.csv')
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
data_ = data[~data['自治州-盟-地区']]
mod = sm.OLS(data_.locked_down.apply(int), data_[['gdp2018']])
res = mod.fit()
res.summary()
# %% 副省级 pure
data_ = data
mod = sm.OLS(data_.locked_down.apply(int), data_[['sub_prov_ct']])
res = mod.fit()
res.summary()

# %% 总regression
fix_date = '2020-02-04'
reg_results = []
for fix_date in dates[10:]:
	fix_datetime = pd.to_datetime(fix_date)
	data['locked_on_date'] = data.lockdown_date.apply(lambda x: not(not(isinstance(x, str)) or pd.to_datetime(x) > fix_datetime))
	data['case_on_date'] = data[fix_date]

	data_ = data[~data['自治州-盟-地区']]

	mod = sm.OLS(data_.locked_on_date.apply(int),
	             data_[['case_on_date',
	                    'gdp2018', 'Log_popHR18_all', 'second_ind', 'third_ind',
	                    'sub_prov_ct', 'age_feb20', 'tenure']])
	res = mod.fit()

	res_dict = dict(res.params)
	reg_results.append(res_dict)


reg_results = pd.DataFrame(reg_results)
reg_results.index = dates[10:]


# %% variable-wise regression
sns.regplot(x='third_ind', y='gdp2018', data=data); plt.show()




