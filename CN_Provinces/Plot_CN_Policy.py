import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import requests
import json
from tqdm import tqdm

# %% load maps
map = gpd.read_file('CN_Provinces/Geo_data_CN/chn_admbnda_adm2_ocha.shp', encoding='utf-8')
a = pd.DataFrame(map)
cn = gpd.read_file('CN_Provinces/Geo_data_CN/全国.json')

# %% get city-level geopandas data

with open('CN_Provinces/Prov-city.json') as json_file:
    code2city = json.load(json_file)
codes = []
for c in code2city.keys():
	if c[-2:] == '00':
		codes.append(c)
# %%
cn = pd.DataFrame()
CN = gpd.GeoDataFrame()
error_list = []
save_dict = {}
# %%
for c in tqdm(codes):
	r = requests.get('https://geo.datav.aliyun.com/areas_v2/bound/'+c+'_full.json')
	if r.status_code != '200':
		error_list.append(c)
		continue
	open('/Users/qitianhu/Downloads/' + c + '.json', 'wb').write(r.content)

	# save_dict[c] = r.text
	# CN = CN.append(json.loads(r.text), ignore_index=True)
	# cn = cn.append(json.loads(r.text), ignore_index=True)
	# open('facebook.ico', 'wb').write(r.content)

# %%


a = gpd.read_file('/Users/qitianhu/Downloads/黑龙江省.json')

r = requests.get('https://geo.datav.aliyun.com/areas_v2/bound/230600_full.json')



a.plot()
plt.show()