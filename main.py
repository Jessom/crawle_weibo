#-*-coding:utf8-*-

from os import path
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import jieba

d = path.dirname(__file__)
user_id = 5337887050
background = "resource/background/nm.png"

# 读取文本内容，并分词
comment_text = open(path.join(d, "result\\%d\\%d")%(user_id, user_id), "rb").read().decode('utf-8')
text = " ".join(jieba.cut(comment_text))

# 读取蒙版
color_mask = np.array(Image.open(path.join(d, background)))
stopwords = set(STOPWORDS)
stopwords.add("said")

wordcloud = WordCloud(
	font_path="resource/simhei.ttf",
	max_words=2000,
	max_font_size=40,
	background_color='white',
	mask=color_mask,
	stopwords=stopwords,
	random_state=42
).generate(text)

# 着色
image_colors = ImageColorGenerator(color_mask)

# wordcloud.to_file("pjl_cloud4.jpg")
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis('off')
# plt.figure()

# 重新着色
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
wordcloud.to_file(path.join(d, "result\\%d\\%d.jpg"%(user_id, user_id)))
plt.axis('off')
plt.figure()
# plt.imshow(color_mask, cmap=plt.cm.gray, interpolation="bilinear")
# plt.axis("off")
plt.show()
