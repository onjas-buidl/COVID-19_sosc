"""this file combines the output of Combine_Data and XiChen,
	exporting in a one row one day form.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib
from tqdm import tqdm

# %%
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
       'num_firm_total', 'non_domestic_firms_total',
       'pct_of_non_domestic_firm', 'primary_emp_share_total',
       'secondary_emp_share_total', 'tertiary_emp_share_total',

       'name', 'inaug_time', 'birthmonth', 'is_female',
       'age_feb20', 'party_age', 'work_age', 'tenure',
       'nativeplace', 'partytime', 'majorchara', 'firstjobtime', 'nativeprov',
       'is_STEM_major', 'rule_in_native_prov', 'is_BA', 'is_MA', 'is_PhD']]

# # %% match using city_shortname in my dataset -- 只有275个城市了
# a = d[~d.ct_shortname.isin(xc.cityname.unique())].ct_shortname.to_list()
# print(a)
# b = xc[~xc.cityname.isin(d.ct_shortname.unique())].cityname.to_list()
# print(list(set(b)))

# %% m - merged
m = pd.merge(xc, d, left_on='cityname', right_on='ct_shortname', how='inner')
m['ct_shortname+date'] = m.ct_shortname + m.date.apply(str)

# %% 再添加 Baidu Index 信息
bd = pd.read_csv('Data/Pop_Movement/city_bd_diff_holi-melt.csv')
del bd['prov']
dates = ['20200124', '20200125', '20200126', '20200127', '20200128', '20200129', '20200130', '20200131', '20200201', '20200202', '20200203', '20200204', '20200205', '20200206', '20200207', '20200208', '20200209', '20200210', '20200211', '20200212', '20200213', '20200214', '20200215', '20200216', '20200217', '20200218', '20200219', '20200220', '20200221', '20200222', '20200223', '20200224', '20200225', '20200226', '20200227', '20200228', '20200229']
bd['Date'] = bd.Date.apply(lambda x: pd.to_datetime(dates[x]))
bd.rename(columns={'value': 'bdidx_19m20'}, inplace=True)
bd['ct_shortname+date'] = bd.ct_shortname + bd.Date.apply(str)


b = pd.merge(m, bd, on='ct_shortname+date', how='left')
b.rename(columns={'ct_shortname_x': 'ct_shortname'}, inplace=True)
b = b[~b.Date.isnull()]


# %% 整理 + export
var_list = \
       ['prov', 'citycode', 'ctnm', 'ct_shortname', 'prov_full', 'date', # identifiers
       # basic info
       'centlon', 'centlat',
       # dependent variables
       'locked_down', 'lockdown_date', 'bdidx_19m20', 'xc_lockdown', 'xc_closed',
       # COVID cases 
       'daySinceFirstCase', 'd_cum_confirm',
       # political
       'sub_prov_ct', 'gdp2018', '自治州-盟-地区', 'in_291',
       # economic
       'pdensity', 'gdp_p', 'hospital_d',
       'popHR18_all', 'Log_popHR18_all', 'gdp_per_10k',
       'primary_ind', 'second_ind', 'third_ind',
       'prov_leader_rank', 'num_hospital_total', 'num_doctors_total',
       'num_firm_total', 'non_domestic_firms_total',
       'pct_of_non_domestic_firm', 'primary_emp_share_total',
       'secondary_emp_share_total', 'tertiary_emp_share_total',

       'name', 'inaug_time', 'birthmonth', 'is_female',
       'age_feb20', 'party_age', 'work_age', 'tenure',
       'nativeplace', 'partytime', 'majorchara', 'firstjobtime', 'nativeprov',
       'is_STEM_major', 'rule_in_native_prov', 'is_BA', 'is_MA', 'is_PhD']


b = b[var_list]



# %% 加上 cumulative case
ori = pd.read_csv('Data/291城信息汇总-V1.csv')
b['cumulative_case'] = 0
import tqdm
for i in tqdm.tqdm(range(b.shape[0])):
       v = ori.loc[ori.ct_shortname == b.iloc[i]['ct_shortname']][str(b.iloc[i]['date'])[:10]].values
       assert v.shape == (1,)
       b.iloc[i, b.columns.get_loc('cumulative_case')] = v[0]

       # b.ix[i]['cumulative_case'] = v[0]

b.to_csv('Data/276城_3source_by_day.csv', index=False)
b.index = [i for i in range(b.shape[0])]
# %% 输出不 by_day 的数据 (by_ct)

b = pd.read_csv('Data/276城_3source_by_day.csv')

b[['gdp2018', 'gdp_p', 'gdp_per_10k']].corr()

del b['nativeprov'], b['nativeplace'], b['name']
del b['firstjobtime'], b['d_cum_confirm']
del b['partytime'], b['date'], b['prov_full']

a = b.groupby('ct_shortname').max()
a['ct_shortname'] = a.index
a = a[['ct_shortname'] + a.columns.to_list()]
a['log_cumulative_case'] = np.log(a.cumulative_case)

# %% add columns of mean baidu index
b = pd.read_csv('Data/276城_3source_by_day.csv')
dates_needed = [i[:4]+'-'+i[4:6]+'-'+i[6:] for i in dates[8:18]]
b = b[b.date.isin(dates_needed)]
b = b[['ct_shortname', 'bdidx_19m20']]
b_ = b.groupby('ct_shortname').mean()
b_.rename(columns={'bdidx_19m20': 'bdidx_19m20_feb1_10'}, inplace=True)
b_['ct_shortname'] = b_.index
b_.index = range(b_.shape[0])
b_ = b_[['ct_shortname','bdidx_19m20_feb1_10' ]]
a.index = range(a.shape[0])
a = a.loc[:,~a.columns.duplicated()]

c = pd.merge(a, b_, on='ct_shortname')
c.rename(columns={'ct_shortname_x':'ct_shortname_x'},inplace=True)
# del c['ct_shortname_y']



c.to_csv('Data/276城_3source_by_ct_V2.csv', index=False)

# %%
ag = a.groupby('prov').mean()

ag.sort_values('xc_lockdown')['xc_lockdown']
# 湖北、江西、浙江、广西、黑龙江、安徽、河北

ag.sort_values('locked_down')['locked_down']
# 江西、内蒙古、湖北、辽宁、江苏