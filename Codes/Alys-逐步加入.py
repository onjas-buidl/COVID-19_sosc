import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from tqdm import tqdm
from collections import Counter
import seaborn as sns
import functools

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
# dep_var = 'bdidx_avgdiff_date'
dep_var = 'bdidx_avgdiff_holiday'

l = ['case_on_date', 'gdp2018', 'case_per_10k']
l += ['second_ind', 'third_ind'                               ]
# l += ['sub_prov_ct'                                           ]
l += ['age_feb20', 'tenure', 'prov_leader_rank'               ]
# l += ['yiji_jan23', 'yiji_jan24', 'yiji_jan25', 'yiji_jan26'  ]
l += ['num_hospital_total', 'num_doctors_total'               ]
l += ['num_firm_total', 'pct_of_non_domestic_firm'            ]
l += ['secondary_emp_share_total', 'tertiary_emp_share_total' ]
l += ['is_STEM_major', 'is_BA', 'is_MA', 'is_PhD', 'is_female']
l += ['rule_in_native_prov', 'party_age', 'work_age'          ]


indep_vars = l
indep_string = '~ ' + functools.reduce(lambda x, y: x+' + '+y, l)
fix_date = '2020-02-04'
reg_results = []
# %% regress
fix_date = '2020-02-04'
reg_results = []

for fix_date in tqdm(dates[10:]):
	fix_datetime = pd.to_datetime(fix_date)
	data['locked_on_date'] = data.lockdown_date.apply(
		lambda x: int(not (not (isinstance(x, str)) or pd.to_datetime(x) > fix_datetime)))
	data['case_on_date'] = data[fix_date]
	data['case_per_10k'] = data['case_on_date'] / data['popHR18_all']

	results = smf.ols(dep_var + indep_string, data=data).fit()

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
reg_results.to_csv('/Users/qitianhu/Desktop/results_'+dep_var+'-'+str(indep_string.count('+')+1)+'var.csv')

# %% export to STATA

data[['locked_on_date', 'case_on_date', 'gdp2018', 'case_per_10k', 'second_ind', 'third_ind', 'sub_prov_ct', 'age_feb20', 'tenure', 'prov_leader_rank', 'yiji_jan23', 'yiji_jan24', 'yiji_jan25', 'yiji_jan26', 'num_hospital_total', 'num_doctors_total', 'num_firm_total', 'pct_of_non_domestic_firm', 'is_STEM_major', 'is_BA', 'is_MA', 'is_PhD', 'is_female', 'rule_in_native_prov', 'party_age', 'work_age']].to_stata('Data/feb_29_alldata.dta')

data[['locked_on_date', 'bdidx_avgdiff_holiday', 'bdidx_avgdiff_date'] + indep_vars].to_stata('Data/'+'feb_29_'+str(indep_string.count('+')+1)+'var_alldata.dta')



# %% test for multicolinearty
import time
from statsmodels.stats.outliers_influence import variance_inflation_factor
from joblib import Parallel, delayed

def multicollinearity_check(X, thresh=5.0):
    data_type = X.dtypes
    # print(type(data_type))
    int_cols = \
    X.select_dtypes(include=['int', 'int16', 'int32', 'int64', 'float', 'float16', 'float32', 'float64']).shape[1]
    total_cols = X.shape[1]
    try:
        if int_cols != total_cols:
            raise Exception('All the columns should be integer or float, for multicollinearity test.')
        else:
            variables = list(range(X.shape[1]))
            dropped = True
            print('''\n\nThe VIF calculator will now iterate through the features and calculate their respective values.
            It shall continue dropping the highest VIF features until all the features have VIF less than the threshold of 5.\n\n''')
            while dropped:
                dropped = False
                vif = [variance_inflation_factor(X.iloc[:, variables].values, ix) for ix in variables]
                print('\n\nvif is: ', vif)
                maxloc = vif.index(max(vif))
                if max(vif) > thresh:
                    print('dropping \'' + X.iloc[:, variables].columns[maxloc] + '\' at index: ' + str(maxloc))
                    # del variables[maxloc]
                    X.drop(X.columns[variables[maxloc]], 1, inplace=True)
                    variables = list(range(X.shape[1]))
                    dropped = True

            print('\n\nRemaining variables:\n')
            print(X.columns[variables])
            # return X.iloc[:,variables]
            return X
    except Exception as e:
        print('Error caught: ', e)


data_clean = multicollinearity_check(data[indep_vars])


