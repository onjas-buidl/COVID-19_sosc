import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei']# 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus'] = False # in case minus sign is shown as box

dates = ['2020-01-'+str(i) for i in range(24, 32)] + \
        ['2020-02-0'+str(i) for i in range(1, 10)] + ['2020-02-'+str(i) for i in range(10, 30)]

dates_label = list(map(lambda x: x[6:], dates))# [i for i in range(24, 32)]+[i for i in range(1, 30)]
dates_label2 = list(map(lambda x: x[5:]+'-'+'2020', dates))


def get_city_info(ct_name='嘉兴', prov_name="浙江省",search_type='confirmedCount'):
    """all possible types: currentConfirmedCount, confirmedCount, suspectedCount, curedCount, deadCount"""
    count = []
    dict_memory = {i: 0 for i in dates}
    if ct_name:
        for d in dates:
            with open('COVID-19/DXY-CN-by_city/' + d + '.json') as json_file:
                day = json.load(json_file)
            for p in day:
                if p['provinceName'] == prov_name:
                    for city in p['cities']:
                        if city['cityName'] == ct_name:
                            count.append(city[search_type])
                            dict_memory[d] = city[search_type]
    else:
        for d in dates:
            with open('COVID-19/DXY-CN-by_city/' + d + '.json') as json_file:
                day = json.load(json_file)
            for p in day:
                if p['provinceName'] == prov_name:
                        count.append(p[search_type])
                        dict_memory[d] = p[search_type]

    if len(count) == 0:
        print('Cannot find city!')
        return
    elif len(count) != len(dates):
        print('Size don\'t match, try to interpolate')
    # df = pd.DataFrame({'date':dates_label2, search_type:count})
    # df['date'] = df.date.apply(pd.to_datetime)
    # df.set_index('date', inplace=True)
    # df.plot()
    # df[search_type].plot(sty)
    plt.bar(height=count, x=dates_label)
    # plt.xlabel(dates_label)
    plt.xticks(rotation=65)
    if ct_name:
        plt.title(ct_name +' - '+search_type)
    else:
        plt.title(prov_name + ' - ' + search_type)
    plt.show()
    plt.close(fig='all')
    return count

# get_city_info(ct_name='秦皇岛',
#               prov_name='河北省')


# %% manually produce dictionary
def get_city_info_dict(prov_name='河北省',
    ct_name='保定',
    search_type='confirmedCount'):
    # prov_name='河北省'
    # ct_name='保定'
    # search_type='confirmedCount'
    count = []
    dict_memory = {i: 0 for i in dates}
    if prov_name[-1:]!='市':
        for d in dates:
            with open('COVID-19/DXY-CN-by_city/' + d + '.json') as json_file:
                day = json.load(json_file)
            for p in day:
                if p['provinceName'] == prov_name:
                    for city in p['cities']:
                        if city['cityName'] == ct_name:
                            count.append(city[search_type])
                            dict_memory[d] = city[search_type]
    else:
        for d in dates:
            with open('COVID-19/DXY-CN-by_city/' + d + '.json') as json_file:
                day = json.load(json_file)
            for p in day:
                if p['provinceName'] == prov_name:
                    count.append(p[search_type])
                    dict_memory[d] = p[search_type]
    return dict_memory

# dict_memory
get_city_info_dict(prov_name='上海市', ct_name='保定', search_type='confirmedCount')

def first_case_date(dict_memory):
    for k in dict_memory.keys():
        if dict_memory[k] > 0:
            return k
    return 'No_case'

# %% prepare data for Plot lockdown timeline
pc = pd.read_excel('CN_Provinces/CN_Policy/V2-Yuhang_Pan-CN_lockdown_data.xlsx')
# add two columns to this policy data -- one showing time since Wuhan lockdown, the other show
# time since first case
pc.rename(columns={'new_start': 'lockdown'}, inplace=True)
pc['lockdown'] = pc['lockdown'].apply(lambda x: str(x)[4:6]+'-'+str(x)[6:8]+'-2020')
pc['lockdown'] = pc['lockdown'].apply(pd.to_datetime)

wuhan_lockdown = pc['lockdown'][0]
pc['daySinceWuhanLock'] = (pc.lockdown - pc['lockdown'][0]).apply(lambda x: x.days)

# get date of first case
pc['city_name2010'] = pc['city_name2010'].apply(lambda n: n[:-1] if n[-1]=='市' else n )
pc['dateFirstCase'] = \
    pc.apply(lambda r: first_case_date(get_city_info_dict(
        ct_name=r.city_name2010, prov_name=r.prov)), axis=1)
pc.at[8, 'dateFirstCase'] = '2020-01-25' # 湖北咸宁
pc.at[9, 'dateFirstCase'] = '2020-01-24' # 恩施

pc.at[15, 'dateFirstCase'] = '2020-02-15' # 山东东营好像没有病例 -- 直接算成 2.15吧
# https://www.zhihu.com/question/369952861
pc.at[38, 'dateFirstCase'] = '2020-02-15' # 辽宁抚顺好像没有病例 -- 直接算成 2.15
pc.at[94, 'dateFirstCase'] = '2020-02-15' # 内蒙古阿拉善盟好像没有病例 -- 算成 2.15

pc.at[56, 'dateFirstCase'] = '2020-01-24' # 山东-济南-莱芜区直接算成济南市的情况
# pc['dateFirstCase'] = pc['dateFirstCase'].apply(lambda x: str(x)[4:6]+'-'+str(x)[6:8]+'-2020')
pc['dateFirstCase'] = pc['dateFirstCase'].apply(pd.to_datetime)
pc['daySinceFirstCase'] = (pc['dateFirstCase'] - pc['lockdown']).apply(lambda x: x.days)

# 对于没有病例的那几位，再设为 +20
pc.at[15, 'daySinceFirstCase'] = 20 # 山东东营好像没有病例 -- 直接算成 2.15吧
pc.at[38, 'daySinceFirstCase'] = 20 # 辽宁抚顺好像没有病例 -- 直接算成 2.15
pc.at[94, 'daySinceFirstCase'] = 20 # 内蒙古阿拉善盟好像没有病例 -- 算成 2.15

pc.to_excel('CN_Provinces/CN_Policy/V3-Yuhang_Pan-CN_lockdown_data.xlsx')

# %% simple plot
plt.scatter(x=list(pc.daySinceFirstCase), y=list(pc.daySinceWuhanLock))
plt.show()
plt.close(fig='all')


# %% plot with label
fig, ax = plt.subplots(figsize=(15, 15))
# fig.set_dpi
for i in range(pc.shape[0]):
    plt.plot(pc.iloc[i].daySinceWuhanLock, pc.iloc[i].daySinceFirstCase, '.')
    plt.text(pc.iloc[i].daySinceWuhanLock, pc.iloc[i].daySinceFirstCase,
             pc.iloc[i].city_name2010)
# plt.show()
plt.xlabel('Lockdown Time (day since Wuhan lockdown)')
plt.ylabel('Lockdown Date since first case in the city')
plt.title('Graph showing Policy Responsiveness Among Lockdown cities (东营、抚顺、阿拉善盟 didn\'t have a case)')
plt.savefig('CN_Provinces/*Graphs/firstCase-VS-wuhanLockdown.png', dpi=300)
plt.close(fig='all')

# ================
# %% 第一例病毒的时间
prov_firsts = {}
# note!! 上海数据有误，第一天应该是 1.21
city_firsts = {}
for d in dates:
    with open('COVID-19/DXY-CN-by_city/' + d + '.json') as json_file:
        day = json.load(json_file)
    for p in day:
        if p['provinceName'] not in prov_firsts.keys() and p['confirmedCount'] != 0:
            prov_firsts[p['provinceName']] = d
        for ct in p['cities']:
            if ct['cityName'] not in city_firsts.keys() and ct['confirmedCount'] != 0:
                city_firsts[ct['cityName']] = d




df = pd.DataFrame({'dates': list(city_firsts.values()), 'c':1})
df.groupby('dates').count()