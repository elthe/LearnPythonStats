#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
对于图形的平滑与滤波，但从滤波角度来讲，
一般主要的目的都是为了实现对图像噪声的消除，增强图像的效果。
首先介绍二维卷积运算，图像的滤波可以看成是滤波模板与原始图像对应部分的的卷积运算。

对于2D图像可以进行低通或者高通滤波操作，
低通滤波（LPF）有利于去噪，模糊图像，高通滤波（HPF）有利于找到图像边界。

统一的2D滤波器cv2.filter2D
Opencv提供的一个通用的2D滤波函数为cv2.filter2D()，
滤波函数的使用需要一个核模板，对图像的滤波操作过程为：
将和模板放在图像的一个像素A上，求与之对应的图像上的每个像素点的和，核不同，得到的结果不同，
而滤波的使用核心也是对于这个核模板的使用，需要注意的是，该滤波函数是单通道运算的，
也就是说对于彩色图像的滤波，需要将彩色图像的各个通道提取出来，对各个通道分别滤波才行。
这里说一个与matlab相似的情况，matlab中也有一个类似的滤波函数imfilter,
对于滤波函数的应用其实不只在于滤波，对于许多图像的整体处理上，
其实都可以用滤波函数来组合实现，得到更快的效果
cv2.filter2D(src,dst,kernel,auchor=(-1,-1))函数：
输出图像与输入图像大小相同
中间的数为-1，输出数值格式的相同plt.figure()
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取图像
img = cv2.imread('./images/cv_flower2.jpg')

# 灰度转换
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 转化数值类型
img1 = np.float32(img)

# kernel定义
kernel_identity = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
kernel_3x3 = np.ones((3, 3), np.float32) / 9.0
kernel_5x5 = np.ones((5, 5), np.float32) / 25.0
kernel_1 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
kernel_2 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
kernel_myh = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
# 列表
kernel_list = [kernel_identity, kernel_3x3, kernel_5x5, kernel_1, kernel_2, kernel_myh]
kernel_name = ["identity", "3x3", "5x5", "kernel_1", "kernel_2", "myh"]

# 参数列表
param_list = [-1, cv2.CV_16S, cv2.CV_32F, cv2.CV_64F]
# 标题列表
title_list = ['Same', 'CV_16S', 'CV_32F', 'CV_64F']

# 多子图绘制
fig, axes = plt.subplots(len(kernel_list), len(param_list) + 2, sharey=False, sharex=False)
# 设置图片尺寸
fig.set_size_inches(10, len(kernel_list) * 12 // 7)
# 总标题
fig.suptitle('')
# 设置标题(中文字体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

for i in range(len(kernel_list)):
    for j in range(len(param_list) + 2):
        if j == 0:
            show = img
            title = '原图'
        elif j == 1:
            show = gray
            title = '灰度图'
        else:
            param = param_list[j - 2]
            # 简单阈值
            show = cv2.filter2D(gray, param, kernel_list[i])
            title = "%s-%s" % (title_list[j - 2], kernel_name[i])

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
plt.savefig('./images/cv_img_filter2d_result.jpg')
# 显示绘制后的图片
plt.show()
