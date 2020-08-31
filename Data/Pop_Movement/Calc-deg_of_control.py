import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']# 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus'] = False # in case minus sign is shown as box

bd = pd.read_excel('Data/Pop_Movement/baidu_index-2019~20/Data/migrate_Trend.xlsx',
                   sheet_name='internalflowhistory')

bd.dropna(inplace=True)
bd.rename(columns={'Unnamed: 0': 'name', 'Unnamed: 1': 'type'}, inplace=True)
bd.loc[bd.name == '吉林市', 'name'] = '吉林'
bd['name'] = bd.name.apply(lambda x: x[:-2] if x[-2:] == '地区' else x)
bd.rename(columns={'name': 'ct_shortname'}, inplace=True)

dates = ['20200124', '20200125', '20200126', '20200127', '20200128', '20200129', '20200130', '20200131', '20200201', '20200202', '20200203', '20200204', '20200205', '20200206', '20200207', '20200208', '20200209', '20200210', '20200211', '20200212', '20200213', '20200214', '20200215', '20200216', '20200217', '20200218', '20200219', '20200220', '20200221', '20200222', '20200223', '20200224', '20200225', '20200226', '20200227', '20200228', '20200229']
dates19 = ['20190124', '20190125', '20190126', '20190127', '20190128', '20190129', '20190130', '20190131', '20190201', '20190202', '20190203', '20190204', '20190205', '20190206', '20190207', '20190208', '20190209', '20190210', '20190211', '20190212', '20190213', '20190214', '20190215', '20190216', '20190217', '20190218', '20190219', '20190220', '20190221', '20190222', '20190223', '20190224', '20190225', '20190226', '20190227', '20190228', '20190301']
dates19_match = ['20190204', '20190205', '20190206', '20190207', '20190208', '20190209', '20190210', '20190211', '20190212', '20190213', '20190214', '20190215', '20190216', '20190217', '20190218', '20190219', '20190220', '20190221', '20190222', '20190223', '20190224', '20190225', '20190226', '20190227', '20190228', '20190301', '20190302', '20190303', '20190304', '20190305', '20190306', '20190307', '20190308', '20190309', '20190310', '20190311', '20190312']
l = list(bd.columns)

# %% create mean difference -- holiday-match
bd['20sum'] = 0
bd['19sum'] = 0
for i in dates:
    bd['20sum'] = bd['20sum'] + bd[i]
bd['20sum'] = bd['20sum'] / len(dates)
for i in dates19_match:
    bd['19sum'] = bd['19sum'] + bd[i]
bd['19sum'] = bd['19sum'] / len(dates)
bd['bd_feb29avgdif_holi'] = bd['19sum'] - bd['20sum']

bd.rename(columns={'name': 'ct_shortname'}, inplace=True)
# %% create mean difference -- date match
bd['20sum'] = 0
bd['19sum'] = 0
for i in dates:
    bd['20sum'] = bd['20sum'] + bd[i]
bd['20sum'] = bd['20sum'] / len(dates)
for i in dates19:
    bd['19sum'] = bd['19sum'] + bd[i]
bd['19sum'] = bd['19sum'] / len(dates)
bd['bd_feb29avgdif_date'] = bd['19sum'] - bd['20sum']

# %% 只搞到15号
dates = dates[:23]
bd['20sum'] = 0
bd['19sum'] = 0
for i in dates:
    bd['20sum'] = bd['20sum'] + bd[i]
bd['20sum'] = bd['20sum'] / len(dates)
for i in dates19_match:
    bd['19sum'] = bd['19sum'] + bd[i]
bd['19sum'] = bd['19sum'] / len(dates)
bd['bd_feb15avgdif_holi'] = bd['19sum'] - bd['20sum']

bd['20sum'] = 0
bd['19sum'] = 0
for i in dates:
    bd['20sum'] = bd['20sum'] + bd[i]
bd['20sum'] = bd['20sum'] / len(dates)
for i in dates19:
    bd['19sum'] = bd['19sum'] + bd[i]
bd['19sum'] = bd['19sum'] / len(dates)
bd['bd_feb15avgdif_date'] = bd['19sum'] - bd['20sum']


bd[['ct_shortname', 'bd_feb15avgdif_date', 'bd_feb15avgdif_holi',
    'bd_feb29avgdif_date', 'bd_feb29avgdif_holi']].to_csv('Data/Pop_Movement/百度迁徙平均政策强度.csv', index=False)
# %% 每个城市每天的 difference
dates = ['20200124', '20200125', '20200126', '20200127', '20200128', '20200129', '20200130', '20200131', '20200201', '20200202', '20200203', '20200204', '20200205', '20200206', '20200207', '20200208', '20200209', '20200210', '20200211', '20200212', '20200213', '20200214', '20200215', '20200216', '20200217', '20200218', '20200219', '20200220', '20200221', '20200222', '20200223', '20200224', '20200225', '20200226', '20200227', '20200228', '20200229']
dates19 = ['20190124', '20190125', '20190126', '20190127', '20190128', '20190129', '20190130', '20190131', '20190201', '20190202', '20190203', '20190204', '20190205', '20190206', '20190207', '20190208', '20190209', '20190210', '20190211', '20190212', '20190213', '20190214', '20190215', '20190216', '20190217', '20190218', '20190219', '20190220', '20190221', '20190222', '20190223', '20190224', '20190225', '20190226', '20190227', '20190228', '20190301']
dates19_match = ['20190204', '20190205', '20190206', '20190207', '20190208', '20190209', '20190210', '20190211', '20190212', '20190213', '20190214', '20190215', '20190216', '20190217', '20190218', '20190219', '20190220', '20190221', '20190222', '20190223', '20190224', '20190225', '20190226', '20190227', '20190228', '20190301', '20190302', '20190303', '20190304', '20190305', '20190306', '20190307', '20190308', '20190309', '20190310', '20190311', '20190312']

holi = False
if holi:
    for i in range(len(dates)):
        bd[str(i)] = bd[dates19_match[i]] - bd[dates[i]]
else:
    for i in range(len(dates)):
        bd[str(i)] = bd[dates19[i]] - bd[dates[i]]

bd = pd.merge(bd, cscv[['ct_shortname', 'prov']], on='ct_shortname', how='left')
exp = bd[['ct_shortname', 'prov'] + [str(i) for i in range(len(dates))]]
# exp.dropna(inplace=True)
exp.to_csv('Data/Pop_Movement/city_bd_diff_holi.csv', index=False)

if holi:
    pd.melt(exp, id_vars=['ct_shortname', 'prov'], value_vars=None, var_name='Date',
            value_name='value', col_level=None).to_csv('Data/Pop_Movement/city_bd_diff_holi-melt.csv', index=False)
else:
    pd.melt(exp, id_vars=['ct_shortname', 'prov'], value_vars=None, var_name='Date',
            value_name='value', col_level=None).to_csv('Data/Pop_Movement/city_bd_diff_date-melt.csv', index=False)

# %% 把每天的病毒数量也加上去？





# %% plot to check -- 按公历日期
# ctnm = '嘉兴'
# city_name = '西宁'
# differences = []
# trend_20 = []
# trend_19 = []
# bd_ = bd[bd.name == city_name]
# # a = bd19[bd19.name == city_name]
# # b = bd20[bd20.name == city_name]
# for i in range(len(dates)):
#        trend_20.append(float(bd_[dates[i]]))
#        trend_19.append(float(bd_[dates19[i]]))
#        # differences.append(a['2019'+i].mean() - b['2020'+i].mean())
#
# plt.plot(dates, trend_20, c='r')
# plt.plot(dates, trend_19, c='b')
# plt.xticks(rotation=45)
# plt.title(city_name+' - 按照公历日期. Red: 2020 Blue: 2019')
# plt.show()
#
#
#
# # city_name = '北京'
# differences = []
# trend_20 = []
# trend_19 = []
# bd_ = bd[bd.name == city_name]
# # a = bd19[bd19.name == city_name]
# # b = bd20[bd20.name == city_name]
# for i in range(len(dates)):
#        trend_20.append(float(bd_[dates[i]]))
#        trend_19.append(float(bd_[dates19_match[i]]))
#        # differences.append(a['2019'+i].mean() - b['2020'+i].mean())
#
# plt.plot(dates, trend_20, c='r')
# plt.plot(dates, trend_19, c='b')
# plt.xticks(rotation=45)
# plt.title(city_name+' - 按照放假日期. Red: 2020 Blue: 2019')
# plt.show()



