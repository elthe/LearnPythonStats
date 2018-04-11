#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
对于图形的平滑与滤波，但从滤波角度来讲，
一般主要的目的都是为了实现对图像噪声的消除，增强图像的效果。
首先介绍二维卷积运算，图像的滤波可以看成是滤波模板与原始图像对应部分的的卷积运算。

对于2D图像可以进行低通或者高通滤波操作，
低通滤波（LPF）有利于去噪，模糊图像，高通滤波（HPF）有利于找到图像边界。

# 双边滤波
# 双边滤波函数为cv2.bilateralFilter()。
# 该滤波器可以在保证边界清晰的情况下有效的去掉噪声。
# 它的构造比较复杂，即考虑了图像的空间关系，也考虑图像的灰度关系。
# 双边滤波同时使用了空间高斯权重和灰度相似性高斯权重，确保了边界不会被模糊掉。
# cv2.bilateralFilter(img,d,’p1’,’p2’)函数有四个参数需要，
# d是领域的直径，后面两个参数是空间高斯函数标准差和灰度值相似性高斯函数标准差。
# 9---滤波领域直径
# 后面两个数字：空间高斯函数标准差，灰度值相似性标准差

"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取图像
img = cv2.imread('./images/cv_flower2.jpg')

# 灰度转换
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 添加点噪声
for i in range(2000):
    temp_x = np.random.randint(0, img.shape[0])
    temp_y = np.random.randint(0, img.shape[1])
    gray[temp_x][temp_y] = 255

# 转化数值类型
img1 = np.float32(img)

# 列表
x_list = range(3, 36, 2)

# 参数列表
y_list = [25, 50, 75, 80, 90]

# 多子图绘制
fig, axes = plt.subplots(len(x_list), len(y_list) + 2, sharey=False, sharex=False)
# 设置图片尺寸
fig.set_size_inches(10, len(x_list) * 12 // 7)
# 总标题
fig.suptitle('')
# 设置标题(中文字体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

for i in range(len(x_list)):
    for j in range(len(y_list) + 2):
        if j == 0:
            show = img
            title = '原图'
        elif j == 1:
            show = gray
            title = '灰度+噪声'
        else:
            # 双边滤波
            show = cv2.bilateralFilter(gray, x_list[i], y_list[j - 2], y_list[j - 2])
            title = "径%d-标%d" % (x_list[i], y_list[j - 2])

        ax = axes[i][j]
        # 显示图片
        ax.imshow(show, 'gray')
        # 显示标题
        ax.set_title(title)
        # 隐藏坐标轴
        ax.set_xticks([])
        ax.set_yticks([])

# 调整每隔子图之间的距离
plt.tight_layout()
# 保存图片
plt.savefig('./images/cv_img_blur_bilateral_result.jpg')
# 显示绘制后的图片
plt.show()