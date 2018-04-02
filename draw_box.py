#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
绘制函数直线图。
"""

from common import logcm
from common import plotcm

import numpy as np
import matplotlib.pyplot as plt

# 随机生成一个标准正态分布形状是600*2的数组
data = np.random.standard_normal((600, 2))
logcm.print_obj(data, 'data')

# 图绘制
fig = plt.figure()
# 设置图片尺寸
fig.set_size_inches(10, 16)
# 总标题
fig.suptitle(u'散点图、直方图、箱形图')
# 设置标题(中文字体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

for i in range(4):
    for j in range(2):
        index = i * 2 + j
        ax = fig.add_subplot(4, 2, index + 1)

        # 添加网格
        ax.grid(True)
        # 轴标签和图标题
        ax.set_xlabel('')
        ax.set_ylabel('')

        # 散点图
        if index == 0:
            # 用plot绘制散点图，且为红色圆标记
            ax.plot(data[:, 0], data[:, 1], 'ro')
            ax.set_title('plot散点图')
        elif index == 1:
            # 用scatter绘制散点图
            ax.scatter(data[:, 0], data[:, 1], marker='o')
            ax.set_title('scatter散点图')
        elif index == 2:
            # 用scatter绘制散点图
            ax.scatter(data[:, 0], data[:, 1], marker='o', c='r')
            ax.set_title('scatter散点图-指定色')
        elif index == 3:
            # 随机颜色
            c = np.random.randint(0, 10, len(data))
            ax.scatter(data[:, 0], data[:, 1], c=c, marker='o')
            ax.set_title('scatter散点图-随机色')
        elif index == 4:
            # 直方图
            ax.hist(data, bins=30, label=['1st', '2nd'])
            ax.legend(loc=0)
            ax.set_title('hist直方图')
        elif index == 5:
            # 堆叠的直方图
            ax.hist(data, bins=20, label=['1st', '2nd'], color=['b', 'm'], stacked=True, rwidth=0.8)
            ax.legend(loc=0)
            ax.set_title('hist堆叠直方图')
        elif index == 6:
            # 箱形图
            ax.boxplot(data)
            # X轴：旋转50度
            ax.set_xticks([1, 2], ['1st', '2nd'])
            ax.set_title('箱形图')
        elif index == 7:
            line = ax.plot(data, 'r')
            plt.setp(line, linestyle='--')
            ax.set_title('折线图')

# 保存图片
plt.savefig('images/draw_box_result.jpg')
# 显示绘制后的图片
plt.show()
