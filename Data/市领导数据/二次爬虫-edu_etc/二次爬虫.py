import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# import random
from tqdm import tqdm
# from collections import Counter
# import statsmodels.api as sm
import requests
from bs4 import BeautifulSoup
import zhconv


ct_list = ['六安市', '柳州市', '桂林市', '百色市', '普洱市', '邯郸市', '安康市', '黄冈市', '陇南市', '天水市', '朝阳市', '怀化市', '淮南市', '曲靖市', '承德市', '辽阳市', '贵港市', '河池市', '白城市', '黄山市', '濮阳市', '郴州市', '咸阳市', '抚州市', '西宁市', '南宁市', '延安市', '赣州市', '昆明市', '景德镇市', '崇左市', '兰州市', '庆阳市', '北海市', '贺州市', '毕节市', '石家庄市', '沧州市', '大同市', '吕梁市', '包头市', '绥化市', '宿州市', '南阳市', '张家界市', '益阳市', '乌海市', '鄂尔多斯市', '鹤岗市', '十堰市', '广元市', '乐山市', '达州市', '齐齐哈尔市', '佛山市', '保山市', '萍乡市', '安庆市', '亳州市', '株洲市', '湘潭市', '邵阳市', '上饶市', '安阳市', '焦作市', '来宾市', '信阳市', '江门市', '日喀则市', '林芝市', '廊坊市', '宜宾市', '南充市', '内江市', '三门峡市', '商丘市', '铜仁市', '淮北市', '南平市', '营口市', '新余市', '吉安市', '洛阳市', '临沧市', '拉萨市', '宜昌市', '雅安市', '蚌埠市', '马鞍山市', '开封市', '平顶山市', '儋州市', '六盘水市', '晋城市', '宁波市', '驻马店市', '孝感市', '舟山市', '新乡市', '周口市', '张家口市', '襄阳市', '大庆市', '池州市', '湛江市', '成都市', '昭通市', '乌鲁木齐市', '克拉玛依市', '芜湖市', '河源市', '钦州市', '昌都市', '榆林市', '白银市', '武威市', '吐鲁番市', '大连市', '深圳市', '吴忠市', '丽江市', '张掖市', '平凉市', '定西市', '赤峰市', '巴彦淖尔市', '哈尔滨市', '巴中市', '山南市', '宝鸡市', '固原市', '中卫市', '太原市', '银川市', '福州市', '滁州市', '长沙市', '常德市', '眉山市', '南京市', '海东市', '衡水市', '漯河市', '嘉峪关市', '酒泉市', '朔州市', '许昌市', '阳江市', '泸州市', '石嘴山市', '鞍山市', '三亚市', '哈密市', '沈阳市', '辽源市', '随州市', '伊春市', '潍坊市', '韶关市', '连云港市', '湖州市', '绍兴市', '金华市', '衢州市', '梧州市', '玉林市', '长治市', '盘锦市', '吉林市', '双鸭山市', '防城港市', '珠海市', '清远市', '东莞市', '呼伦贝尔市', '泉州市', '九江市', '鹰潭市', '盐城市', '宿迁市', '宁德市', '烟台市', '铜川市', '徐州市', '济宁市', '贵阳市', '杭州市', '温州市', '东营市', '泰安市', '惠州市', '云浮市', '绵阳市', '遂宁市', '鸡西市', '嘉兴市', '丽水市', '宣城市', '攀枝花市', '广安市', '锦州市', '荆州市', '广州市', '本溪市', '葫芦岛市', '黄石市', '鹤壁市', '梅州市', '抚顺市', '枣庄市', '鄂州市', '滨州市', '茂名市', '青岛市', '泰州市', '肇庆市', '中山市', '白山市', '佳木斯市', '淮安市', '台州市', '铜陵市', '莆田市', '德州市', '岳阳市', '娄底市', '海口市', '德阳市', '商洛市', '金昌市', '邢台市', '运城市', '通辽市', '丹东市', '阜新市', '无锡市', '常州市', '南通市', '扬州市', '咸宁市', '秦皇岛市', '日照市', '厦门市', '聊城市', '永州市', '三明市', '漳州市', '渭南市', '晋中市', '铁岭市', '长春市', '松原市', '汕头市', '潮州市', '阜阳市', '郑州市', '菏泽市', '资阳市', '安顺市', '通化市', '淄博市', '遵义市', '呼和浩特市', '西安市', '苏州市', '黑河市', '汕尾市', '自贡市', '临汾市', '唐山市', '镇江市', '龙岩市', '衡阳市', '武汉市', '阳泉市', '忻州市', '南昌市', '济南市', '威海市', '临沂市', '揭阳市', '保定市', '四平市', '合肥市', '七台河市', '牡丹江市', '玉溪市', '宜春市', '汉中市', '乌兰察布市', '荆门市']
data = pd.read_csv('Data/所有信息汇总-V1.csv')
data = data[data.ctnm.isin(ct_list)]

cs = pd.read_excel('Data/市领导数据/戴敏-new/市委书记.xlsx')
cs = cs[(cs.year == 2018) & cs.ctnm.isin(ct_list)]
cs['name-month'] = cs
cs.drop(['leavereasons', 'age', 'tennu', 'change'], axis=1, inplace=True)
# %%
cs_name = '颜赣辉'
save_dict = {}
# %% do scraping
for cs_name in tqdm(data.name):
	url = 'https://zh.wikipedia.org/wiki/' + cs_name
	response = requests.get(url)

	if response.status_code == 200:
		soup = BeautifulSoup(response.content)
		soup.select('p')
		save_dict[cs_name] = response.content
		try:
			new_dict = {
				'year': 2020,
				'citycode': int(cs.loc[cs.ctnm == ct_name, 'citycode']),
				'ctnm': ct_name,
				'provincecode': int(cs.loc[cs.ctnm == ct_name, 'provincecode']),
				'provincename': cs.loc[cs.ctnm == ct_name, 'provincename'].values[0],
				'name': soup.select('tr:nth-child(2) th+ td > a')[0].text,
				'race': soup.select('caption+ tbody tr:nth-child(3) th+ td')[0].text,
				'age': soup.select('caption+ tbody tr:nth-child(5) th+ td')[0].text,
				'inaug_time': soup.select('caption+ tbody tr:nth-child(6) th+ td')[0].text,
				'note': ''
			}
		except IndexError:
			error_list.append(ct_name)
			print(ct_name, 'IndexError')
			continue
		else:
			cs_20_full = cs_20_full.append(new_dict, ignore_index=True)
			left_ct.remove(ct_name)
	else:
		error_list.append(ct_name)





