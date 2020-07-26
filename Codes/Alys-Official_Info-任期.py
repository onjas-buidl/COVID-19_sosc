import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from tqdm import tqdm
from collections import Counter
import statsmodels.api as sm

# %% basic plot
cs = pd.read_excel('CN_Provinces/市领导数据/疫情-20市委书记-331ct-V2.xlsx')
cs.tenure.hist(bins=8)
plt.show()
cs_lc = cs[cs.locked_down]

# %% Plot percentage that lockdown
c_lk = dict(Counter(cs_lc.tenure))
c_all = dict(Counter(cs.tenure))
# c_lk = np.histogram(cs20_lc.age_feb20, bins=10)
# c_all = np.histogram(cs20.age_feb20, bins=17)

tenure_range = [i for i in range(0, 9)]
percentages = []
for i in tenure_range:
	if i not in c_lk.keys():
		percentages.append(0)
	else:
		percentages.append(c_lk[i] / c_all[i])

# 同时 plot bar graph line graph (two axses)
plt.figure()
plt.bar(tenure_range, percentages, label='lck percentage')
plt.ylabel('Percentage of lockdown')
axes2 = plt.twinx()
axes2.plot(tenure_range, list(reversed(list(c_all.values()))),
           label='number of officials', color='orange')
axes2.set_ylabel('Number of officials')

plt.title('Percentage of officials that choosed lockdown vs. Tenure in Feb 2020')
plt.legend()
# plt.show()
plt.savefig('CN_Provinces/市领导数据/Yuhang封城市委书记数据/pct_lck_vs_tenure.png')
plt.close(fig='all')


# %% Causal analysis with OLS

cs = pd.read_excel('CN_Provinces/市领导数据/疫情-20市委书记-331ct-V2.xlsx')
cs = cs[cs.provincecode != 420000]  # 只看非湖北的
# 再把辽宁、江西、内蒙古给排除了
# cs = cs[cs.provincecode.apply(lambda code: code not in [210000, 360000, 150000])]

cs = cs[cs.tenure <= 5]
# cs = cs[(cs.tenure <= 4) & (cs.tenure >= 3)]

# mod = sm.OLS(cs.locked_down.apply(int), cs.tenure)
mod = sm.OLS(cs.locked_down.apply(int), cs[['tenure', 'age_feb20']])
res = mod.fit()
print(res.summary())


