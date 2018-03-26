#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
随机生成数字，然后统计分布规律。
"""

import random

import matplotlib.pyplot as plt
import numpy as np

from common import logcm

# 随机数的数量
randomNum = 10000
randomIntFrom = 1
randomIntTo = 100
# 随机方法
randomMethods = ['random.randint', 'np.random.randint', 'np.random.normal', 'np.random.uniform']

# 多子图绘制
fig, axes = plt.subplots(2, 4, sharey=False, sharex=True)
# 设置图片尺寸
fig.set_size_inches(12, 8)
# 总标题
fig.suptitle(u'不同方法获取%d个随机整数（%d - %d）分布统计图' % (randomNum, randomIntFrom, randomIntTo))
# 设置标题(中文字体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# X轴坐标设置
x = np.arange(randomIntFrom + 1, randomIntTo, 1)
logcm.print_obj(x, 'x')

for i in range(2):
    for j in range(4):
        # 索引
        index = j
        # 随机数的数组
        listRandom = []
        ax = axes[i, j]
        if randomMethods[index] == 'random.randint':
            lp = 0
            while lp <= randomNum:
                listRandom.append(random.randint(randomIntFrom, randomIntTo))
                lp += 1

        if randomMethods[index] == 'np.random.randint':
            listRandom = np.random.randint(randomIntFrom, randomIntTo, randomNum).tolist()

        if randomMethods[index] == 'np.random.normal':
            # 使用平均数和指定方差值生成正态分布的随机数，取整后返回
            listRandom = np.around(np.random.normal((randomIntTo - randomIntFrom) / 2, 16, randomNum)).tolist()

        if randomMethods[index] == 'np.random.uniform':
            listRandom = np.around(np.random.uniform(randomIntFrom, randomIntTo, randomNum)).tolist()

        if len(listRandom) == 0:
            continue;

        logcm.print_obj(listRandom, 'listRandom(%s)' % randomMethods[index])
        if i == 0:
            # Y轴：随机数分布数组
            y = []
            for no in x:
                y.append(listRandom.count(no))
            ax.plot(x, y)
        else:
            ax.hist(listRandom, 10,
                    alpha=.5)

        # 方法名显示
        ax.set_title(randomMethods[index])

# 保存图片
plt.savefig('images/normal_random_result.jpg')
# 显示绘制后的图片
plt.show()
