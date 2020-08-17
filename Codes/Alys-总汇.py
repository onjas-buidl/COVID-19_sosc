import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from tqdm import tqdm
from collections import Counter
import seaborn as sns; sns.set(color_codes=True)
import statsmodels.formula.api as smf

data = pd.read_csv('Data/所有信息汇总-V1.csv')
dates = ['2020-01-'+str(i) for i in range(24, 32)] + \
        ['2020-02-0'+str(i) for i in range(1, 10)] + ['2020-02-'+str(i) for i in range(10, 30)]

data = data[data.prov != '湖北省']
data['gdp_per_10k'] = data['gdp2018'] / data.popHR18_all

# %% 总regression using smf
fix_date = '2020-02-04'
reg_results = []

for fix_date in dates[10:]:
	fix_datetime = pd.to_datetime(fix_date)
	data['locked_on_date'] = data.lockdown_date.apply(lambda x: int(not(not(isinstance(x, str)) or pd.to_datetime(x) > fix_datetime)))
	data['case_on_date'] = data[fix_date]
	data['case_per_10k'] = data['case_on_date'] / data['popHR18_all']
	data_ = data[~data['自治州-盟-地区']]
	results = smf.ols('locked_on_date ~ case_on_date + gdp2018 + case_per_10k + ' +
	        'second_ind + third_ind + ' +
	        'sub_prov_ct + age_feb20 + tenure + prov_leader_rank', data=data_).fit()

	res_dict = {} # dict(results.params)
	for k in results.pvalues.keys():
		if results.pvalues[k] < .01:
			res_dict[k] = str(round(results.params[k], 5)) + '***'
		elif results.pvalues[k] < .05:
			res_dict[k] = str(round(results.params[k], 5)) + '**'
		elif results.pvalues[k] < .1:
			res_dict[k] = str(round(results.params[k], 5)) + '*'
		else:
			res_dict[k] = str(round(results.params[k], 5))


	reg_results.append(res_dict)


reg_results = pd.DataFrame(reg_results)
reg_results.index = dates[10:]
reg_results.to_csv('/Users/qitianhu/Desktop/reg_results.csv')

