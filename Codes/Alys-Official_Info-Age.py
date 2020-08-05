"""这文档主要
1. 搞2020市委书记数据集
2. 探索市委书记年龄
"""

# %% Imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from tqdm import tqdm
from collections import Counter
# import statsmodels.api as sm
import statsmodels.formula.api as smf

# %% 把全部官员替换疫情中的官员，+ statistical check
cs20 = pd.read_excel('CN_Provinces/市领导数据/疫情-20市委书记-331ct-V2.xlsx')
cs20 = cs20[cs20.provincecode != 420000]  # 只看非湖北的
# 再把辽宁、江西、内蒙古给排除了
cs20 = cs20[cs20.provincecode.apply(lambda code: code not in [210000, 360000, 150000])]


cs20_lc = cs20[cs20.locked_down]
cs20_lc.age_feb20.mean()
cs20[~cs20['locked_down']].age_feb20.mean()


lc_mean = cs20_lc.age_feb20.mean()
c = 0
n = 100000
l = list(cs20.age_feb20)
for i in tqdm(range(n)):
	if np.mean(random.choices(l, k=90)) >= lc_mean:
		c += 1

print('p-value is:', c/n)  # it's fucking significant!


# %% further Histograms
cs20 = pd.read_excel('CN_Provinces/市领导数据/疫情-20市委书记-331ct-V2.xlsx')
cs20 = cs20[cs20.provincecode != 420000]  # 只看非湖北的

cs20.age_feb20.hist(bins=17)
cs20_lc.age_feb20.hist(bins=10, color='red')
plt.title('Age distribution of officials: total vs. lock-down officials')
# plt.savefig('CN_Provinces/市领导数据/Yuhang封城市委书记数据/Age_distrib_by_lockdown.png')
plt.show()
# %% Percentage by age group
from collections import Counter
np.histogram(cs20.age_feb20)
# plot the age group lockdown
c_lk = dict(Counter(cs20_lc.age_feb20))
c_all = dict(Counter(cs20.age_feb20))
# c_lk = np.histogram(cs20_lc.age_feb20, bins=10)
# c_all = np.histogram(cs20.age_feb20, bins=17)

age_range = [i for i in range(44, 62)]
percentages = []
for i in age_range:
	if i not in c_lk.keys():
		percentages.append(0)
	else:
		percentages.append(c_lk[i] / c_all[i])

plt.bar(x=age_range, height=percentages)
# plt.show()
plt.title('Percentage of officials that choosed lockdown vs. Age group')
# plt.savefig('CN_Provinces/市领导数据/Yuhang封城市委书记数据/pct_lck_vs_age.png')
plt.show()




# %% ########## More qualitative exploration ##########
cs20 = pd.read_excel('CN_Provinces/市领导数据/疫情-20市委书记-331ct-V2.xlsx')
cs20.sort_values('provincename', inplace=True)
cols = cs20.columns.tolist()
cols = [cols[-2]] + cols[:-2] + [cols[-1]]
cs20 = cs20[cols]

# %% Regression: how does one extra age contribute to lkd choice

cs = pd.read_excel('Data/市领导数据/疫情-20市委书记-331ct-V2.xlsx')
cs = cs[cs.provincecode != 420000]  # 只看非湖北的
# 再把辽宁、江西、内蒙古给排除了
cs = cs[cs.provincecode.apply(lambda code: code not in [210000, 360000, 150000])]
cs = cs[cs.age_feb20 >= 55]
cs['locked_down'] = cs.locked_down.apply(int)

# mod = sm.OLS(cs.locked_down.apply(int), cs.age_feb20 )
# res = mod.fit()
# print(res.summary())

res = smf.ols('locked_down ~ age_feb20', data=cs).fit()
res.summary()

import seaborn as sns
sns.regplot(y='locked_down', x='age_feb20', data=cs); plt.show()