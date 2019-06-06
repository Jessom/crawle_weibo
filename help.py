#-*-coding:utf8-*-

import re
import os
from bs4 import BeautifulSoup
import requests
import shutil
import time
from lxml import etree
import config as conf
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import collections

user_id = conf.config["userId"]
cookie = conf.config["cookie"]
help_url = "https://weibo.cn/msg/attitude?rl=1&page=%d"

# 休息时间
sleep_time = 10

# 获取点赞页码
def get_help_pages():
	print("准备爬取 %d 用户被赞信息"%user_id)
	url = help_url%(1)
	html = requests.get(url, cookies = cookie).content
	body = etree.HTML(html)
	return (int)(body.xpath('//input[@name="mp"]')[0].attrib['value'])

# 获取点赞页面具体内容
def get_help_page(pages, p=1):
  try:
    result = ""
    url = help_url%p
    lxml = requests.get(url, cookies = cookie).content
    body = etree.HTML(lxml)
    content = body.xpath("//div[@class='c']")
    for each in content:
      strs = etree.tostring(each)
      soup = BeautifulSoup(strs, "lxml")
      addrs = soup.find('a', href=re.compile(r"^\/u\/\d{5,16}", re.I))
      if addrs:
        result += addrs.string + '\n'
    print('第 %d 页爬取完成'%p)
    if pages != p:
      print("休息 %d 秒"%sleep_time)
      time.sleep(sleep_time)
    return result
  except Exception as e:
    print("第%d页读取失败，原因是："%p, e)

# 写入数据
def save_help(content):
  try:
    fi = open("./result/%d_help"%user_id, "wb")
    fi.write(bytes(content, encoding = "utf8"))
    print("数据写入成功，路径是:", "./result/my_help")
  except Exception as e:
    print("写入数据失败，原因是：", e)

# 生成词云图
def word_img(content):
  d = os.path.dirname(__file__)
  background = conf.config["background"]
  color_mask = np.array(Image.open(os.path.join(d, background)))
  stopwords = set(STOPWORDS)
  stopwords.add("said")

  wordcloud = WordCloud(
    font_path="resource/simhei.ttf",
    max_words=2000,
    max_font_size=40,
    background_color='white',
    mask=color_mask,
    stopwords=stopwords,
    repeat=True,
    random_state=42
  ).generate(content)

  image_colors = ImageColorGenerator(color_mask)
  # 重新着色
  plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
  wordcloud.to_file(os.path.join(d, "result/my_help.jpg"))
  plt.axis('off')
  plt.figure()
  plt.show()

if __name__ == '__main__':
  pages = get_help_pages()
  print("点赞页码读取成功，共计 %d 页"%pages)
  result = ""
  for page in range(1, pages+1):
    result += get_help_page(pages, page)

  cont = ""
  for item in collections.Counter(result.split('\n')).most_common():
    cont += item[0] + ' ' + str(item[1]) + "\n"
  save_help(cont)
  word_img(result)
