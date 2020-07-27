"""
本文件希望产生一个 csv data, s.t. 每个城市每天的COVID info 都在上面
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib
from tqdm import tqdm



dates = ['2020-01-'+str(i) for i in range(24, 32)] + \
        ['2020-02-0'+str(i) for i in range(1, 10)] + ['2020-02-'+str(i) for i in range(10, 30)]

dates_label = list(map(lambda x: x[6:], dates)) # [i for i in range(24, 32)]+[i for i in range(1, 30)]
dates_label2 = list(map(lambda x: x[5:]+'-'+'2020', dates))


# %% prepare
city_keys = ['cityName', 'confirmedCount', 'suspectedCount', 'curedCount', 'deadCount']
prov_keys = ['provinceName', 'provinceShortName', 'confirmedCount', 'suspectedCount', 'curedCount', 'deadCount', 'comment']
# city_df = pd.DataFrame(columns=['date']+city_keys)
# prov_df = pd.DataFrame(columns=['date']+prov_keys)
prov_df_list = []
city_df_list = []
new_city_ = {'cityName': -1,
 'confirmedCount': -1,
 'suspectedCount': -1,
 'curedCount': -1,
 'deadCount': -1}
new_prov_ = {'provinceName': -1,
 'provinceShortName': -1,
 'confirmedCount': -1,
 'suspectedCount': -1,
 'curedCount': -1,
 'deadCount': -1,
 'comment': -1}
# %% Do the conversion loop
for d in tqdm(dates):
	with open('Data/COVID-19/DXY-CN-by_city/' + d + '.json') as json_file:
		day = json.load(json_file)
	for p in day:
		new_prov = new_prov_.copy()
		new_prov['date'] = d
		for k1 in p.keys():
			if k1 != 'cities':
				new_prov[k1] = p[k1]
		# prov_df = prov_df.append(new_prov, ignore_index=True)
		prov_df_list.append(new_prov)
		if p['provinceName'][-1] == '市':
			continue

		for city in p['cities']:
			new_city = new_city_.copy()
			new_city['date'] = d
			new_city['prov'] = p['provinceName']
			for k2 in city.keys():
				new_city[k2] = city[k2]
			# city_df = city_df.append(new_city, ignore_index=True)
			city_df_list.append(new_city)


df_city = pd.DataFrame(city_df_list)
df_prov = pd.DataFrame(prov_df_list)
not_city = ['临高县', '陵水县', '固始县', '呼伦贝尔牙克石市', '包头市东河区',
            '锡林郭勒盟锡林浩特', '鄂尔多斯东胜区', '赤峰市松山区', '兴安盟乌兰浩特', '通辽市经济开发区',
            '锡林郭勒盟二连浩特', '鄂尔多斯鄂托克前旗', '呼伦贝尔牙克石', '琼中县', '呼伦贝尔牙克石市']
to_remove = ['宁东管委会', '通辽市经济开发区', '待明确地区', '未知地区', '未明确地区', '监狱系统', '省十里丰监狱',
             '包头市东河区', '外地来粤人员', '赤峰市松山区']
city_rename = {'丽江市': '丽江', '西双版纳州': '西双版纳', '漯河市': '漯河', '白银市': '白银',
               '琼海市': '琼海', '东方市': '东方', '吐鲁番市': '吐鲁番', '四平市': '四平',
               '第八师石河子市': '石河子', '乌海市': '乌海', '兵团第八师石河子市': '石河子',
               '鹤壁市':'鹤壁', '淄博市':'淄博', '安阳市':'安阳', '邯郸市':'邯郸', '金昌市':'金昌',
               '天水市':'天水', '平凉市':'平凉', '吉林市':'吉林', '临高县':'临高','凉山':'凉山州',
               '昌吉':'昌吉州', '楚雄':'楚雄州', '澄迈县':'澄迈', '琼中县':'琼中', '红河':'红河州',
               '锡林郭勒': '锡林郭勒盟', '长垣县':'长垣', '阿克苏':'阿克苏地区', '陵水县':'陵水',
               '文山':'文山州'}

# %% Clean the raw dataframes -- city

df_city = df_city[~df_city.cityName.isin(to_remove)]
df_city['cityName'] = df_city.cityName.apply(lambda x: city_rename[x] if x in city_rename.keys() else x)
df_city = df_city[~df_city.cityName.str.contains('第', '师')] # 删除新疆兵团
# df_city.cityName.apply(lambda x: x[:-1] if x[-1] == '市')
# df_city.cityName.uniq33ue()
# df_city.to_csv('Data/COVID-19/me-市级新冠数据V0.1.csv')
df_city.drop(756, inplace=True) # drop a 漯河 row
# ct = '嘉兴'
# aggregate data
city_agg_df = []
new_city_ = dict(zip(dates, [-1 for _ in range(len(dates))]))

for ct in tqdm(df_city.cityName.unique()):
	a = df_city[df_city.cityName == ct]
	a.drop_duplicates(inplace=True)
	new_city = new_city_.copy()
	for d in a.date.unique():
		new_city['cityName'] = ct
		assert len(a.prov.unique()) == 1
		new_city['prov'] = a.prov.unique()[0]
		new_city[d] = int(a[a.date == d]['confirmedCount'].values)
	city_agg_df.append(new_city)
	del new_city

city_agg_df = pd.DataFrame(city_agg_df)
city_agg_df.replace(-1, np.nan, inplace=True)
city_agg_df.to_csv('Data/COVID-19/me-市级新冠数据V1.0.csv')
df_prov = df_prov[~df_prov.provinceName.str.contains('待明确地区', '澳门')]
df_prov = df_prov[~df_prov.provinceName.str.contains('台湾', '香港')]

# %% 省级数据清洗
prov_agg_df = []

new_prov_ = dict(zip(dates, [-1 for _ in range(len(dates))]))
for p in tqdm(df_prov.provinceName.unique()):
	a = df_prov[df_prov.provinceName == p]
	a.drop_duplicates(inplace=True)
	new_prov = new_prov_.copy()
	for d in a.date.unique():
		new_prov['provinceName'] = p
		new_prov['provinceShortName'] = a['provinceShortName'].unique()[0]
		# assert len(a.prov.unique()) == 1
		# new_city['prov'] = a.prov.unique()[0]
		new_prov[d] = int(a[a.date == d]['confirmedCount'].values)
	prov_agg_df.append(new_prov)
	del new_prov

prov_agg_df = pd.DataFrame(prov_agg_df)
prov_agg_df.replace(-1, np.nan, inplace=True)
prov_agg_df.to_csv('Data/COVID-19/me-省级新冠数据V1.0.csv')
