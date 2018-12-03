# -*- coding: utf-8 -*-
from pyecharts import Geo
import config as conf

user_id = conf.config["userId"]
city = {}

f = open("result/%d/%d_address"%(user_id, user_id), "rb")
while True:
    line = f.readline().strip().decode('utf-8')
    item = line.replace(" ", "")
    if line:
        ii = item[0:item.find("·")]
        city[ii] = city.get(ii, 0) + 1
    else:
        break

data = []

for item in city:
    print(item)
    i = (item, city[item])
    data.append(i)


geo = Geo("全国主要城市空气质量", "data from pm2.5", title_color="#fff",
          title_pos="center", width=1000,
          height=600, background_color='#404a59')
attr, value = geo.cast(data)
geo.add("", attr, value, visual_range=[0, 200], maptype='china',visual_text_color="#fff",
        symbol_size=10, is_visualmap=True)
geo.render("全国主要城市空气质量.html")#生成html文件
# geo#直接在notebook中显示
