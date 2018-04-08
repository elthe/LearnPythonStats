#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
读取URL内容，生成词云
"""

import jieba.analyse
import matplotlib.pyplot as plt

from common import htmlcm
from common import logcm
from common import webcm
from common import wordscm
from scipy.misc import imread
from wordcloud import WordCloud

# 加载内容URL的内容
url = 'http://www.leadbankmap.com/baogao/detail_4800.html'
encoding = 'utf-8'
html = webcm.read_url(url, encoding)
content = htmlcm.clean_html(html)

# 加载停用词列表
stopwords = wordscm.load_stopwords('./data', 'words_stop1.txt', encoding)

# 导入stopwords
jieba.analyse.set_stop_words('./data/words_stop1.txt')

# 文字频率排行
seg = jieba.analyse.textrank(content, topK=50, withWeight=False, allowPOS=('nt', 'n', 'nv'))
cut_text = " ".join(seg)
logcm.print_obj(cut_text, 'cut_text')

# 产生词云
color_mask = imread("./data/words_mask_china.png")  # 读取背景图片
cloud = WordCloud(
    # 设置字体，不指定就会出现乱码
    font_path="./data/words_font_simhei.ttf",
    # 设置背景色
    background_color='white',
    # 词云形状
    mask=color_mask,
    # 允许最大词汇
    max_words=50,
    # 最大号字体
    max_font_size=40
)
word_cloud = cloud.generate(cut_text)

# 保存图片
word_cloud.to_file("./images/words_cloud1_result.jpg")

# 显示词云图片
plt.imshow(word_cloud)
# 坐标轴不显示
plt.axis('off')
# 显示
plt.show()
