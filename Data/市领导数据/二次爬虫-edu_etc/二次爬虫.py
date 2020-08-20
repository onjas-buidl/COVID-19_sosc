"""
爬取市委书记的具体信息：教育
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
# %%
need_vars = ['sex', 'bmymager', 'nativeplace', 'partytime', 'education', 'majorchara', 'firstjobtime']
ct_list = ['六安市', '柳州市', '桂林市', '百色市', '普洱市', '邯郸市', '安康市', '黄冈市', '陇南市', '天水市', '朝阳市', '怀化市', '淮南市', '曲靖市', '承德市', '辽阳市', '贵港市', '河池市', '白城市', '黄山市', '濮阳市', '郴州市', '咸阳市', '抚州市', '西宁市', '南宁市', '延安市', '赣州市', '昆明市', '景德镇市', '崇左市', '兰州市', '庆阳市', '北海市', '贺州市', '毕节市', '石家庄市', '沧州市', '大同市', '吕梁市', '包头市', '绥化市', '宿州市', '南阳市', '张家界市', '益阳市', '乌海市', '鄂尔多斯市', '鹤岗市', '十堰市', '广元市', '乐山市', '达州市', '齐齐哈尔市', '佛山市', '保山市', '萍乡市', '安庆市', '亳州市', '株洲市', '湘潭市', '邵阳市', '上饶市', '安阳市', '焦作市', '来宾市', '信阳市', '江门市', '日喀则市', '林芝市', '廊坊市', '宜宾市', '南充市', '内江市', '三门峡市', '商丘市', '铜仁市', '淮北市', '南平市', '营口市', '新余市', '吉安市', '洛阳市', '临沧市', '拉萨市', '宜昌市', '雅安市', '蚌埠市', '马鞍山市', '开封市', '平顶山市', '儋州市', '六盘水市', '晋城市', '宁波市', '驻马店市', '孝感市', '舟山市', '新乡市', '周口市', '张家口市', '襄阳市', '大庆市', '池州市', '湛江市', '成都市', '昭通市', '乌鲁木齐市', '克拉玛依市', '芜湖市', '河源市', '钦州市', '昌都市', '榆林市', '白银市', '武威市', '吐鲁番市', '大连市', '深圳市', '吴忠市', '丽江市', '张掖市', '平凉市', '定西市', '赤峰市', '巴彦淖尔市', '哈尔滨市', '巴中市', '山南市', '宝鸡市', '固原市', '中卫市', '太原市', '银川市', '福州市', '滁州市', '长沙市', '常德市', '眉山市', '南京市', '海东市', '衡水市', '漯河市', '嘉峪关市', '酒泉市', '朔州市', '许昌市', '阳江市', '泸州市', '石嘴山市', '鞍山市', '三亚市', '哈密市', '沈阳市', '辽源市', '随州市', '伊春市', '潍坊市', '韶关市', '连云港市', '湖州市', '绍兴市', '金华市', '衢州市', '梧州市', '玉林市', '长治市', '盘锦市', '吉林市', '双鸭山市', '防城港市', '珠海市', '清远市', '东莞市', '呼伦贝尔市', '泉州市', '九江市', '鹰潭市', '盐城市', '宿迁市', '宁德市', '烟台市', '铜川市', '徐州市', '济宁市', '贵阳市', '杭州市', '温州市', '东营市', '泰安市', '惠州市', '云浮市', '绵阳市', '遂宁市', '鸡西市', '嘉兴市', '丽水市', '宣城市', '攀枝花市', '广安市', '锦州市', '荆州市', '广州市', '本溪市', '葫芦岛市', '黄石市', '鹤壁市', '梅州市', '抚顺市', '枣庄市', '鄂州市', '滨州市', '茂名市', '青岛市', '泰州市', '肇庆市', '中山市', '白山市', '佳木斯市', '淮安市', '台州市', '铜陵市', '莆田市', '德州市', '岳阳市', '娄底市', '海口市', '德阳市', '商洛市', '金昌市', '邢台市', '运城市', '通辽市', '丹东市', '阜新市', '无锡市', '常州市', '南通市', '扬州市', '咸宁市', '秦皇岛市', '日照市', '厦门市', '聊城市', '永州市', '三明市', '漳州市', '渭南市', '晋中市', '铁岭市', '长春市', '松原市', '汕头市', '潮州市', '阜阳市', '郑州市', '菏泽市', '资阳市', '安顺市', '通化市', '淄博市', '遵义市', '呼和浩特市', '西安市', '苏州市', '黑河市', '汕尾市', '自贡市', '临汾市', '唐山市', '镇江市', '龙岩市', '衡阳市', '武汉市', '阳泉市', '忻州市', '南昌市', '济南市', '威海市', '临沂市', '揭阳市', '保定市', '四平市', '合肥市', '七台河市', '牡丹江市', '玉溪市', '宜春市', '汉中市', '乌兰察布市', '荆门市']
data = pd.read_csv('Data/所有信息汇总-V1.csv')
data = data[data.ctnm.isin(ct_list)]
data = data[['ctnm', 'name', 'birthmonth']]
# data['name-birth'] = data.name + data.birthmonth.apply(lambda x: str(pd.to_datetime(x)))
# data['name-birth'] = data['name-birth'].apply(lambda x: x[:-12])

# 整理戴敏数据
cs = pd.read_excel('Data/市领导数据/戴敏-new/市委书记.xlsx')
cs = cs[cs.year.isin([2015, 2016, 2017, 2018]) & cs.ctnm.isin(ct_list)]
cs = cs[['name', 'sex', 'bmymager', 'nativeplace', 'partytime', 'education', 'majorchara', 'firstjobtime', 'edu']]
# 只关注这些data
is_miss = cs[need_vars].isnull()
cs['missing_need_var'] = is_miss.sex | is_miss.bmymager | is_miss.nativeplace | is_miss.partytime | is_miss.education | is_miss.majorchara | is_miss.firstjobtime
# cs = cs[~cs['missing_need_var']]

cs.loc[cs.bmymager == '1958-00'] = '1958-01'
cs['name-birth'] = cs.name + cs.bmymager
cs = cs[~cs['name-birth'].duplicated()]
# cs['need_in_total_data'] = cs['name-birth'].isin(data['name-birth'])
data = pd.merge(data, cs, on='name', how='left')
data.drop(['bmymager'], axis=1, inplace=True)
data['missing_need_var'] = data.missing_need_var.fillna(True)
# %% 调和两者
# data['cs_has_data'] = data['name-birth'].isin(cs['name-birth'])
# # 选出不需要爬的：7个var都有
# name_list = list(data[~data.cs_has_data].name)
# todo_df = data[(~data.cs_has_data)][['ctnm', 'name', 'birthmonth']]

# %% 不调和了lmao 直接爬全部的得了

cs_name = '颜赣辉'
cs_city = '宜春市'

names = ['city', 'name', 'bmymager',
        'sex', 'nativeplace', 'partytime', 'education',
        'majorchara', 'firstjobtime', 'edu']

new_dict = dict(zip(names, [[] for _ in names]))
# set keywords to match for each category
match_list = [('sex', ('男', '女')),
              ('nativeplace', ['人']),
              ('partytime', ['加入', '入党']),
              ('education', ['学历', '学', '校', '学院', '专业', '毕业']),
              ('majorchara', ['专业', '系']),
              ('firstjobtime', ['参加工作'])
              ]
df_list = []
error_list = []
save_dict = {}
raw_dict = {}
# %% just get wiki pages
for i in tqdm(range(todo_df.shape[0])):
	cs_name = todo_df.name.iloc[i]
	ct_name = todo_df.ctnm.iloc[i]
	url = 'https://zh.wikipedia.org/wiki/' + cs_name
	response = requests.get(url)

	if response.status_code == 200:
		soup = BeautifulSoup(response.content, "html.parser")
		page = ''
		for p in soup.select('p'):
			page += p.text
		page = zhconv.convert(page, 'zh-cn')
		raw_dict[cs_name] = page
	else:
		print('error', ct_name, cs_name)
		error_list.append(cs_name)
		continue

scraped_df = pd.DataFrame(df_list)
# %% 存一下

with open('Data/市领导数据/二次爬虫-edu_etc/raw_dict_save', 'wb') as file:
	pickle.dump(raw_dict, file)

with open('Data/市领导数据/二次爬虫-edu_etc/raw_dict_save', 'rb') as file:
	raw_dict = pickle.load(file, encoding='bytes')

# %% process scraped data
error_list2, df_list = [], []
todo_df = data[data['missing_need_var']]
for i in tqdm(range(todo_df.shape[0])):
	cs_name = todo_df.name.iloc[i]
	ct_name = todo_df.ctnm.iloc[i]
	# url = 'https://zh.wikipedia.org/wiki/' + cs_name
	# response = requests.get(url)
	try:
		page = raw_dict[cs_name]
	except KeyError:
			# print('key error', ct_name, cs_name)
			error_list2.append(cs_name)
			continue
	if ct_name not in page:
		# print('wrong-page error', ct_name, cs_name)
		error_list2.append(ct_name)
		continue
	phrases = re.split('，|。|；|中华人民共和国政治人物', page)
	# new_dict_ = {}
	# new_dict_['city'] = ct_name
	# new_dict_['name'] = cs_name
	# new_dict_['bmymager'] = todo_df.birthmonth.iloc[i]

	for m in match_list:
		if not pd.isnull(todo_df.loc[todo_df.ctnm == ct_name, m[0]]).iloc[0]:
			continue
		l = []
		for p in phrases:
			if any([(w in p) for w in m[1]]):
				l.append(p)
		todo_df.loc[todo_df.ctnm == ct_name, m[0]] = str(l).replace('\',\'', ' ').replace('[', '').replace(']', '')

	# df_list.append(new_dict_)
	# del new_dict_


# df_list = pd.DataFrame(df_list)
# %% 手动清洗
# df_list['nativeplace'] = df_list.nativeplace.apply(lambda x: x[0][:-1])
todo_df['url'] = 'https://zh.wikipedia.org/wiki/' + todo_df.name
todo_df['baidu'] = 'https://baike.baidu.com/item/' + todo_df.name
todo_df.to_excel('Data/市领导数据/二次爬虫-edu_etc/全291人信息整理.xlsx', index=False)


# %%
a = pd.read_excel('Data/市领导数据/二次爬虫-edu_etc/爬到75人信息整理.xlsx', index=False)