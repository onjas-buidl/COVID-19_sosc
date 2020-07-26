import pandas as pd
import matplotlib.pyplot as plt
import json

p = pd.read_excel('CN_Provinces/CN_Policy/V1-Yuhang_Pan-CN_lockdown_data.xlsx')

with open('CN_Provinces/省市对照表.json') as json_file:
    code2city = json.load(json_file)
city2code = dict(map(reversed, code2city.items()))

def return_prov(city_name):
    if city_name in city2code.keys():
        code = city2code[city_name]
        return code2city[code[:2]+'0000']
    else:
        return '?????'

p['prov'] = p.city_name2010.apply(return_prov)
p['city_code2020'] = p.city_name2010.apply(lambda x: city2code[x])

p.to_excel('CN_Provinces/CN_Policy/V2-Yuhang_Pan-CN_lockdown_data.xlsx')

