"""
firstjobtime -- ' 年 月 参加工作
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import zhconv
import re
import pickle
import os

# %%
var_2_clean = ['sex', 'nativeplace', 'partytime', 'education', 'majorchara', 'firstjobtime', 'edu']
cs = pd.read_excel('Data/市领导数据/二次爬虫-edu_etc/全291人信息整理 - 手动整理2.xlsx')
