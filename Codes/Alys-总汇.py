import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from tqdm import tqdm
from collections import Counter
import seaborn as sns

sns.set(color_codes=True)
import statsmodels.formula.api as smf

data = pd.read_csv('Data/所有信息汇总-V2.csv')
dates = ['2020-01-' + str(i) for i in range(24, 32)] + \
        ['2020-02-0' + str(i) for i in range(1, 10)] + ['2020-02-' + str(i) for i in range(10, 30)]

data = data[data.prov != '湖北省']
data['gdp_per_10k'] = data['gdp2018'] / data.popHR18_all
data = data[~data['自治州-盟-地区']]
# %% 总regression using smf - dep=included dummy
dep_var = 'locked_on_date'
dep_var = 'bdidx_avgdiff_date'

indep_string = ' ~ case_on_date + gdp2018 + case_per_10k + ' +\
				'second_ind + third_ind + ' +  \
				'sub_prov_ct + age_feb20 + tenure + prov_leader_rank + ' +  \
				'yiji_jan23 + yiji_jan24 + yiji_jan25 + yiji_jan26 + ' + \
				'num_hospital_total + num_doctors_total + ' +  \
				'num_firm_total + pct_of_non_domestic_firm + ' + \
				'is_STEM_major + is_BA + is_MA + is_PhD + is_female + ' +  \
				'rule_in_native_prov + party_age + work_age'

fix_date = '2020-02-04'
reg_results = []

for fix_date in tqdm(dates[10:]):
	fix_datetime = pd.to_datetime(fix_date)
	data['locked_on_date'] = data.lockdown_date.apply(
		lambda x: int(not (not (isinstance(x, str)) or pd.to_datetime(x) > fix_datetime)))
	data['case_on_date'] = data[fix_date]
	data['case_per_10k'] = data['case_on_date'] / data['popHR18_all']


	results = smf.ols(dep_var + indep_string, data = data).fit()


	res_dict = {}  # dict(results.params)
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
reg_results.to_csv('/Users/qitianhu/Desktop/reg_results_'+str(formula_string.count('+')+1)+'var.csv')

# %% export to STATA

data[['locked_on_date','case_on_date', 'gdp2018', 'case_per_10k', 'second_ind', 'third_ind', 'sub_prov_ct', 'age_feb20', 'tenure', 'prov_leader_rank', 'yiji_jan23', 'yiji_jan24', 'yiji_jan25', 'yiji_jan26', 'num_hospital_total', 'num_doctors_total', 'num_firm_total', 'pct_of_non_domestic_firm', 'is_STEM_major', 'is_BA', 'is_MA', 'is_PhD', 'is_female', 'rule_in_native_prov', 'party_age', 'work_age']].to_stata('Data/feb_29_alldata.dta')


