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

# 配置一览
cfg_list = [
    {
        'func': lambda x: x / 2,
        'label': r'$f(x)=\frac{1}{2}x$',
        'color': 'gray',
        'line': '--',
        'x_lbl': 5
    },
    {
        'func': lambda x: x,
        'label': r'$f(x)=x$',
        'color': 'black',
        'line': '--',
        'x_lbl': 5
    },
    {
        'func': lambda x: 2 * x,
        'label': r'$f(x)=2x$',
        'color': 'gray',
        'line': '--',
        'x_lbl': 4
    },
    {
        'func': lambda x: 3*x,
        'label': r'$f(x)=3x$',
        'color': 'gray',
        'line': '--',
        'x_lbl': 3
    },
]

for cfg in cfg_list:
    plotcm.draw_func_line(ax, x, cfg['func'], cfg['label'], cfg['x_lbl'], cfg['color'], cfg['line'])

# 设置X，Y轴坐标范围
plt.ylim(0, 10)
plt.xlim(0, 10)

# 设置XY轴标题
plt.xlabel('x')
plt.ylabel('y=f(x)')

# 坐标
plt.xticks(range(0, 11))
plt.yticks(range(0, 11))

# 设置图例备注显示位置
ax.legend(loc='best')

# 保存图片
plt.savefig('images/draw_line2_result.jpg')
# 显示绘制后的图片
plt.show()
