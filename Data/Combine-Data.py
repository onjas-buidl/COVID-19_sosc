import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib
from tqdm import tqdm

cs = pd.read_excel('Data/市领导数据/疫情-20市委书记-331ct-V2.xlsx')
cv = pd.read_csv('Data/COVID-19/me-市级新冠数据V1.0.csv')

# %% 给city virus info 加上 city code

with open('Data/Geo_data_CN/省市对照表.json') as json_file:
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

cv_no = cv[cv.cityCode.isnull()]
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

	# SECOND ROUND __ 发现names_mo2code 竟然自己删除重复的lmao | syntax: cvindex, cityCode
	change_list = [(11, )]
# %% Further Debug
cv = cv[~cv.cityCode.isnull()]
cv['cityCode'] = cv.cityCode.apply(int)
# cv['cityCode'] = cv['cityCode'] // 100 * 100
# cv[cv.cityName == '朝阳']


# cv['cityFullName'] = cv.cityCode.apply(lambda x: code2name[str(x)])
# cv['error']

# %% combine 省委书记 + 城市疫情
cscv = pd.merge(cs, cv, left_on='citycode', right_on='cityCode')
cscv.shape

# %% Debug
errors = []
for i in range(cs.shape[0]): # cs.citycode
	if cs.iloc[i].citycode not in list(cscv.citycode):
		errors.append(i)


cs.iloc[errors[2]]