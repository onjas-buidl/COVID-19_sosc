import pandas as pd
import numpy as np


gdp = pd.read_csv('Data/Geo_data_CN/GDP/tabula-gdp2018-clean.csv')

gdp = gdp[gdp.year == 2018]



