import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei'] # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus'] = False # in case minus sign is shown as box

policy = pd.read_excel('CN_Provinces/CN_Policy/V3-Yuhang_Pan-CN_lockdown_data.xlsx')



wf = pd.read_stata('CN_Provinces/CN_Policy/COVID_LOCKDOWN/data/wf.dta')





