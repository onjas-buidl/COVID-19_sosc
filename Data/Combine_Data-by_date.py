"""this file combines the output of Combine_Data and XiChen,
	exporting in a one row one day form.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib
from tqdm import tqdm


xc = pd.read_stata('Data/Xi_Chen_data/2019-nCoV.dta')
xc = xc[['cityname', 'provincename',
         'date', 'd_cum_confirm', 'lockdown', 'closed',
         'pdensity', 'gdp_p', 'hospital_d',
         'centlon', 'centlat']]
xc['cityname'] = xc.cityname.replace('吉林市', '吉林')
xc.rename(columns={'lockdown': 'xc_lockdown', 'closed': 'xc_closed'}, inplace=True)

# 这里填 whatever Combine_Data outputs
d = pd.read_csv('Data/291城信息汇总-V1.csv')
d = d[['prov', 'citycode', 'ctnm', 'ct_shortname', 'prov_full',

       'locked_down', 'daySinceFirstCase', 'lockdown_date',
       'sub_prov_ct', 'gdp2018', '自治州-盟-地区', 'in_291',
       'popHR18_all', 'Log_popHR18_all', 'gdp_per_10k',
       'primary_ind', 'second_ind', 'third_ind',
       'prov_leader_rank', 'num_hospital_total', 'num_doctors_total',
       'num_firm_total', 'num_non-domestic_firms_total',
       'pct_of_non_domestic_firm', 'primary_emp_share_total',
       'secondary_emp_share_total', 'tertiary_emp_share_total',

       'name', 'inaug_time', 'birthmonth', 'is_female',
       'age_feb20', 'party_age', 'work_age', 'tenure',
       'nativeplace', 'partytime', 'majorchara', 'firstjobtime', 'nativeprov',
       'is_STEM_major', 'rule_in_native_prov', 'is_BA', 'is_MA', 'is_PhD']]

# %% match using city_shortname in my dataset -- 只有275个城市了
a = d[~d.ct_shortname.isin(xc.cityname.unique())].ct_shortname.to_list()
print(a)
b = xc[~xc.cityname.isin(d.ct_shortname.unique())].cityname.to_list()
print(list(set(b)))

# %% m - merged
m = pd.merge(xc, d, left_on='cityname', right_on='ct_shortname', how='inner')
m['ct_shortname+date'] = m.ct_shortname + m.date.apply(str)

# %% 再添加 Baidu Index 信息
bd = pd.read_csv('Data/Pop_Movement/city_bd_diff_holi-melt.csv')
del bd['prov']
dates = ['20200124', '20200125', '20200126', '20200127', '20200128', '20200129', '20200130', '20200131', '20200201', '20200202', '20200203', '20200204', '20200205', '20200206', '20200207', '20200208', '20200209', '20200210', '20200211', '20200212', '20200213', '20200214', '20200215', '20200216', '20200217', '20200218', '20200219', '20200220', '20200221', '20200222', '20200223', '20200224', '20200225', '20200226', '20200227', '20200228', '20200229']
bd['Date'] = bd.Date.apply(lambda x: pd.to_datetime(dates[x]))
bd.rename(columns={'value': 'bdidx_19-20'}, inplace=True)
bd['ct_shortname+date'] = bd.ct_shortname + bd.Date.apply(str)


b = pd.merge(m, bd, on='ct_shortname+date', how='left')
b = b[~b.Date.isnull()]


# %% 整理 + export

b = b[['prov', 'citycode', 'ctnm', 'ct_shortname', 'prov_full',

       'locked_down', 'lockdown_date', 'bdidx_19-20', 'xc_lockdown', 'xc_closed'
       'daySinceFirstCase', 'd_cum_confirm',
       'sub_prov_ct', 'gdp2018', '自治州-盟-地区', 'in_291',
       'pdensity', 'gdp_p', 'hospital_d', 'centlon', 'centlat',
       'popHR18_all', 'Log_popHR18_all', 'gdp_per_10k',
       'primary_ind', 'second_ind', 'third_ind',
       'prov_leader_rank', 'num_hospital_total', 'num_doctors_total',
       'num_firm_total', 'num_non-domestic_firms_total',
       'pct_of_non_domestic_firm', 'primary_emp_share_total',
       'secondary_emp_share_total', 'tertiary_emp_share_total',

       'name', 'inaug_time', 'birthmonth', 'is_female',
       'age_feb20', 'party_age', 'work_age', 'tenure',
       'nativeplace', 'partytime', 'majorchara', 'firstjobtime', 'nativeprov',
       'is_STEM_major', 'rule_in_native_prov', 'is_BA', 'is_MA', 'is_PhD']]


b.to_csv('',276城_3source_by_day.csv index=False)