import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
l = []

fnames = [i for i in os.walk('Data/市领导数据/人民网地方政府资料库front/')][0][2]


for fn in fnames:
	with open('Data/市领导数据/人民网地方政府资料库front/'+fn,'r',encoding="GBK") as file:
		l.append(file.read())
# %%

def get_major_date(ctnm):
	c = 0
	l_ = []
	ret_list = []
	for p in l:
		if '市长' in p and ctnm in p:
			soup = BeautifulSoup(p)
			s = soup.select('.box01').__str__().replace('\n<br/>\n\t\t \n\t\t\t\u3000\u3000', '\n').replace('[<div class="box01">\n         \n\t\t\t\u3000\u3000', '').replace('\n（人民网资料 截至2018年12月）<br/>\n</div>]', '').replace('\n<br/>\n</div>]','')
			s = s.split('\n')
			l_.append(list(filter(lambda x: '<' not in x and '（人民网资料' not in x, s)))

	for p in l_:
		if len(p) < 4:
			continue
		for i in range(-1, -4, -1):
			if '市长' in p[i] and ctnm in p[i]:
				ret_list.append(p)
	if len(ret_list) == 1:
		return(ret_list[0][0])
	else:
		return ret_list

r = get_major_date('苏州')

#%%
# data = pd.read_csv('Data/276城_3source_by_ct_V3.csv')
# for ctn in data.ct_shortname:
# 	get_major_date(ctn)
#
#
# for i in l_:
# 	print(i[-1])