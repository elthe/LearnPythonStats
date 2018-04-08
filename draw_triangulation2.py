#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
绘制3D同心三角网，对分隔点数，层数变化，生成对比图。
1）先算半径和角度
2）再算X和Y
3）使用matplotlib.tri.Triangulation计算三角网
4）设置屏蔽范围
5）使用plot.triplot绘制
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import scipy.spatial

from common import logcm
from mpl_toolkits.mplot3d import Axes3D

# 角度分割数列表
angles_list = [2, 3, 4, 5, 6, 8, 10, 14, 20, 26, 30, 36, 42]
# 同心环层数
radii_list = [2, 4, 8, 12]
# Z value
z_list = [5, 10, 15, 20]

# 起始半径
min_radius = 0.25

# 图绘制
fig = plt.figure()
# 设置图片尺寸
fig.set_size_inches(14, 3 * len(angles_list))

# 设置标题(中文字体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

for i in range(len(angles_list)):
    n_angles = angles_list[i]
    for j in range(len(radii_list)):
        n_radii = radii_list[j]

        idx = i * len(radii_list) + j + 1
        logcm.print_obj(idx, 'idx')
        ax = fig.add_subplot(len(angles_list), len(radii_list), idx, projection='3d')

        z_idx = z_list[i % len(z_list)]

        # 半径数组
        radii = np.linspace(min_radius, 0.95, n_radii)

        # 角度数组（0～2PI）
        angles = np.linspace(0, 2 * math.pi, n_angles, endpoint=False)
        logcm.print_obj(angles, 'angles')

        # 增加一个新维度，并复制N份
        angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)
        logcm.print_obj(angles, 'angles after repeat')

        # 在第二维度上，从1开始，每两个加上单位角度的一半
        angles[:, 1::2] += math.pi / n_angles
        logcm.print_obj(angles, 'angles new2')

        # x = 半径 * COS(角度)
        x = (radii * np.cos(angles)).flatten()
        logcm.print_obj(x, 'x')

        # y = 半径 * SIN(角度)
        y = (radii * np.sin(angles)).flatten()
        logcm.print_obj(y, 'y')

        # Create the Delaunay tessalation using scipy.spatial
        pts = np.vstack([x, y]).T
        tess = scipy.spatial.Delaunay(pts)

        # Create the matplotlib Triangulation object
        x = tess.points[:, 0]
        y = tess.points[:, 1]
        tri = tess.vertices  # or tess.simplices depending on scipy version
        triang = mtri.Triangulation(x=pts[:, 0], y=pts[:, 1], triangles=tri)

        # Plotting
        z = x * x + y * y + z_idx

        ax.plot_trisurf(triang, z)
        ax.set_title("%d点 %d层 高%d" % (n_angles, n_radii, z_idx))

# 调整每隔子图之间的距离
plt.tight_layout()
# 保存图片
plt.savefig('images/draw_triangulation2_result.jpg')
# 显示绘制后的图片
plt.show()
