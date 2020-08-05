import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import requests
import json
from tqdm import tqdm
import statsmodels.api as sm
import seaborn as sns; sns.set(color_codes=True)


data = pd.read_csv('Data/每日确诊+市委书记信息+副省级+GDP+pop+产业结构-V1.csv')

# %%
a = data[['prov', 'age_feb20']].groupby('prov').mean()


