"""Based on the results
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib
import tqdm

dates = ['20200124', '20200125', '20200126', '20200127', '20200128', '20200129', '20200130', '20200131', '20200201', '20200202', '20200203', '20200204', '20200205', '20200206', '20200207', '20200208', '20200209', '20200210', '20200211', '20200212', '20200213', '20200214', '20200215', '20200216', '20200217', '20200218', '20200219', '20200220', '20200221', '20200222', '20200223', '20200224', '20200225', '20200226', '20200227', '20200228', '20200229']
dates_needed = [i[:4]+'-'+i[4:6]+'-'+i[6:] for i in dates[8:18]]
# # %% build initial a
# byday = pd.read_csv('Data/276城_3source_by_day.csv')
# del byday['nativeprov'], byday['nativeplace'], byday['name']
# del byday['firstjobtime'], byday['d_cum_confirm']
# del byday['partytime'], byday['date'], byday['prov_full']
#
# a = byday.groupby('ct_shortname').max()
# a['ct_shortname'] = a.index
# a = a[['ct_shortname'] + a.columns.to_list()]
# a['log_cumulative_case'] = np.log(a.cumulative_case)
# # %%
# byday = pd.read_csv('Data/276城_3source_by_day.csv')
# byday = byday[byday.date.isin(dates_needed)]
# byday = byday[['ct_shortname', 'bdidx_19m20']]
# b_ = byday.groupby('ct_shortname').mean()
# b_.rename(columns={'bdidx_19m20': 'bdidx_19m20_feb1_10'}, inplace=True)
# b_['ct_shortname'] = b_.index
# b_.index = range(b_.shape[0])
# b_ = b_[['ct_shortname', 'bdidx_19m20_feb1_10' ]]
# a.index = range(a.shape[0])
# a = a.loc[:,~a.columns.duplicated()]
#
# byct = pd.merge(a, b_, on='ct_shortname')
# byct.rename(columns={'ct_shortname_x': 'ct_shortname_x'}, inplace=True)

"""date num的规则：1就是2.1, 0是1.31，以此类推
	OR date - pd.to_datetime('2020-1-31')
	ALSO 没lockdown的城市设为3.1号lockdown
"""
# %% 加上xi chen lockdown和原有lockdown 的 date num
byct = pd.read_csv('Data/276城_3source_by_ct_V2.csv')
# 先处理原有lockdown
byct['lockdown_date'] = byct.lockdown_date.apply(pd.to_datetime)
byct.lockdown_date.apply(lambda day: day.day if day else 0)
byct['lockdown_datenum'] = \
	(byct.lockdown_date - pd.to_datetime('2020-1-31')).apply(lambda d: d.days if d else 30)
# 30是3.1 - 1.30的天数
byct['lockdown_datenum'].fillna(30, inplace=True)

# %% 再处理 XiChen closed
xc = pd.read_stata('Data/Xi_Chen_data/2019-nCoV.dta')
xc = xc[['cityname', 'provincename',
         'date', 'd_cum_confirm', 'lockdown', 'closed',
         'pdensity', 'gdp_p', 'hospital_d',
         'centlon', 'centlat']]
xc['cityname'] = xc.cityname.replace('吉林市', '吉林')
xc.rename(columns={'lockdown': 'xc_lockdown', 'closed': 'xc_closed'}, inplace=True)

# 转化date to datenum
xc['xc_lockdown_datenum'] = (xc.date - pd.to_datetime('2020-1-31')).apply(lambda d: d.days)
xc['xc_closed_datenum'] = (xc.date - pd.to_datetime('2020-1-31')).apply(lambda d: d.days)

# 先处理xc lockdown
xc_lkd = xc[xc.xc_lockdown>0].groupby('cityname').min() # 找到每个城市datenum最小且已经lockdown的
xc_lkd['ct_shortname'] = xc_lkd.index
byct = pd.merge(byct, xc_lkd[['ct_shortname', 'xc_lockdown_datenum']],
                on='ct_shortname', how='left')
byct['xc_lockdown_datenum'] = byct['xc_lockdown_datenum'].fillna(30)

# 再处理 xc closed
xc_cls = xc[xc.xc_closed>0].groupby('cityname').min() # 找到每个城市datenum最小且已经lockdown的
xc_cls['ct_shortname'] = xc_cls.index
byct = pd.merge(byct, xc_cls[['ct_shortname', 'xc_closed_datenum']],
                on='ct_shortname', how='left')
byct['xc_closed_datenum'] = byct['xc_closed_datenum'].fillna(30)
byct['hu_liao_jiang_nei'] = byct.prov.isin(['湖北省', '辽宁省', '江西省', '内蒙古自治区']).apply(int)
# %% export csv

byct.to_csv('Data/276城_3source_by_ct_V3.csv', index=False)
#%% export to Stata form
byct = pd.read_csv('Data/276城_3source_by_ct_V3.csv')
# byct[['lockdown_datenum','xc_lockdown_datenum','xc_closed_datenum',
#       'locked_down', 'xc_lockdown', 'xc_closed', 'hu_liao_jiang_nei', 'tenure',
#       'age_feb20', 'gdp2018', 'cumulative_case', 'hospital_d', 'Log_popHR18_all']].to_stata('Data/276城_3source_by_ct_V3.dta')

l = byct.columns.tolist()
l.remove('ct_shortname')
l.remove('prov')
l.remove('ctnm')
l.remove('自治州-盟-地区')

a = byct[l]
a.to_stata('Data/276城_3source_by_ct_V3.dta')

# %% 加上市长信息，同样明明
byct = pd.read_csv('Data/276城_3source_by_ct_V3.csv')
mayor = pd.read_excel('Data/市领导数据/人民网-市长-V1.xlsx')



