#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
绘制函数直线图。
"""

from common import logcm
from common import plotcm

import numpy as np
import matplotlib.pyplot as plt

# 多子图绘制
fig, ax = plt.subplots(figsize=(8, 8))
# 设置图片尺寸
fig.set_size_inches(8, 8)

# X轴范围
x = np.arange(0.01, 10, 0.01)

# 取得参数值
y1 = x / 2
y2 = x
y3 = 2 * x
y4 = 3 * x
y5 = x * x
y6 = x * x * x
y7 = 1 / x
y8 = x ** 0.5
y9 = np.log(x)

# 根据坐标画图
ax.plot(x, y1, '--', color='gray', label=r'$\frac{1}{2}x$')
ax.plot(x, y2, '-', color='black', label='x')
ax.plot(x, y3, '--', color='gray', label='2x')
ax.plot(x, y4, '--', color='gray', label='3x')
ax.plot(x, y5, '-.', color='b', label=r'$x^2$')
ax.plot(x, y6, '-.', color='purple', label=r'$x^3$')
ax.plot(x, y7, ':', color='r', label=r'$\frac{1}{x}$')
ax.plot(x, y8, '-.', color='b', label=r'$\sqrt{x}$')
ax.plot(x, y9, ':', color='g', label=r'$\lnx$')

ax.text(7, 3.5, r'$y=\frac{1}{2}x$', color='gray', verticalalignment="top", horizontalalignment="left")
ax.text(5, 5, r'$y=x$', color='black', verticalalignment="top", horizontalalignment="left")
ax.text(3, 6, r'$y=2x$', color='gray', verticalalignment="top", horizontalalignment="left")
ax.text(2.2, 6.6, r'$y=3x$', color='gray', verticalalignment="top", horizontalalignment="left")
ax.text(2.2, 9.3, r'$y=x^3$', color='purple', verticalalignment="top", horizontalalignment="left")
ax.text(3, 8.8, r'$y=x^2$', color='b', verticalalignment="top", horizontalalignment="left")
ax.text(9, 3.2, r'$y=\sqrt{x}$', color='b', verticalalignment="bottom", horizontalalignment="left")
ax.text(8.5, 0.125, r'$y=\frac{1}{x}$', color='r', verticalalignment="bottom", horizontalalignment="left")
ax.text(8.5, 2.2, r'$y=lnx$', color='g', verticalalignment="bottom", horizontalalignment="left")

# 设置X，Y轴坐标范围
plt.ylim(0, 10)
plt.xlim(0, 10)

# 设置XY轴标题
plt.xlabel('x')
plt.ylabel('y')

# 坐标
plt.xticks(range(0, 11))
plt.yticks(range(0, 11))

# 设置图例备注显示位置
ax.legend(loc='best')

# 保存图片
plt.savefig('images/draw_line_result.jpg')
# 显示绘制后的图片
plt.show()
