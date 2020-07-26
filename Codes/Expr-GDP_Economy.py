import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei'] # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus'] = False # in case minus sign is shown as box

# %% Data Import and Cleaning
cs = pd.read_excel('CN_Provinces/市领导数据/疫情-20市委书记-331ct-V2.xlsx')
econ1 = pd.read_excel('CN_Provinces/不全-1999-2019各地级市GDP及第一二三产业GDP数据.xlsx',
                      sheet_name='GDP第一产业')
econ2 = pd.read_excel('CN_Provinces/不全-1999-2019各地级市GDP及第一二三产业GDP数据.xlsx',
                      sheet_name='GDP第二产业')
econ3 = pd.read_excel('CN_Provinces/不全-1999-2019各地级市GDP及第一二三产业GDP数据.xlsx',
                      sheet_name='GDP第三产业')
econ1 = econ1[econ1.year == 2019]
econ2 = econ2[econ2.year == 2019]
econ3 = econ3[econ3.year == 2019]


