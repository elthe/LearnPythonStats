#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
绘制函数直线图。
"""

from common import logcm
from common import plotcm

import numpy as np
import matplotlib.pyplot as plt

# X轴范围
x = np.arange(0.01, 10, 0.01)

# 配置一览
cfg_list = [
    [
        {
            'func': lambda x: x / 2,
            'label': r'$f(x)=\frac{1}{2}x$',
            'color': 'orange',
            'line': '--',
            'x_lbl': 8,
            'points': [3]
        },
        {
            'func': lambda x: x,
            'label': r'$f(x)=x$',
            'color': 'black',
            'line': '--',
            'x_lbl': 7,
            'points': [3]
        },
        {
            'func': lambda x: 2 * x,
            'label': r'$f(x)=2x$',
            'color': 'r',
            'line': '--',
            'x_lbl': 4,
            'points': [3]
        },
        {
            'func': lambda x: 3 * x,
            'label': r'$f(x)=3x$',
            'color': 'b',
            'line': '--',
            'x_lbl': 3.3,
            'points': [3]
        }
    ],
    [
        {
            'func': lambda x: x * x,
            'label': r'$f(x)=x^2$',
            'color': 'r',
            'line': '--',
            'x_lbl': 2.6,
            'points': [2]
        },
        {
            'func': lambda x: x,
            'label': r'$f(x)=x$',
            'color': 'black',
            'line': '--',
            'x_lbl': 7,
            'points': [2]
        },
        {
            'func': lambda x: x ** 0.5,
            'label': r'f(x)=$\sqrt{x}$',
            'color': 'orange',
            'line': '--',
            'x_lbl': 7,
            'points': [2]
        },
        {
            'func': lambda x: x * x * x,
            'label': r'$f(x)=x^3$',
            'color': 'blue',
            'line': '--',
            'x_lbl': 2.15,
            'points': [2]
        }
    ],
    [
        {
            'func': lambda x: 1 / x,
            'label': r'$f(x)=\frac{1}{x}$',
            'color': 'b',
            'line': '--',
            'x_lbl': 0.125,
            'points': [0.2]
        },
        {
            'func': lambda x: x,
            'label': r'$f(x)=x$',
            'color': 'black',
            'line': '--',
            'x_lbl': 7,
            'points': [5]
        },
        {
            'func': lambda x: np.log(x),
            'label': r'$f(x)=\lnx$',
            'color': 'r',
            'line': '--',
            'x_lbl': 7,
            'points': [5]
        },
        {
            'func': lambda x: np.log10(x),
            'label': r'$f(x)=\log_{10}x$',
            'color': 'orange',
            'line': '--',
            'x_lbl': 7,
            'points': [5]
        }
    ],
    [
        {
            'func': lambda x: np.exp(x),
            'label': r'$f(x)=e^x$',
            'color': 'b',
            'line': '--',
            'x_lbl': 2,
            'points': [1]
        },
        {
            'func': lambda x: x,
            'label': r'$f(x)=x$',
            'color': 'black',
            'line': '--',
            'x_lbl': 7,
            'points': [1]
        },
        {
            'func': lambda x: 10 ** x,
            'label': r'$f(x)=10^x$',
            'color': 'r',
            'line': '--',
            'x_lbl': 0.95,
            'points': [1]
        }
    ]
]

# 多子图绘制
fig, axes = plt.subplots(2, 2, figsize=(10, 10), sharex=False, sharey=False)  # 设置图片尺寸

for i in range(len(cfg_list)):
    # 取得坐标轴
    ax = axes[i // 2][i % 2]
    # 显示网格
    ax.grid(True)
    # 坐标值范围
    ax.set_xticks(range(0, 11))
    ax.set_yticks(range(0, 11))
    # 设置X，Y轴坐标范围
    ax.set_ylim(0, 10)
    ax.set_xlim(0, 10)

    for j in range(len(cfg_list[i])):
        # 取得配置
        cfg = cfg_list[i][j]
        # 画线
        plotcm.draw_func_line(ax, x, cfg['func'], cfg['label'], cfg['x_lbl'], cfg['color'], cfg['line'])
        # 绘制坐标点
        if 'points' in cfg:
            # 计算坐标点
            xps = np.array(cfg['points'])
            yps = cfg['func'](xps)
            # 画点
            plotcm.draw_point_list(ax, xps, yps, show_label=True, show_line=False, color=cfg['color'])

# 调整每隔子图之间的距离
plt.tight_layout()

# 保存图片
plt.savefig('images/draw_line2_result.jpg')
# 显示绘制后的图片
plt.show()
