import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from tqdm import tqdm
from collections import Counter
import seaborn as sns; sns.set(color_codes=True)
import statsmodels.formula.api as smf

data = pd.read_csv('Data/每日确诊+市委书记信息+副省级+GDP+pop+产业结构+省一级响应-V1.csv')
dates = ['2020-01-'+str(i) for i in range(24, 32)] + \
        ['2020-02-0'+str(i) for i in range(1, 10)] + ['2020-02-'+str(i) for i in range(10, 30)]

data = data[data.prov != '湖北省']
# data['locked_on_date'] = data['locked_on_date'].apply(int)

# %% 病例与lockdown的关系 Fix Date: find lockdown on date & case on date
fix_date = '2020-02-07'
results_case = {}
results_sub_p = {}
significance = {}
for fix_date in dates:
	fix_datetime = pd.to_datetime(fix_date)
	data['locked_on_date'] = data.lockdown_date.apply(lambda x: int(not(not(isinstance(x, str)) or pd.to_datetime(x) > fix_datetime)))
	data['case_on_date'] = data[fix_date]
	# mod = sm.OLS(data.locked_on_date.apply(int), data[[fix_date, 'sub_prov_ct']])
	res = smf.ols('locked_on_date ~ case_on_date + sub_prov_ct', data=data).fit()
	results_case[fix_date] = res.params[1]
	results_sub_p[fix_date] = res.params[2]
	significance[fix_date] = res.f_pvalue

# %% 城市GDP -- pure
data_ = data[~data['自治州-盟-地区']]
mod = sm.OLS(data_.locked_down.apply(int), data_[['gdp2018']])
res = mod.fit()
res.summary()
# %% 副省级 pure
data_ = data
# mod = sm.OLS(data_.locked_down.apply(int), data_[['sub_prov_ct']])
mod = smf.ols('locked_on_date ~ sub_prov_ct', data=data) #data_.locked_down.apply(int), data_[['sub_prov_ct']])
res = mod.fit()
res.summary()

# %% 总regression using sm
fix_date = '2020-02-04'
reg_results = []
for fix_date in dates[10:]:
	fix_datetime = pd.to_datetime(fix_date)
	data['locked_on_date'] = data.lockdown_date.apply(lambda x: int(not(not(isinstance(x, str)) or pd.to_datetime(x) > fix_datetime)))
	data['case_on_date'] = data[fix_date]

	data_ = data[~data['自治州-盟-地区']]
	# smf.ols('case_on_date',
	#                     'gdp2018', 'Log_popHR18_all', 'second_ind', 'third_ind',
	#                     'sub_prov_ct', 'age_feb20', 'tenure')
	mod = sm.OLS(data_.locked_on_date.apply(int),
	             data_[['case_on_date',
	                    'gdp2018', 'Log_popHR18_all', 'second_ind', 'third_ind',
	                    'sub_prov_ct', 'age_feb20', 'tenure']])
	res = mod.fit()

	res_dict = dict(res.params)
	reg_results.append(res_dict)


reg_results = pd.DataFrame(reg_results)
reg_results.index = dates[10:]


# %% 总regression using smf
fix_date = '2020-02-04'
reg_results = []

for fix_date in dates[10:]:
	fix_datetime = pd.to_datetime(fix_date)
	data['locked_on_date'] = data.lockdown_date.apply(lambda x: int(not(not(isinstance(x, str)) or pd.to_datetime(x) > fix_datetime)))
	data['case_on_date'] = data[fix_date]
	data['case_per_10k'] = data['case_on_date'] / data['popHR18_all']
	data_ = data[~data['自治州-盟-地区']]
	results = smf.ols('locked_on_date ~ case_on_date + gdp2018 +' +
	        'Log_popHR18_all + second_ind + third_ind + ' +
	        'sub_prov_ct + age_feb20 + tenure', data=data_).fit()
	# results = smf.ols('locked_on_date ~ case_per_10k + gdp2018 +' +
	#                   ' second_ind + third_ind + ' +
	#                   'sub_prov_ct + age_feb20 + tenure', data=data_).fit()
	# results.summary()
	# res = mod.fit()

	res_dict = dict(results.params)
	reg_results.append(res_dict)


reg_results = pd.DataFrame(reg_results)
reg_results.index = dates[10:]
reg_results.to_csv('/Users/qitianhu/Desktop/reg_results.csv')


# %% variable-wise regression
sns.regplot(x='third_ind', y='gdp2018', data=data) ; plt.show()




