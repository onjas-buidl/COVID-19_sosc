"""这文档主要
1. 搞2020市委书记数据集
2. 探索市委书记年龄
"""

# %% Imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from tqdm import tqdm
from collections import Counter
import statsmodels.api as sm

# %% initial analysis
cs = pd.read_excel('CN_Provinces/市领导数据/市委书记.xlsx')
cs = cs[cs.year == 2018]
cs['birthmonth'] = cs.bmymager.apply(pd.to_datetime)
# 用2018因为特殊原因
cs['age'] = (pd.to_datetime('2018-02-01') - cs['birthmonth']).astype('<m8[Y]')
# cs['birth'] = cs.bmymager.apply(pd.to_datetime)
cs.to_excel('CN_Provinces/CN_Policy-不用了/2018-all_secretary_info.xlsx', index=False)
cs.age.mean()

cs.age.quantile(.1)
cs.age.quantile(.9)

pc = pd.read_excel('CN_Provinces/CN_Policy-不用了/V4-Yuhang_Pan-CN_lockdown_data加官员信息.xlsx')
pc['age'] = (pd.to_datetime('2020-02-01') - pc['birthmonth']).astype('<m8[Y]')
pc.age.mean()


# %% Processing to have the full 2020.7 City Secretary list
existing = list(pc.city_code2010.apply(lambda x: x*100))
newcs = pd.read_excel('CN_Provinces/市领导数据/市委书记 2020.xlsx')
newcs['locked_down'] = newcs.citycode.apply(lambda x: True if x in existing else False)

for n in ['personid',
       'name', 'bmymager', 'sex', 'nativeplace', 'birthplace',
       'politicalstatus', 'Unnamed: 12', 'partytime', 'education',
       'majorchara', 'firstjobtime', 'age', 'edu', 'tennu', 'change']:
	newcs.loc[newcs.locked_down == False, n] = 0
newcs.year = 2020

# newcs.loc[newcs.existing == 1111, 'bmymager'] = 0
newcs.to_excel('CN_Provinces/市领导数据/市委书记_2020-V0.5.xlsx', index=False)

# %% Official Scraper -- prepare
import requests
from bs4 import BeautifulSoup

partial_done = pd.read_excel('CN_Provinces/市领导数据/市委书记_2020-V0.5.xlsx')
partial_done = partial_done[partial_done.locked_down == False]
partial_done = partial_done[partial_done.name == 0]


# cs_20_full = pd.DataFrame()
save_dict = {}
error_list = []
todo_ct =  [i for i in list(cs.ctnm) if i not in list(partial_done.ctnm)]
left_ct = todo_ct.copy()



# %%  Do Scrape
for ct_name in tqdm(todo_ct):
	url = 'https://zh.wikipedia.org/wiki/' + ct_name
	response = requests.get(url)

	if response.status_code == 200:
		soup = BeautifulSoup(response.content)
		save_dict[ct_name] = response.content
		try:
			new_dict = {
				'year': 2020,
				'citycode': int(cs.loc[cs.ctnm == ct_name, 'citycode']),
				'ctnm': ct_name,
				'provincecode': int(cs.loc[cs.ctnm == ct_name, 'provincecode']),
				'provincename': cs.loc[cs.ctnm == ct_name, 'provincename'].values[0],
				'name': soup.select('tr:nth-child(2) th+ td > a')[0].text,
				'race': soup.select('caption+ tbody tr:nth-child(3) th+ td')[0].text,
				'age': soup.select('caption+ tbody tr:nth-child(5) th+ td')[0].text,
				'inaug_time': soup.select('caption+ tbody tr:nth-child(6) th+ td')[0].text,
				'note': ''
			}
		except IndexError:
			error_list.append(ct_name)
			print(ct_name, 'IndexError')
			continue
		else:
			cs_20_full = cs_20_full.append(new_dict, ignore_index=True)
			left_ct.remove(ct_name)
	else:
		error_list.append(ct_name)
# %%
error_list.append('永州市')
cs_20_full.to_excel('CN_Provinces/市领导数据/wiki-20市委书记-322ct.xlsx', index=False)
# %%
cs_20_full = pd.read_excel('CN_Provinces/市领导数据/wiki-20市委书记-322ct.xlsx')
# one error corrected for 沈阳 in Excel -- many fields
cs_20_full.drop(110, inplace=True) # 删除三沙市
cs_20_full.drop(159, inplace=True) # 删除阿里地区!!
cs_20_full.drop(299, inplace=True) # 删除莱芜市!!
cs_20_full['age'] = cs_20_full.age.apply(lambda x: x[:8])
cs_20_full['age'] = cs_20_full.age.apply(lambda x: x[:7] if x[-1] == '（' else x)
cs_20_full['age'] = cs_20_full['age'].apply(lambda x: x.replace('年', '-').replace('月', ''))
# cs_20_full['age'] = cs_20_full.age.apply(pd.to_datetime)
cs_20_full.rename(columns={'age': 'birthmonth'}, inplace=True)
cs_20_full['race'] = cs_20_full.race.apply(lambda x: x.replace('\n', '').replace('\n', ''))
cs_20_full['inaug_time'] = \
	cs_20_full.inaug_time.apply(lambda x: x.replace('年', '-').replace('月', '').replace('4日', '').replace('7日', '').replace('\n', ''))
cs_20_full.drop('Unnamed: 0', axis=1, inplace=True)
cs_20_full.to_excel('CN_Provinces/市领导数据/wiki-20市委书记-322ct-V2.xlsx', index=False)



# %% 331 city aggregate
cs20 = pd.read_excel('CN_Provinces/市领导数据/wiki-20市委书记-331ct-V1.xlsx')
cs20['time_of_data_entry'] = pd.to_datetime('Jul 21 2020 5:00 PM')
cs20.drop(['year', 'Unnamed: 0'], axis=1, inplace=True)
error_list = ['唐山市', '秦皇岛市', '松原市', '福州市', '日照市', '临沂市', '十堰市', '随州市', '广州市', '内江市', '永州市']
for ct_name in error_list:
	cs20.loc[cs20.ctnm == ct_name, 'citycode'] = cs.loc[cs.ctnm == ct_name].citycode.values[0]
	cs20.loc[cs20.ctnm == ct_name, 'provincecode'] = cs.loc[cs.ctnm == ct_name].provincecode.values[0]
	cs20.loc[cs20.ctnm == ct_name, 'provincename'] = cs.loc[cs.ctnm == ct_name].provincename.values[0]

# sum(cs20.inaug_time.apply(pd.to_datetime) > pd.to_datetime('Feb 01, 2020'))
cs20.to_excel('CN_Provinces/市领导数据/疫情-20市委书记-331ct-V1.xlsx', index=False)


# %% 数据创建！Combine & Produce final aggregate dataset
"""
主要issue是2020.2：到底算不算决定lockdown policy的人呢
非武汉城市的lockdown是1.25 - 2.13
	一月份那几位的上任都在这个时段之前，所以可以算进去
"""

cs20 = pd.read_excel('CN_Provinces/市领导数据/疫情-20市委书记-331ct-V1.xlsx')
cs20 = cs20[cs20.rule_in_covid]
cs20['age_feb20'] = (pd.to_datetime('2020-02-01') - cs20['birthmonth'].apply(pd.to_datetime)).astype('<m8[Y]')

# add lockdown info
pc = pd.read_excel('CN_Provinces/CN_Policy-不用了/V4-Yuhang_Pan-CN_lockdown_data加官员信息.xlsx')
cs20['locked_down'] = cs20.citycode.apply(lambda x: x/100 in list(pc.city_code2010))
pc_need = pc[['daySinceFirstCase']]
pc_need['citycode'] = pc.city_code2010.copy() * 100
pc_need['lockdown_date'] = pc.lockdown
cs20 = pd.merge(cs20, pc_need, on='citycode', how='left')

cs20['tenure'] = (pd.to_datetime('2020-02-01') - cs20['inaug_time'].apply(pd.to_datetime)).astype('<m8[Y]')

cs20.to_excel('CN_Provinces/市领导数据/疫情-20市委书记-331ct-V2.xlsx', index=False)
