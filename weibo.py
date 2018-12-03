#-*-coding:utf8-*-

import re
import os
from bs4 import BeautifulSoup
import requests
import shutil
import time
from lxml import etree
import config as conf

user_id = conf.config["userId"]
cookie = conf.config["cookie"]
base_url = "https://weibo.cn/%d/profile?filter=1&page=%d"

# 文本内容
result = ""
# 地址
address = ""
# 图片地址
urllist_set = set()
# 爬取完当前页，休眠时间
sleep_time = 40

try:
	data_path = os.getcwd() + "/result/%d/"%user_id
	if not os.path.exists(data_path):
		os.makedirs(data_path)
		os.makedirs(data_path+"/imgs/")
		print("目录创建成功")
except Exception as e:
	print("目录创建失败，原因：", e)

# 获取总页码
def get_pages():
	print("准备爬取 %d 用户"%user_id)
	url = base_url%(user_id, 1)
	html = requests.get(url, cookies = cookie).content
	body = etree.HTML(html)
	return (int)(body.xpath('//input[@name="mp"]')[0].attrib['value'])

# 获取每页的数据
def get_page(page=1):
	# 在 python ，如果在 def 中直接修改全局变量的值，会变成局部变量
	# 这里如果不使用 global 重新声明 result ，会报如下错误
	# local variable 'result' referenced before assignment
	global result
	global address
	try:
		url = base_url%(user_id, page)
		lxml = requests.get(url, cookies = cookie).content
		# 解析爬取到的html内
		body = etree.HTML(lxml)
		content = body.xpath("//span[@class='ctt']")
		for each in content:
			# 解析地址
			strs = etree.tostring(each)
			soup = BeautifulSoup(strs, "lxml")
			addrs = soup.find('a', href=re.compile(r"^https://weibo.cn/sinaurl", re.I))
			text = ""
			if addrs:
				if addrs.string.find("·") > -1:
					address = address + addrs.string + "\n"
					text = re.sub(r"%s"%addrs.string, "", each.xpath("string(.)"), 0)
				else:
					text = each.xpath("string(.)")
				result = result + text + "\n"
			else:
				text = each.xpath("string(.)")
				result = result + text + "\n"
		print("第 %d 页读取成功"%page)
		analysis_img(lxml)
		print("图片读取完成，休息 %d 秒"%sleep_time)
		time.sleep(sleep_time)
	except Exception as e:
		print("第%d页读取失败，原因是："%page, e)

# 解析图片
def analysis_img(lxml):
	soup = BeautifulSoup(lxml, "lxml")
	urllist = soup.find_all('a',href=re.compile(r"^https://weibo.cn/mblog/oripic",re.I))
	urllist1 = soup.find_all('a',href=re.compile(r'^https://weibo.cn/mblog/picAll',re.I))
	for img_url in urllist:
		img_url["href"] = re.sub(r"amap", "", img_url["href"])
		urllist_set.add(requests.get(img_url["href"], cookies=cookie).url)
	for img_all in urllist1:
		html_content = requests.get(img_all["href"], cookies=cookie).content
		soups = BeautifulSoup(html_content, "lxml")
		urllist2 = soups.find_all('a',href=re.compile(r'^/mblog/oripic',re.I))
		for imgurl in urllist2:
			imgurl['href'] = 'https://weibo.cn' + re.sub(r"amp;", '', imgurl['href'])
			urllist_set.add(requests.get(imgurl["href"], cookies = cookie).url)

# 保存爬取到的内容
def save_result():
	try:
		fi = open(data_path+"%d"%user_id, "wb")
		fi.write(bytes(result, encoding = "utf8"))
		f2 = open(data_path+"%d_address"%user_id, "wb")
		f2.write(bytes(address, encoding = "utf8"))
		print("数据写入成功，路径是：", data_path)
	except Exception as e:
		print("存储数据失败，原因：", e)

# 下载图片
def download_img():
	# 写入图片地址
	link = ""
	fi = open(data_path+"%d_image"%user_id, "wb")
	for eachlink in urllist_set:
		link = link + eachlink + "\n"
	fi.write(bytes(link, encoding = "utf8"))
	# 下载图片
	x = 1
	for imgurl in urllist_set:
		temp = data_path+"/imgs/%s.jpg"%x
		print("正在下载第 %s 张图片"%x)
		try:
			r = requests.get(imgurl, stream=True)
			if r.status_code == 200:
				with open(temp, 'wb') as f:
					r.raw.decode_content = True
					shutil.copyfileobj(r.raw, f)
		except Exception as e:
			print("第 %s 张图片下载失败，原因："%x, e)
		x = x + 1

if __name__ == '__main__':
	pages = get_pages()
	print("数据读取成功，共计 %d 页"%pages)
	for page in range(1, pages+1):
		get_page(page)
	save_result()
	download_img()
