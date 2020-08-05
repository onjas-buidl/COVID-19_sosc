import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib
from tqdm import tqdm

cs = pd.read_excel('Data/市领导数据/疫情-20市委书记-331ct-V3.xlsx')
cv = pd.read_csv('Data/COVID-19/me-市级新冠数据V1.1.csv')

# %% 给city virus info 加上 city code

with open('Data/Geo_data_CN/省市对照表-old.json') as json_file:
	code2name = json.load(json_file)
name2code = {value : key for (key, value) in code2name.items()}
names = list(name2code.keys())
names_mo = list(map(lambda x: x[:-1], names)) # there are duplicates here!
names_mo2code = {value[:-1] : key for (key, value) in code2name.items()}

for n in names_mo2code.keys():
	if names_mo.count(n) > 1:
		names_mo2code[n] = np.nan

def add_code(ctnm):
	if ctnm in names:
		return name2code[ctnm]
	elif ctnm in names_mo:
		return names_mo2code[ctnm]
	else:
		return np.nan

# take care of those not directly identified
cv['cityCode'] = cv['cityName'].apply(add_code)
cv_no = cv[cv.cityCode.isnull()]
for i in cv_no.index:
	c = 0
	the_name = ''
	n = cv.iloc[i].cityName
	for j in names:
		if (n in j) or (n[:-1] in j):
			c += 1
	if c == 1:
		for j in names:
			if (n in j) or (n[:-1] in j):
				the_name = j
		cv.loc[i, 'cityCode'] = name2code[the_name]


if True:
	# cv.loc[1, 'cityCode'] = 532800
	# cv.loc[117, 'cityCode'] = 522700
	cv.loc[122, 'cityCode'] = 422800
	cv.loc[134, 'cityCode'] = 469028
	cv.loc[140, 'cityCode'] = 532500
	cv.loc[182, 'cityCode'] = 533100
	cv.loc[199, 'cityCode'] = 513300
	cv.loc[207, 'cityCode'] = 433100
	# cv.loc[216, 'cityCode'] =
	# cv.loc[217, 'cityCode'] =
	# cv.loc[220, 'cityCode'] =
	# cv.loc[221, 'cityCode'] =
	# cv.loc[226, 'cityCode'] =
	# cv.loc[227, 'cityCode'] =
	# cv.loc[228, 'cityCode'] =
	# cv.loc[229, 'cityCode'] =
	# cv.loc[230, 'cityCode'] =
	# cv.loc[231, 'cityCode'] =
	# cv.loc[232, 'cityCode'] =
	# cv.loc[238, 'cityCode'] =
	cv.loc[265, 'cityCode'] = 469030
	# cv.loc[286, 'cityCode'] =
	cv.loc[298, 'cityCode'] = 222400
	# cv.loc[300, 'cityCode'] =
	cv.loc[304, 'cityCode'] = 513200
	cv.loc[307, 'cityCode'] = 469027
	# cv.loc[328, 'cityCode'] =
	# cv.loc[329, 'cityCode'] =
	cv.loc[330, 'cityCode'] = 532600
	cv.loc[333, 'cityCode'] = 652300
	cv.loc[335, 'cityCode'] = 469029
	# cv.loc[342, 'cityCode'] =
	# cv.loc[343, 'cityCode'] =
	cv.loc[344, 'cityCode'] = 532900
	# cv.loc[345, 'cityCode'] =

	# SECOND ROUND __ 发现names_mo2code 竟然自己删除重复的lmao |
	# syntax: cvindex, the 行政编码
	change_list = [(11, 442000), (23, 430100), (26, 430600), (30, 430300), (32, 511600), (76, 360100), (81, 360800),
	               (82, 610100), (88, 211300), (98, 421000), (113, 220200),(119, 620400),
	               (122, 422800), (134, 469028), (135, 211200), (140, 532500), (142, 622900), (152, 650100),
	               (157, 130800), (160, 410700), (164, 430400), (166, 430500), (169, 340200), (173, 140200),
	               (182, 533100), (193, 320800), (199, 513300), (203, 410500), (207, 433100), (212, 341000),
	               (236, 512000), (240, 130500), (267, 211000), (279, 410900), (289, 220500), (321, 532300)]
	for pair in change_list:
		cv.loc[pair[0], 'cityCode'] = pair[1]
cv_no = cv[cv.cityCode.isnull()]
# %% Further Debug
cv = cv[~cv.cityCode.isnull()]
cv['cityCode'] = cv.cityCode.apply(int)
cv['cityFullName'] = cv.cityCode.apply(lambda x: code2name[str(x)])
cv = cv[cv.columns.tolist()[-2:] + cv.columns.tolist()[:-2]]



# %% combine 省委书记 + 城市疫情
cscv = pd.merge(cs, cv, how='left',left_on='ctnm', right_on='cityFullName')

fsj = ['沈阳', '大连', '长春', '哈尔滨','南京','杭州', '济南', '青岛', '宁波',
             '厦门','武汉','成都','西安','广州','深圳']
cscv['sub_prov_ct'] = 0
for i in fsj:
	cscv.loc[cscv.cityName == i, 'sub_prov_ct'] = 1


# %% cscv COVID data cleaning

dates = ['2020-01-'+str(i) for i in range(24, 32)] + \
        ['2020-02-0'+str(i) for i in range(1, 10)] + ['2020-02-'+str(i) for i in range(10, 30)]

cscv.loc[cscv.ctnm=='松原市', '2020-01-26'] = 1
cscv.loc[cscv.ctnm=='长春市', '2020-01-26'] = 1
cscv.loc[cscv.ctnm=='呼伦贝尔市', '2020-01-26'] = 2
cscv.loc[cscv.ctnm=='呼伦贝尔市', '2020-01-27'] = 2
cscv.loc[cscv.ctnm=='西宁市', '2020-01-26'] = 4
cscv.loc[cscv.ctnm=='鞍山市', '2020-02-02'] = 1
cscv.loc[cscv.ctnm=='吉林市', '2020-01-26'] = 1

for d in dates:
	cscv[d] = cscv[d].replace(np.nan, 0)

# %% GDP!!!

gdp = pd.read_csv('Data/城市数据/GDP/tabula-gdp2018-clean.csv')
cscv = pd.merge(cscv, gdp, left_on='ctnm', right_on='cityname', how='left')
cscv['自治州-盟-地区'] = cscv.gdp2018.isnull()

# %% Population size
pop = pd.read_excel('Data/城市数据/Population/pop2018.xlsx')[['popHR18_all', 'ctnm']]
pop['Log_popHR18_all'] = pop['popHR18_all'].apply(np.log)

cscv = pd.merge(cscv, pop, on='ctnm', how='left')

# %% GDP产业
ind = pd.read_excel('Data/城市数据/产业分布/2018城市GDP产业分布.xlsx')
ind = ind.dropna()

cscv = pd.merge(cscv, ind, on='ctnm', how='left')

# %% 省级一级响应
prov_res = pd.read_excel('Data/CN_Policy-不用了/各省一级响应.xlsx')
prov_res.set_index('prov_full', inplace=True)
res_df = []
for row in cscv.iterrows():
	res_df.append({'yiji_jan23': int(prov_res.loc[row[1]['provincename']]['yiji_date'] == pd.Timestamp('2020-01-23 00:00:00')),
	               'yiji_jan24': int(prov_res.loc[row[1]['provincename']]['yiji_date'] == pd.Timestamp('2020-01-24 00:00:00')),
	               'yiji_jan25': int(prov_res.loc[row[1]['provincename']]['yiji_date'] == pd.Timestamp('2020-01-25 00:00:00')),
	               'yiji_jan26': int(prov_res.loc[row[1]['provincename']]['yiji_date'] == pd.Timestamp('2020-01-26 00:00:00')),
	               'ctnm': row[1]['ctnm']})

res_df = pd.DataFrame(res_df)
res_df['yiji_num'] = res_df.yiji_jan24 + res_df.yiji_jan24*2

cscv = pd.merge(cscv, res_df, on='ctnm', how='left')

# %% 删掉多余变量 + Export
cscv.drop(['provincecode', 'off_month', 'race', 'time_of_data_entry', 'rule_in_covid', 'cityCode', 'cityName',
           'cityFullName', 'prov', 'note'], axis=1, inplace=True)
cscv.rename(columns={'provincename': 'prov'}, inplace=True)
cscv['locked_down'] = cscv.locked_down.apply(int)

# cscv.to_csv('Data/每日确诊+市委书记信息+副省级-V1.csv', index=False)
cscv.to_csv('Data/每日确诊+市委书记信息+副省级+GDP+pop+产业结构+省一级响应-V1.csv', index=False)


# # %% sanity check
# import random
# import statsmodels.api as sm
# import seaborn as sns; sns.set(color_codes=True)
#
#
# k = [i for i in range(1000)]
# a = pd.DataFrame({'a': k, 'b': [2*i + 1 + random.random() for i in k]})
# a.to_stata('test.dta')
# mod = sm.OLS(a.b, a.a)
# res = mod.fit()
# res.summary()


