import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

pc = pd.read_excel('CN_Provinces/CN_Policy/V4-Yuhang_Pan-CN_lockdown_data加官员信息.xlsx')

sj = pd.read_excel('CN_Provinces/戴敏市领导数据/市委书记.xlsx')
sj = sj[sj.year==2018]
# sj['birth'] = sj.bmymager.apply(pd.to_datetime)
sj.age.mean()
sj.age.hist()
plt.show()



pc['age'] = (pd.to_datetime('2020-02-01') - pc['birthmonth']).astype('<m8[Y]')
pc.age.mean()
pc.age.hist()
plt.show()


# %% perform Statistical significance test
c = 0
l = list(sj.age.dropna())
for i in range(10000):
	# selected = []
	# for j in range(pc.shape[0]):
	# 	selected.append(random.choice(l))

	if np.mean(random.choices(l, k=pc.shape[0])) >= 55.6:
		c += 1


