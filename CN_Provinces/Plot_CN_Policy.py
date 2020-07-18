import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import requests
import json
from tqdm import tqdm


with open('CN_Provinces/省市对照表.json') as json_file:
    code2city = json.load(json_file)
city2code = dict(map(reversed, code2city.items()))

# %% load data -- cts (map of all cities)
cts = gpd.read_file('CN_Provinces/Geo_data_CN/chn_admbnda_adm2_ocha.shp', encoding='utf-8')
cts['ADM2_ZH'] = cts.ADM2_ZH.apply(lambda x: x[:-3] if ('〔' in x or '[' in x) else x)
cts.at[6, 'ADM2_ZH'] = '莱芜区'
replace_n = {'海西蒙古族自治州':'海西蒙古族藏族自治州', '那曲地区':'那曲市', '株州市':'株洲市'}
cts['ADM2_ZH'] = cts.ADM2_ZH.apply(lambda x: replace_n[x] if x in replace_n.keys() else x)
cts = cts[(cts.ADM2_ZH != '香港') & (cts.ADM2_ZH != '澳门')]
# cts['city_code2020'] = cts.ADM2_PCODE.apply(lambda s: int(s[2:]))
cts['city_code2020'] = cts.ADM2_ZH.apply(lambda s: city2code[s])
cts.set_index('city_code2020', inplace=True)

a = pd.DataFrame(cts.drop('geometry', axis=1))
# cn is the map of provincial boundaries
cn = gpd.read_file('CN_Provinces/Geo_data_CN/全国.json')

dates = [str(i) for i in range(20200123, 20200132)] + \
	[str(i) for i in range(20200201, 20200214)]

policy = pd.read_excel('CN_Provinces/CN_Policy/V2-Yuhang_Pan-CN_lockdown_data.xlsx')

# %% create date columns in map to show policy situation

for d in dates:
	cts[d] = 0
	for n in policy['city_code2020']:
		if int(policy[policy.city_code2020 == n]['new_start'].values) <= int(d):
			cts.at[str(n), d] = 1
a = pd.DataFrame(cts.drop('geometry', axis=1))


for n in policy['city_code2020']:
	assert str(n) in cts.index

# %% Plotting pictures for animation
for d in tqdm(dates):
	fig, ax = plt.subplots(figsize=(15, 15))
	cn.boundary.plot(ax=ax)
	cts.plot(ax=ax, column=d)
	plt.title('Locked-down Cities on '+ d[:4] + '-' + d[4:6] + '-' + d[6:])
	plt.savefig('CN_Provinces/Geo_data_CN/animate_Yuhang_policy/'+d+'.png')
	plt.close(fig='all')
# %% ========================
# %% Plot time since Wuhan lockdown and first case in town
import subprocess
subprocess.call(["python", "plot-Virus_info.py"], cwd="CN_Provinces")