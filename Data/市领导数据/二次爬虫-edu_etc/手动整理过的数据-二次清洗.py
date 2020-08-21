"""
firstjobtime -- ' 年 月 参加工作
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import zhconv
import re
import pickle
import os



# %% setup
var_str_clean = ['sex', 'nativeplace', 'partytime', 'education', 'firstjobtime'] #, 'edu'] 'majorchara'
cs = pd.read_excel('Data/市领导数据/二次爬虫-edu_etc/全291人信息整理 - 手动整理2.xlsx')
cs.drop(['name-birth', 'url', 'baidu', 'missing_need_var'], axis=1, inplace=True)
cs['majorchara'].fillna(1, inplace=True)
cs['partytime'] = cs['partytime'].apply(str)
cs['firstjobtime'] = cs['firstjobtime'].apply(str)
cs['education'] = cs['education'].apply(lambda x: x[:30] if len(x) > 30 else x)
cs['birthmonth'] = cs['birthmonth'].apply(pd.to_datetime)

cs['sex'].replace('男, 男', '男', inplace=True)

for n in var_str_clean:
	cs[n] = cs[n].apply(lambda x: x.replace('\'', '').replace('"', '').replace('“', '').replace('”', '').replace(']', '').replace('[', '').replace('【', '').replace('】', '').replace('‘', '').replace('’', ''))

# %% partytime
cs['partytime'] = cs['partytime'].apply(lambda x: x.replace('入党', '').replace('加入中国共产党', '').replace('年', '-').replace('月', '').replace('-00', '-1'))
cs['partytime'] = cs['partytime'].apply(pd.to_datetime)

to_fill_partytime = cs[cs.partytime.isnull()]

for p in to_fill_partytime.iterrows():
	p = p[-1]
	self_birth = p.birthmonth
	estimate_partytime = cs[np.abs((cs.birthmonth - self_birth)/np.timedelta64(1, 'M')) <= 12].partytime.mean()
	cs.loc[cs.name == p['name'], 'partytime'] = estimate_partytime


# %% firstjobtime
cs['firstjobtime'] = cs['firstjobtime'].apply(lambda x: x.replace('参加工作', '').replace('年', '-').replace('月', ''))
cs['firstjobtime'] = cs['firstjobtime'].apply(pd.to_datetime)
# for i in range(cs.shape[0]):
# 	pd.to_datetime(cs['firstjobtime'][i])
# cs.iloc[i]

to_fill_firstjobtime = cs[cs.firstjobtime.isnull()]

for p in to_fill_firstjobtime.iterrows():
	p = p[-1]
	self_birth = p.birthmonth
	estimate_firstjobtime = cs[np.abs((cs.birthmonth - self_birth)/np.timedelta64(1, 'M')) <= 12].firstjobtime.mean()
	cs.loc[cs.name == p['name'], 'firstjobtime'] = estimate_firstjobtime

# %% nativeplace 整理



cs.drop(['ctnm', 'birthmonth'], axis=1, inplace=True)
cs.to_csv('Data/市领导数据/291市委书记-二次爬详细个人信息.csv', index=False)