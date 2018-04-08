#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
获取即时财经新闻，生成词云
"""

import jieba.analyse
import matplotlib.pyplot as plt
import tushare as ts

from common import logcm
from common import wordscm
from scipy.misc import imread
from wordcloud import WordCloud

# 获取即时财经新闻，类型包括国内财经、证券、外汇、期货、港股和美股等新闻信息。
# 数据更新较快，使用过程中可用定时任务来获取。
news = ts.get_latest_news(top=150, show_content=True)
news.dropna()
logcm.print_obj(news, 'news')

# 信息类型
classify_list = ['证券', '国内财经', '外汇', '期货', '港股', '美股']
encoding = 'utf-8'

# 加载停用词列表
stopwords = wordscm.load_stopwords('./data', 'words_stop1.txt', encoding)

# 导入stopwords
jieba.analyse.set_stop_words('./data/words_stop1.txt')

# 多子图绘制
fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharex=True, sharey=True)
fig.suptitle(u'')
# 设置标题(中文字体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

for i in range(2):
    for j in range(3):
        index = i * 2 + j
        # 当前分类
        classify_name = classify_list[index]
        # 根据分类筛选得到数据子集
        news_tmp = news[news.classify == classify_name]
        logcm.print_obj(news_tmp.shape, 'shape of ' + classify_name)

        # 设置标题
        axes[i][j].set_title('%s (%d 条)' % (classify_name, news_tmp.shape[0]))
        # 如果没有数据，则跳过
        if news_tmp.size == 0:
            continue

        # 加载内容URL的内容
        content = ""
        for cont in list(news_tmp.content):
            # 如果内容为None，则跳过
            if cont is not None:
                content += cont

        # 文字频率排行
        seg = jieba.analyse.textrank(content, topK=50, withWeight=False, allowPOS=('nt', 'n', 'nv'))
        cut_text = " ".join(seg)
        logcm.print_obj(cut_text, 'cut_text of ' + classify_name)

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
            max_font_size=50,
            # 图片尺寸
            width=500,
            height=400
        )
        word_cloud = cloud.generate(cut_text)
        # 显示词云图片
        axes[i][j].imshow(word_cloud)

# 不显示XY轴刻度
plt.xticks(())
plt.yticks(())

# 调整每隔子图之间的距离
plt.tight_layout()

# 保存图片
plt.savefig('images/words_cloud2_result.jpg')
# 显示
plt.show()
