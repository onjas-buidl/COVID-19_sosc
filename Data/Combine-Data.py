import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib
from tqdm import tqdm

cs = pd.read_excel('Data/市领导数据/疫情-20市委书记-331ct-V2.xlsx')
cv = pd.read_csv('Data/COVID-19/me-市级新冠数据V1.0.csv')

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
# cv['cityCode'] = cv['cityCode'] // 100 * 100
# cv[cv.cityName == '朝阳']
# cv['cityFullName'] = cv.cityCode.apply(lambda x: code2name[str(x)])
# cv['error']
# cv[cv.cityCode % 100 == 0].shape



# %% combine 省委书记 + 城市疫情
cscv = pd.merge(cs, cv, how='left',left_on='ctnm', right_on='cityFullName')

fsj = ['沈阳', '大连', '长春', '哈尔滨','南京','杭州', '济南', '青岛', '宁波',
             '厦门','武汉','成都','西安','广州','深圳']
cscv['sub_prov_ct'] = 0
for i in fsj:
	cscv.loc[cscv.cityName == i, 'sub_prov_ct'] = 1

"""
直辖市到时候和省级单位一起算吧"""
# zxs = ['北京', '天津', '重庆', '上海']
# cscv['direct_control_ct'] = 0
# for i in zxs:
# 	cscv.loc[cscv.cityName == i, 'sub_prov_ct'] = 1
#
# cscv.direct_control_ct.sum()

cscv.to_csv('Data/每日确诊+市委书记信息+副省级-V1.csv', index=False)


