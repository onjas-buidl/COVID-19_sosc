# %%


with open('Data/Geo_data_CN/民政部2020年5月中华人民共和国县以上行政区划代码') as file:
	lines = file.readlines()
lines = lines[2:] # 删除开头两行
# s删除港澳台
lines = lines[:-3]
# %%
for i in range(len(lines)):
	lines[i] = lines[i][:-7]
	lines[i] = lines[i].split('\t')
	lines[i][1] = lines[i][1].strip()
	lines[i] = tuple(lines[i])

lines = dict(lines)
import json

with open('Data/Geo_data_CN/民政部2020年5月中华人民共和国县以上行政区划代码.json', 'w') as fp:
    json.dump(lines, fp)