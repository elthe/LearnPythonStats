#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
正态分布是一种连续分布，其函数可以在实线上的任何地方取值。
正态分布由两个参数描述：
  1) 分布的平均值μ (mu)
  2) 方差σ2 (sigma)。
"""

import matplotlib.pyplot as plt
import numpy as np

from common import logcm
from scipy import stats

# 参数组设置（多组参数）
mu = [3, 5, 7, 5, 5, 5]
sigma = [2, 2, 2, 2, 4, 6]
dashes = ['--', '-', '--', '-', '--', '--']
colors = ['g', 'b', 'r', 'g', 'b', 'r']
titles = ['方差不变修改平均值', '平均值不变修改方差']

# 多子图绘制
fig, axes = plt.subplots(2, 1, sharey=True, sharex=True)
# 设置图片尺寸
fig.set_size_inches(10, 6)
# 总标题
fig.suptitle(u'正态分布（Normal Distribution）参数调整示例图')
# 设置标题(中文字体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

plt.ylim(0.0, 0.22)
plt.xlim(-10, 20)

# X轴坐标设置
x = np.arange(-10, 20, 0.1)
logcm.print_obj(x, 'x')

for i in range(2):
    ax = axes[i]
    # 设置子画面的标题
    ax.set_title(titles[i])

    for j in range(3):
        # 索引
        index = i * 3 + j
        # 取得参数值
        m = mu[index]
        s = sigma[index]
        d = dashes[index]
        c = colors[index]
        # 根据参数计算正态分布分布Y坐标
        y = stats.norm.pdf(x, m, s)
        logcm.print_obj(y, 'y(m=%d, s=%d)' % (m, s))

        # 根据坐标画图
        line, = ax.plot(x, y, d, color=c)
        # 绘制顶点虚线
        maxY = max(y)
        y2 = np.arange(0, maxY, 0.001)
        x2 = np.repeat(m, len(y2))
        ax.plot(x2, y2, ':', color=c)

        # 设置每条线的备注
        if i == 0:
            l = '$\mu=%d$' % m
            l2 = '$\sigma^2=%d$' % s
        else:
            l = '$\sigma^2=%d$' % s
            l2 = '$\mu=%d$' % m
        # 绘制备注
        ax.text(m, maxY, l, fontsize=12, verticalalignment="bottom", horizontalalignment="center")
        if j == 0:
            ax.text(-7.5, 0.15, l2, fontsize=16, verticalalignment="bottom", horizontalalignment="center")

# 保存图片
plt.savefig('images/normal_distribution3_result.jpg')
# 显示绘制后的图片
plt.show()
