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
mu = [3, 7, 5, 5, 5]
sigma = [2, 2, 2, 4, 6]
dashes = [':', ':', '-', '--', '--']
colors = ['gray', 'b', 'black', 'b', 'r']

# 多子图绘制
fig, ax = plt.subplots()
# 设置图片尺寸
fig.set_size_inches(10, 6)

# 设置X，Y轴坐标范围
plt.ylim(0.0, 0.3)
plt.xlim(-10, 20)

# X轴坐标设置
x = np.arange(-10, 20, 0.1)
logcm.print_obj(x, 'x')

for index in range(len(mu)):
    # 取得参数值
    m = mu[index]
    s = sigma[index]
    d = dashes[index]
    c = colors[index]
    # 根据参数计算正态分布分布Y坐标
    y = stats.norm.pdf(x, m, s)
    logcm.print_obj(y, 'y(m=%d, s=%d)' % (m, s))

    # 设置每条线的备注
    l = '$\mu=%d, \sigma^2=%d$' % (m, s)
    # 根据坐标画图
    line, = ax.plot(x, y, d, color=c, label=l)

# 设置图例备注显示位置
ax.legend(loc='upper right')

# 设置标题(中文字体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.title(u'正态分布（Normal Distribution）')

# 显示文本公式
text = r"$f(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{\frac{(x-\mu)^2}{2\sigma^2}}$"
plt.text(-8, 0.28, text, fontsize=20, verticalalignment="top", horizontalalignment="left")

# 设置XY轴标题
plt.xlabel('x')
plt.ylabel('Probability density')

# 保存图片
plt.savefig('images/normal_distribution1_result.jpg')
# 显示绘制后的图片
plt.show()
