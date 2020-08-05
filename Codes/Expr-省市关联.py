import pandas as pd
import matplotlib.pyplot as plt
import json
from tqdm import tqdm
import seaborn as sns; sns.set(color_codes=True)
import statsmodels.formula.api as smf

data = pd.read_csv('Data/每日确诊+市委书记信息+副省级+GDP+pop+产业结构+省一级响应-V1.csv')
# %%
res = smf.ols('locked_down ~ yiji_num', data=data).fit()
res.summary()



