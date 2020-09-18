import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from tqdm import tqdm
import seaborn as sns



d = pd.read_stata('Data/Xi_Chen_data/2019-nCoV.dta')
data = pd.read_stata('Data/Xi_Chen_data/2019-nCoV.dta', iterator=True)
l = data.variable_labels()

d.groupby('date').sum().lockdown
d.groupby('date').sum().closed

d[d.date == "2020-01-29"].lockdown.sum()
