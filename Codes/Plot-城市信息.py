import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import requests
import json
from tqdm import tqdm
import statsmodels.api as sm
import seaborn as sns; sns.set(color_codes=True)

data = pd.read_csv('Data/每日确诊+市委书记信息+副省级+GDP+pop+产业结构-V1.csv')
dates = ['2020-01-'+str(i) for i in range(24, 32)] + \
        ['2020-02-0'+str(i) for i in range(1, 10)] + ['2020-02-'+str(i) for i in range(10, 30)]

data = data[data.prov != '湖北省']
data = data[~data['自治州-盟-地区']]

# %% statsmodels
sns.regplot(data.primary_ind, data.gdp2018, ); plt.show()

mod = sm.OLS(data.gdp2018, data.primary_ind)
res = mod.fit()
res.summary()
res.params


# %%
import statsmodels.formula.api as smf
results = smf.ols('gdp2018 ~ primary_ind', data=data).fit()
results.summary()




# %%
data[['gdp2018', 'primary_ind']].to_stata('Data/每日确诊_市委书记信息_副省级_GDP_pop_产业结构_V1.dta', write_index=False)

data.popHR18_all / data.gdp2018











