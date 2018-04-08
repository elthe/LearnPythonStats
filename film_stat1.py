#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
分析CPI指数和票房的关系。
"""

import matplotlib.pyplot as plt
import numpy as np

from common import convertcm
from common import datecm
from common import loadtscm
from common import logcm
from common import statcm

# 居民消费价格指数
df_cpi = loadtscm.get_cpi('2016.1', '2017.12')
logcm.print_obj(df_cpi, 'df_cpi')

# 要处理月份一览
month_list = datecm.date_convert(df_cpi['month'], '%Y.%m', '%Y-%m')
logcm.print_obj(month_list, 'month_list')

# 计算总票房
sum_list = []
max_list = []
min_list = []
mean_list = []
for month in month_list:
    # 查询当月票房
    df_month = loadtscm.month_boxoffice(month)
    box_list = convertcm.to_int(df_month['boxoffice'])
    # 加入列表
    sum_list.append(np.sum(box_list))
    max_list.append(np.max(box_list))
    min_list.append(np.min(box_list))
    mean_list.append(np.mean(box_list))

# 月票房列表
logcm.print_obj(sum_list, 'sum_list')

# 计算月份CPI和总票房的相关性。
s_cpi = df_cpi['cpi']

# 多子图绘制
fig, axes = plt.subplots(3, 2)
# 设置图片尺寸
fig.set_size_inches(10, 15)
# 总标题
fig.suptitle(u'CPI和票房的关系')
# 设置标题(中文字体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 散点图
statcm.scatter_corr(axes[0][0], s_cpi, sum_list, 'CPI vs 总票房', color='r')
statcm.scatter_corr(axes[0][1], s_cpi, max_list, 'CPI vs 最高票房', color='b')
statcm.scatter_corr(axes[1][0], s_cpi, min_list, 'CPI vs 最低票房', color='black')
statcm.scatter_corr(axes[1][1], s_cpi, mean_list, 'CPI vs 平均票房', color='orange')
statcm.scatter_corr(axes[2][0], min_list, max_list, '最低票房 vs 最高票房', color='r')
statcm.scatter_corr(axes[2][1], max_list, sum_list, '最高票房 vs 总票房', color='b')

# 保存图片
plt.savefig('images/film_stat1_result.jpg')
# 显示绘制后的图片
plt.show()
