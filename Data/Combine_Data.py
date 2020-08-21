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

cscv.loc[cscv.ctnm == '松原市', '2020-01-26'] = 1
cscv.loc[cscv.ctnm == '长春市', '2020-01-26'] = 1
cscv.loc[cscv.ctnm == '呼伦贝尔市', '2020-01-26'] = 2
cscv.loc[cscv.ctnm == '呼伦贝尔市', '2020-01-27'] = 2
cscv.loc[cscv.ctnm == '西宁市', '2020-01-26'] = 4
cscv.loc[cscv.ctnm == '鞍山市', '2020-02-02'] = 1
cscv.loc[cscv.ctnm == '吉林市', '2020-01-26'] = 1

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
prov_res['prov_short'] = prov_res.prov
# prov_res.set_index('prov_full', inplace=True)

cscv = pd.merge(cscv, prov_res[['prov_full', 'yiji_date', 'prov_short']],
         left_on='provincename', right_on='prov_full', how='left')
cscv['yiji_jan23'] = (cscv.yiji_date == pd.Timestamp('2020-01-23 00:00:00')).apply(int)
cscv['yiji_jan24'] = (cscv.yiji_date == pd.Timestamp('2020-01-24 00:00:00')).apply(int)
cscv['yiji_jan25'] = (cscv.yiji_date == pd.Timestamp('2020-01-25 00:00:00')).apply(int)
cscv['yiji_jan26'] = (cscv.yiji_date == pd.Timestamp('2020-01-26 00:00:00')).apply(int)

cscv['yiji_num'] = cscv.yiji_jan24 + cscv.yiji_jan25*2 + cscv.yiji_jan26*3

# %% 省领导政治地位
prov_lead = pd.read_excel('Data/城市数据/政治地位/省级领导政治地位.xlsx')
prov_lead['prov_leader_rank'] = prov_lead['省委书记职位得分'].apply(lambda x: float(x.replace(' ', '')))
cscv = pd.merge(cscv, prov_lead[['prov_leader_rank', 'prov_short']], on='prov_short', how='left')


# %% 城市医疗信息
ct_list = list(cscv[~cscv['自治州-盟-地区']].ctnm)
med = pd.read_excel('Data/城市数据/医疗/18年鉴-医疗.xlsx')
med['ctnm'] = med.ctnm.apply(lambda x: x.replace(' ', ''))

# 在 ct_list 中全齐的只有：num_hospital_total, num_doctors_total
med = med[['ctnm', 'num_hospital_total', 'num_doctors_total']]
med = med[~med.num_hospital_total.isnull()]
med['num_hospital_total'] = med['num_hospital_total'].apply(lambda x: int(float(str(x).replace(' ', ''))))
med['num_doctors_total'] = med['num_doctors_total'].apply(lambda x: int(float(str(x).replace(' ', ''))))

cscv = pd.merge(cscv, med, on='ctnm', how='left')



# %% 城市企业数量
firms = pd.read_excel('Data/城市数据/企业/18企业数量.xlsx')
# ctnm correction
firms.loc[150, 'ctnm'] = '日照市'
firms = firms[firms.ctnm.isin(ct_list)]

firms['num_firm_total'] = firms['num_firm_total'].apply(lambda x: np.nan if pd.isnull(x) else np.int(x))
firms['num_domestic_firm_total'] = firms['num_domestic_firm_total'].apply(lambda x: np.nan if pd.isnull(x) else np.int(str(x).replace(' ', '')))

firms['num_non-domestic_firms_total'] = firms.num_firm_total - firms.num_domestic_firm_total
firms[firms['num_non-domestic_firms_total'].isnull()]
firms['pct_of_non_domestic_firm'] = (firms['num_non-domestic_firms_total'] / firms['num_firm_total'])*100

firms = firms[['ctnm', 'num_firm_total' ,'num_non-domestic_firms_total', 'pct_of_non_domestic_firm']]

cscv = pd.merge(cscv, firms, on='ctnm', how='left')

# %% 添加市委书记具体信息
data = pd.read_csv('Data/Aggregate_Data/所有信息汇总-V1.csv')
prov_list = list(data.prov_short.unique())
prov_list += ['北京', '上海', '天津', '重庆']

def prov_short_name(full):
	for i in prov_list:
		if i in full:
			return i
	return np.nan

cs = pd.read_csv('Data/市领导数据/291市委书记-二次爬详细个人信息.csv')
cs['nativeprov'] = cs.nativeplace.apply(prov_short_name)
cs['is_STEM_major'] = (cs.majorchara == 2).apply(int)

cscv = pd.merge(cscv, cs, on='name', how='left')
cscv['rule_in_native_prov'] = cscv.prov_short == cscv.nativeprov
cscv['is_BA'] = (cscv.edu == 16).apply(int)
cscv['is_MA'] = (cscv.edu == 19).apply(int)
cscv['is_PhD'] = (cscv.edu == 22).apply(int)
cscv['partytime'] = cscv['partytime'].apply(pd.to_datetime)
cscv['firstjobtime'] = cscv['firstjobtime'].apply(pd.to_datetime)
cscv['party_age'] = (pd.to_datetime('2020-02-01') - cscv['partytime']).astype('<m8[Y]')
cscv['work_age'] = (pd.to_datetime('2020-02-01') - cscv['firstjobtime']).astype('<m8[Y]')
# cs['age'] = (pd.to_datetime('2018-02-01') - cs['birthmonth']).astype('<m8[Y]')
# cscv.columns
cscv['is_female'] = (cscv.sex == '女').apply(int)

# %% check

a = cscv[~cscv['自治州-盟-地区']].isnull().sum()


# %% 删掉多余变量 + Export
cscv.drop(['provincecode', 'off_month', 'race', 'time_of_data_entry', 'rule_in_covid', 'cityCode', 'cityName',
           'cityFullName', 'prov', 'note', 'education', 'edu'], axis=1, inplace=True)
cscv.rename(columns={'provincename': 'prov'}, inplace=True)
cscv['locked_down'] = cscv.locked_down.apply(int)
# cscv.to_csv('Data/每日确诊+市委书记信息+副省级-V1.csv', index=False)
cscv.to_csv('Data/所有信息汇总-V2.csv', index=False)



