import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from tqdm import tqdm
from collections import Counter
import seaborn as sns
from sklearn import linear_model

sns.set(color_codes=True)
import statsmodels.formula.api as smf

indep_vars = ['case_on_date', 'gdp2018', 'case_per_10k', 'second_ind', 'third_ind', 'age_feb20', 'tenure', 'prov_leader_rank', 'num_hospital_total', 'num_doctors_total', 'num_firm_total', 'pct_of_non_domestic_firm', 'secondary_emp_share_total', 'tertiary_emp_share_total', 'is_STEM_major', 'is_BA', 'is_MA', 'is_PhD', 'is_female', 'rule_in_native_prov', 'party_age', 'work_age']




data = pd.read_csv('Data/feb_29_28var_alldata.csv')
# %% Lasso !!!
lasso_chosen = []
alpha = .01

clf = linear_model.Lasso(alpha=alpha).fit(X=data[indep_vars], y=data['bdidx_avgdiff_holiday'])
clf.coef_
for i in range(len(indep_vars)):
	# if np.abs(clf.coef_[i]) > 0:
	lasso_chosen.append((indep_vars[i], clf.coef_[i]))
# sort the coeffieicnets by their magnitude
lasso_chosen = sorted(lasso_chosen, key=lambda k: abs(k[1]))

for i in lasso_chosen:
	print(i)

