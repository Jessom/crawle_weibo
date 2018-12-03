# crawle_weibo
微博爬虫，爬取微博个人账号的原创微博内容 <br />
纯属娱乐项目

## 环境
windows10 + python3.6.3

## 使用
在项目根目录添加`config.py`文件
``` python
# -*- coding: utf-8 -*-
config = {
	"userId": "userId",			# 需要爬取的用户微博ID
	"cookie": {
		"Cookie": "cookie"		# cookie
	},
	"background": "resource/background/qb.png"	# 生成词云的图片，resource下有几张可选图片
}
```
- 执行`weibo.py`爬取`原创微博`，并下载图片
- 执行`analysis.py`解析微博内容，并生成图表
- 执行`main.py`生成词云图

爬取完成后，会在项目根目录生成`result`文件夹，以及对于的`user_id`文件夹 <br />
解析完成后，会在对应的`user_id`文件夹下生成：
- 分类 `category.txt`
- 使用最多的表情 `express.txt`
- 使用最多的名字 `name.txt`
- 使用最多的词语 `word.txt`
- 分类图表 `category.html`
- 表情图表 `express.html`
- 常去地点 `address.html`

<p align="center"><img src='http://qicloud.jswei.cn/images/git/crawle_weibo/name.jpg' /></p>
<p align="center"><img src='http://qicloud.jswei.cn/images/git/crawle_weibo/pikaqiu.jpg' /></p>
<p align="center"><img src='http://qicloud.jswei.cn/images/git/crawle_weibo/qiaoba.jpg' /></p>

## wordcloud的安装
- 到[http://www.lfd.uci.edu/~gohlke/pythonlibs/#wordcloud](http://www.lfd.uci.edu/~gohlke/pythonlibs/#wordcloud)下载wordcloud模块所需要的whl文件，根据自己版本下载
- `cd`到下载的路径下
- 执行`pip install wordcloud-1.5.0-cp36-cp36m-win32.whl`（这是我下载的版本，根据自己电脑，下载相应的版本即可）

## 解决wordcloud中文乱码
中文乱码，是因为使用的`字体`不支持中文，只要使用支持中文的字体即可
``` python
wordcloud = WordCloud(font_path="simhei.ttf").generate(text)
```
这里的`font_path`就是指定使用的字体文件，`simhei.ttf`是黑体，将字体文件复制到项目下即可，不需要重命名，会自动变成英文名的

## 参考地址
- [https://github.com/dingmyu/weibo_analysis.git](https://github.com/dingmyu/weibo_analysis.git)
- [https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/)
- [https://www.cnblogs.com/tina-python/p/5508402.html](https://www.cnblogs.com/tina-python/p/5508402.html) <br />
还有很多，这里就不一一列举出来了
