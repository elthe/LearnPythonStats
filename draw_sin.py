#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
绘制三角函数曲线图。
"""

from common import logcm
from common import plotcm

import numpy as np
import matplotlib.pyplot as plt
from pylab import *

# 多子图绘制
fig, ax = plt.subplots(figsize=(10, 6))
# 设置图片尺寸
fig.set_size_inches(10, 6)

# X轴范围
x = np.arange(-2 * np.pi, 2 * np.pi, 0.01)

# 取得参数值
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.arcsin(x)
y4 = np.arccos(x)

# 根据坐标画图
ax.plot(x, y1, color='r', label='sin(x)')
ax.plot(x, y2, color='b', label='cos(x)')
ax.plot(x, y3, color='g', label='arcsin(x)')
ax.plot(x, y4, color='black', label='arccos(x)')

# 绘制0轴线
y0 = np.repeat(0, len(y2))
ax.plot(x, y0, ':', color='gray')

# 标记PI单位
vlist, tlist = plotcm.ticks_list_pi(-2, 2.5, 0.5)
xticks(vlist, tlist)

# 设置图例备注显示位置
ax.legend(loc='best')

# 保存图片
plt.savefig('images/draw_sin_result.jpg')
# 显示绘制后的图片
plt.show()
