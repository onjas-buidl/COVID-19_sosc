"""
how effective are the policies in reducing movements.
Just a sanity check here
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']# 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus'] = False # in case minus sign is shown as box

bd = pd.read_excel('CN_Provinces/Pop_Movement/baidu_index-2019~20/Data/migrate_Trend.xlsx',
                   sheet_name='internalflowhistory')
bd.dropna(inplace=True)
bd.rename(columns={'Unnamed: 0': 'name', 'Unnamed: 1': 'type'}, inplace=True)

cols = list(bd.columns)
dates = list(map(lambda d: d[4:], ['20190112', '20190113', '20190114', '20190115',
       '20190116', '20190117', '20190118', '20190119', '20190120', '20190121',
       '20190122', '20190123', '20190124', '20190125', '20190126', '20190127',
       '20190128', '20190129', '20190130', '20190131', '20190201', '20190202',
       '20190203', '20190204', '20190205', '20190206', '20190207', '20190208',
       '20190209', '20190210', '20190211', '20190212', '20190213', '20190214',
       '20190215']))

bd19 = bd[['name', 'type'] + ['2019'+i for i in dates]]
bd20 = bd[['name', 'type'] + ['2020'+i for i in dates]]

policy = pd.read_excel('CN_Provinces/CN_Policy/V3-Yuhang_Pan-CN_lockdown_data.xlsx')
# %% general difference

differences = []
for i in dates:
       differences.append(bd19['2019'+i].mean() - bd20['2020'+i].mean())

plt.plot(differences)
plt.show()

# %% plot a specific city
city_name = '深圳'
differences = []
trend_20 = []
trend_19 = []
a = bd19[bd19.name == city_name]
b = bd20[bd20.name == city_name]
for i in dates:
       trend_20.append(float(b['2020'+i]))
       trend_19.append(float(a['2019' + i]))
       differences.append(a['2019'+i].mean() - b['2020'+i].mean())

plt.plot(dates, trend_20, c='r')
plt.plot(dates, trend_19, c='b')
plt.xticks(rotation=45)
plt.title(city_name+' - in-city movement plot. Red: 2020 Blue: 2019')
plt.show()

