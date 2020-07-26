"""
first from 1.18 - 1.31, produce a dataframe of  columns
'prov', 'date', 'type', 'title', '事例?', '头版?', 'note', 'link'
内蒙古日报
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup

base_url = 'http://szb.northnews.cn/nmgrb/html/2020-01/'
# sample_url = 'http://szb.northnews.cn/nmgrb/html/2020-01/27/node_20333.htm'
# page = requests.get(URL)
# soup = BeautifulSoup(page.content, 'html.parser')
# soup = BeautifulSoup(page.content)

# def get_page(date, node_n):
# 	url_ = base_url + str(date) + '/' + 'node_' + str(n) + '.htm'
# 	page = requests.get(url_)

news = pd.DataFrame(columns=['prov', 'date', 'type', 'title', '事例?', '头版?', 'note', 'link'])

def get_page(date, n):
	url = base_url + str(date) + '/' + 'node_' + str(n) + '.htm'
	return requests.get(url)

date = 18
n = 20200-1
error_list = [20216]
while n <= 20352:
	n += 1
	page = get_page(date, n)
	if page.status_code == 404:
		date += 1
		page = get_page(date, n)
		if (page.status_code == 404) and n not in error_list:
			print('ERROR1:', date, n)
			date -= 1
			continue
		elif page.status_code == 404:
			if n == 20216:
				n = 20232
			else:
				print('ERROR2:', date, n)
			page = get_page(date, n)
			print('date is now:', date)

	soup = BeautifulSoup(page.content)
	articles = soup.select('#main-ed-articlenav-list a')

	is_first_page = requests.get(url=base_url + str(date) + '/' + 'node_1' + '.htm').text == page.text
	# create pandas rows
	for i in range(len(articles)):
		new_row = {'prov': '内蒙古', 'date': '2020-01-' + str(date),
		           'type': '', 'title': articles[i].text, '事例?': '',
		           '头版?': is_first_page, 'note': '',
		           'link': base_url + str(date) + '/' + articles[i]['href']}
		news = news.append(new_row, ignore_index=True)

# results = soup.find_all('#main-ed-articlenav-list a')
#
# soup.select('#main-ed-articlenav-list a')
#
# # main-ed-articlenav-list a
