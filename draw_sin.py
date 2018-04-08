#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
绘制三角函数曲线图。
"""

import matplotlib.pyplot as plt
import numpy as np

from common import logcm
from common import plotcm

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
ax.plot(x, y1, '--', color='r', label='sin(x)')
ax.plot(x, y2, '--', color='b', label='cos(x)')
ax.plot(x, y3, '--', color='g', label='arcsin(x)')
ax.plot(x, y4, '--', color='black', label='arccos(x)')

# 绘制水平线
plotcm.draw_h_line(ax, -2 * np.pi, 2 * np.pi, 0.0, color='black', line_style='-')
plotcm.draw_h_line(ax, -2 * np.pi, 2 * np.pi, 1.0, color='gray', line_style=':')
plotcm.draw_h_line(ax, -2 * np.pi, 2 * np.pi, -1.0, color='gray', line_style=':')

# 绘制Y轴0线
plotcm.draw_v_line(ax, -2, 3, 0.0, color='black', line_style='-')
plotcm.draw_v_line(ax, -2, 3, 1.0, color='gray', line_style=':')
plotcm.draw_v_line(ax, -2, 3, -1.0, color='gray', line_style=':')

# 标记PI单位
vlist, tlist = plotcm.ticks_list_pi(-2, 2.5, 0.25)
vlist.append(-1)
vlist.append(1)
tlist.append('-1.0')
tlist.append('1.0')

# 设置XY轴标题
plt.xlabel('x')
plt.ylabel('y')

# X轴：旋转50度
plt.xticks(vlist, tlist, rotation=80)

# 设置图例备注显示位置
ax.legend(loc='best')

# 保存图片
plt.savefig('images/draw_sin_result.jpg')
# 显示绘制后的图片
plt.show()
