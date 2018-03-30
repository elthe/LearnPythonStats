#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
绘制同心三角网，对分隔点数，层数变化，生成对比图。
1）先算半径和角度
2）再算X和Y
3）使用matplotlib.tri.Triangulation计算三角网
4）设置屏蔽范围
5）使用plot.triplot绘制
"""

from common import logcm

import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import math

# 角度分割数列表
angles_list = [2, 3, 4, 5, 6, 8, 10, 14, 20, 26, 30, 36, 42]
# 同心环层数
radii_list = [2, 4, 8, 12]

# 起始半径
min_radius = 0.25

# 多子图绘制
fig, axes = plt.subplots(len(angles_list)*2, len(radii_list), sharey=True, sharex=True)
# 设置图片尺寸
fig.set_size_inches(12, 3 * len(angles_list) * 2)
# 总标题
fig.suptitle('')
# 设置标题(中文字体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


for i in range(len(angles_list)):
    n_angles = angles_list[i]
    for j in  range(len(radii_list)):
        n_radii = radii_list[j]
        ax1 = axes[2*i][j]
        ax2 = axes[2*i+1][j]

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

        # 生成三角网
        triang = tri.Triangulation(x, y)
        logcm.print_obj(triang.triangles, 'triang.triangles')

        ax2.triplot(triang, 'bo-', lw=1, color='g')
        ax2.set_title("%d点 %d层 中心无屏蔽" % (n_angles, n_radii))

        # Mask off unwanted triangles.
        xmid = x[triang.triangles].mean(axis=1)
        ymid = y[triang.triangles].mean(axis=1)

        # 屏蔽最中心的圆环内部部分。
        mask = np.where(xmid * xmid + ymid * ymid < min_radius * min_radius, 1, 0)
        triang.set_mask(mask)

        ax1.triplot(triang, 'bo-', lw=1)
        ax1.set_title("%d点 %d层 中心有屏蔽" % (n_angles, n_radii))

# 调整每隔子图之间的距离
plt.tight_layout()
# 保存图片
plt.savefig('images/draw_triangulation1_result.jpg')
# 显示绘制后的图片
plt.show()
