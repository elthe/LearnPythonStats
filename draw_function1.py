#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
函数绘图
"""

from common import logcm

import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import math

# 角度分割数
n_angles = 36
# 同心环层数
n_radii = 8
# 起始半径
min_radius = 0.25
# 半径数组
radii = np.linspace(min_radius, 0.95, n_radii)
# 角度数组（0～2PI）
angles = np.linspace(0, 2 * math.pi, n_angles, endpoint=False)
logcm.print_obj(angles, 'angles')
# 增加一个新维度，并复制N份
angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)
logcm.print_obj(angles, 'angles after repeat')
#
angles[:, 1::2] += math.pi / n_angles
logcm.print_obj(angles, 'angles new2')

# x = 半径 * COS(角度)
x = (radii * np.cos(angles)).flatten()
logcm.print_obj(x, 'x')

# y = 半径 * SIN(角度)
y = (radii * np.sin(angles)).flatten()
logcm.print_obj(y, 'y')

# Create the Triangulation; no triangles so Delaunay triangulation created.
triang = tri.Triangulation(x, y)
logcm.print_obj(triang, 'triang')

# Mask off unwanted triangles.
xmid = x[triang.triangles].mean(axis=1)
ymid = y[triang.triangles].mean(axis=1)

# 屏蔽
mask = np.where(xmid * xmid + ymid * ymid < min_radius * min_radius, 1, 0)
triang.set_mask(mask)

# Plot the triangulation.
plt.figure()
plt.gca().set_aspect('equal')
plt.triplot(triang, 'bo-', lw=1)
plt.title('triplot of Delaunay triangulation')

# 保存图片
plt.savefig('images/draw_function1_result.jpg')
# 显示绘制后的图片
plt.show()
