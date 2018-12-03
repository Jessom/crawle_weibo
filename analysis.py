# -*- coding: utf-8 -*-
import re
import jieba
import jieba.analyse
from collections import Counter
import sys
import time
import jieba.posseg as pseg
import keywords_new
from pyecharts import Pie, Bar, Geo
import config as conf

user_id = conf.config["userId"]

f = open("result/%d/%d"%(user_id, user_id), "rb")
f1 = open("result/%d/category.txt"%user_id, "wb")
f2 = open("result/%d/express.txt"%user_id, "wb")
f3 = open("result/%d/word.txt"%user_id, "wb")
f4 = open("result/%d/name.txt"%user_id, "wb")
list1 = []
record = {}
express = {}
name_set = {}
city = {}

while True:
  line = f.readline().strip().decode('utf-8')
  if line:
    # item = line.split(' ', 1)[1]
    item = line
    ex_all = re.findall(u"\\[.*?\\]", item)  
    if ex_all:
      for ex_item in ex_all:
        express[ex_item] = express.get(ex_item, 0) + 1
    for kw, keywords in keywords_new.keyword_dict.items():
      flag = 0
      for key, keyword in keywords.items():
        if flag == 1:
          break
        for word in keyword:
          match_flag = 1
          for small_word in word:
            match = re.search(re.compile(small_word, re.I), item)
            if not match:
              match_flag = 0
              break
          if match_flag == 1:
            record[kw] = record.get(kw, 0) + 1
            flag = 1
            break
    item = re.sub(u"\\[.*?\\]", '', item)
    list = jieba.cut(item, cut_all = False)
    for ll in list:
      list1.append(ll)
    seg_list = pseg.cut(item)
    for word, flag in seg_list:
      if flag == 'nr':
        name_set[word] = name_set.get(word, 0) + 1
  else:
    break

# 解析地址
f5 = open("result/%d/%d_address"%(user_id, user_id), "rb")
while True:
    line = f5.readline().strip().decode('utf-8')
    item = line.replace(" ", "")
    if line:
        ii = item[0:item.find("·")]
        city[ii] = city.get(ii, 0) + 1
    else:
        break

data = []

for item in city:
    i = (item, city[item])
    data.append(i)

count = Counter(list1)
words = ""
wordAttr = []
wordVal = []
for item in sorted(dict(count).items(), key=lambda d:d[1], reverse = True):
  if len(item[0]) >= 2 and item[1] >= 3:
    words = words + item[0] + " " + str(item[1]) + "\n"
    wordAttr.append(item[0])
    wordVal.append(item[1])
f3.write(bytes(words, encoding = "utf8"))
# 生成 单词 图表
# wordChart = Pie("单词", title_pos='center')
# wordChart.add("", wordAttr, wordVal, is_label_show=True, type='scroll', legend_orient="vertical", legend_pos="left")
# wordChart.render('result/%d/word.html'%user_id)

records = ""
recAttr = []
recVal = []
for key, keywords in sorted(record.items(), key=lambda d:d[1], reverse = True):
  records = records + key + " " + str(record[key]) + "\n"
  recAttr.append(key)
  recVal.append(record[key])
f1.write(bytes(records, encoding = "utf8"))
# 生成 类型 图表
recChart = Pie("类型", title_pos='center')
recChart.add("", recAttr, recVal, is_label_show=True, legend_orient="vertical", legend_pos="left")
recChart.render('result/%d/category.html'%user_id)

expressed = ""
expAttr = []
expVal = []
for key, keywords in sorted(express.items(), key=lambda d:d[1], reverse = True):
  expressed = expressed + key + " " + str(express[key]) + "\n"
  expAttr.append(key)
  expVal.append(express[key])
f2.write(bytes(expressed, encoding = "utf8"))
# 生成 表情 图表
expChart = Bar("表情", width=1200, title_pos='center')
expChart.add("", expAttr, expVal, is_stack=True, is_label_show=True, is_datazoom_show=True)
expChart.render('result/%d/express.html'%user_id)

names = ""
nameAttr = []
nameVal = []
for key, keywords in sorted(name_set.items(), key=lambda d:d[1], reverse = True):
  names = names + key + " " + str(name_set[key]) + "\n"
  nameAttr.append(key)
  nameVal.append(name_set[key])
f4.write(bytes(names, encoding = "utf8"))
# 生成 姓名 图表
# nameChart = Pie("姓名", title_pos='center')
# nameChart.add("", nameAttr, nameVal, is_label_show=True, legend_orient="vertical", legend_pos="left")
# nameChart.render('result/%d/name.html'%user_id)

# 生成地图图表
geo = Geo("您经常去的地方", "", title_color="#fff",
          title_pos="center", width=1000,
          height=600, background_color='#404a59')
attr, value = geo.cast(data)
geo.add("", attr, value, visual_range=[0, 200], maptype='china',visual_text_color="#fff",
        symbol_size=10, is_visualmap=True)
geo.render("result/%d/address.html.html"%user_id)

