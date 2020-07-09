"""
北京的数据不太好 有中央部委的，没什么地方性的。
湖北的数据，obviously, 也不太好
西藏没有任何relax policy的数据（官网上有） -- 数据收集有疏漏
	暂时除去西藏数据
"""

from functools import reduce
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# import seaborn
# from scipy.interpolate import spline
import numpy as np

matplotlib.rcParams['font.sans-serif'] = ['SimHei']# 用黑体显示中文
# matplotlib.rcParams['font.sans-serif']=['FangSong']
# matplotlib.rcParams['axes.unicode_minus']=False
matplotlib.rcParams['axes.unicode_minus'] = False # in case minus sign is shown as box


xg1 = pd.read_csv('Gov_data/CH_media_zky/新冠1.csv')
xg2 = pd.read_csv('Gov_data/CH_media_zky/新冠2.csv')
xg1.dropna(inplace=True)
xg2.dropna(inplace=True)
xg = xg1.append(xg2)
xg.rename(columns={'标题': 'title', '发布日期': 'date', '省份': 'prov'}, inplace=True)
xg = xg[xg.prov != '西藏']
xg.drop(xg[xg.prov == '省份'].index, inplace=True)
del xg['操作']
del xg1, xg2

def remove_dot(s):
	if ('...' ==  s[-3:]):
		return s[:-3]
	else:
		return s


xg['title'] = xg['title'].apply(remove_dot)
xg.drop_duplicates(inplace=True)

xg['date'] = xg['date'].apply(pd.to_datetime)
xg.set_index('date', inplace=True)

control_words = ['联防联控', '监督', '举报', '工作实施', '基层医疗卫生', '遗体', '物资保障', '绿色通道', '爱国卫生运动', '大清扫', '大消毒',
                 '延迟企业复工', '集中收治', '排查力度', '阻断传播', '工作指挥部', '紧急通知', '防控工作', '新闻发布会',
                 '一律', '无条件', '收治', '一级应急',  '应急响应', '禁止', '严禁', '部署防控', '通行证', '核酸', '防控措施',
                 '严防', '联防联控', '隔离', '积极防控', '国家卫健委', '国家卫生健康委员会', '防控指挥部',
                 '定点救治', '定点医院', '闭园', '暂停春节部分节庆活动', '结构安装完成', '紧急通告', '暂停', '严密布防',
                 '推迟开学', '停运', '健康码', '健康信息码', '二维码', '加快抗疫', '进一步规范', '疫情防控', '健康管理工作',
                 '医用防护服', '严密防控', '直报系统', '消毒', '遏制疫情', '大数据', '集中筛查', '口罩', '线上开学', '疫情输入']
relax_words = ['复工', '复产', '开工', '扩产', '解除', '返企', '逐步恢复']
no_words = ['众志成城', '友情', '提示', '温情', '一封信', '爱', '暖心', '琐碎',
            '习近平', '李克强', '国新办']    # central gov

# def count_words(title, word_list):
# 	c = 0
# 	for word in word_list:
# 		if (word in title) and (word not in no_words):
# 			c += 1
# 	return c
#
#
# count_contorl = lambda x: count_words(x, control_words)
# count_relax = lambda x: count_words(x, relax_words)
#
# xg['count_control'] = xg['title'].apply(count_contorl)
# xg['count_relax'] = xg['title'].apply(count_relax)

def give_type(title):
	c = 0
	for word in control_words:
		if word in title:
			# c += 1
			c = 1
			break
	for word in relax_words:
		if word in title:
			# c -= 100
			c = -1
			break
	for word in no_words:
		if word in title:
			c = 0
			break
	return c


xg['type'] = xg['title'].apply(give_type)
# %% ========== 全国抗疫+放松政策排名


a = xg[(xg.type == 1)].groupby('prov').count()
a.rename(columns={'type':'control_count'}, inplace=True)
b = xg[(xg.type == -1)].groupby('prov').count()
a['relax_count'] = b['type']
a.sort_values(by='control_count', ascending=False, inplace=True)

a.plot(y = ['control_count', 'relax_count'], kind='bar')
plt.title('control+relax policy count')
plt.xticks(rotation=45)
leg = plt.legend()
plt.savefig('Gov_data/CH_media_zky/Graphs/control-relax_policy_by_prov.png', dpi=300)
plt.show()

# %% control和relax的比值
a = xg[(xg.type == 1)].groupby('prov').count()
a.rename(columns={'type':'control_count'}, inplace=True)
b = xg[(xg.type == -1)].groupby('prov').count()
a['relax_count'] = b['type']
a['strigency_ratio'] = a['control_count'] / a['relax_count']
a.sort_values(by='strigency_ratio', ascending=False, inplace=True)

a.plot(y = 'strigency_ratio', kind='bar')
plt.title('2020年一月到四月各省strigency index')
plt.xticks(rotation=45)
leg = plt.legend()
plt.savefig('Gov_data/CH_media_zky/Graphs/2020年一月到四月各省strigency_index.png', dpi=300)
# plt.show()


# %% ========== 全国初期抗疫政策 by 省

a = xg[(xg.type == 1) & (xg.index >= '2020-01-01') & (xg.index <= '2020-03-01')].groupby('prov').describe()
a.sort_values(by=[('type', 'count')], ascending=False, inplace=True)
plt.xticks(rotation=45)
plt.bar(x=a[('type', 'count')].index, height=list(a[('type', 'count')]) )
plt.title('Number of COVID-Targeting Policies before Mar 2020')
plt.savefig('Gov_data/CH_media_zky/Graphs/initial_control_policy_by_prov.png', dpi=300)
# plt.show()

# %% ========== 全国放松政策 by 省
a = xg[(xg.type == -1)].groupby('prov').describe()
a.sort_values(by=[('type', 'count')], ascending=False, inplace=True)
plt.xticks(rotation=45)
plt.bar(x=a[('type', 'count')].index, height=list(a[('type', 'count')]) )
plt.title('Number of Relaxing Policies')
plt.savefig('Gov_data/CH_media_zky/Graphs/relax_policy_by_prov.png', dpi=300)
# plt.show()

# %% ========== 多省份抗疫政策变化图
# t = xg[xg.type == 1]
# t[t.type == 1].groupby(t.index).sum().plot()


prov_list = ['上海', '广东', '宁夏', '青海']
# prov_list = ['内蒙古', '河南', '吉林', '福建']
fig, ax = plt.subplots()
plt.ylim((0, 22))
for p in prov_list:
	t = xg[(xg.type == 1) & (xg.prov == p)]
	ax.plot(t.groupby(t.index).sum(), label=p)

	# xnew = np.linspace(t.min(), t.max(), 300)
	# power_smooth = spline(T, power, xnew)
	# plt.plot(xnew, power_smooth)

plt.title('抗疫政策变化图')
fig.autofmt_xdate()
ax.fmt_xdata = mdates.DateFormatter('%m-%d')
leg = ax.legend()
# plt.show()
plt.savefig('Gov_data/CH_media_zky/Graphs/随时间变化-'+reduce(lambda i,j: i+j, prov_list) +'.png')

# %% ========== 单省份抗疫政策变化图
# t = xg[xg.type == 1]
# t[t.type == 1].groupby(t.index).sum().plot()

p = '黑龙江'
fig, ax = plt.subplots()
plt.ylim((0, 22))

t = xg[(xg.type == 1) & (xg.prov == p)]
ax.plot(t.groupby(t.index).sum(), label='抗疫')

t = xg[(xg.type == -1) & (xg.prov == p)]
ax.plot((-1)*t.groupby(t.index).sum(), label='放松')
# xnew = np.linspace(t.min(), t.max(), 300)
# power_smooth = spline(T, power, xnew)
# plt.plot(xnew, power_smooth)

plt.title(p + '抗疫-放松政策变化图')
fig.autofmt_xdate()
ax.fmt_xdata = mdates.DateFormatter('%m-%d')
leg = ax.legend()
plt.show()
# plt.savefig('Gov_data/CH_media_zky/Graphs/随时间变化-'+reduce(lambda i,j: i+j, prov_list) +'.png')



# %% maximum policy per day
m = 10
l = list(xg.prov.unique())
for p in l:
	t = xg[(xg.type == 1) & (xg.prov == p)]
	i = int(t.groupby(t.index).sum().max())
	if i > m:
		m = i
# 最多一天22条

