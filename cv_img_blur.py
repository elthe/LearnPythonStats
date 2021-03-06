#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
对于图形的平滑与滤波，但从滤波角度来讲，
一般主要的目的都是为了实现对图像噪声的消除，增强图像的效果。
首先介绍二维卷积运算，图像的滤波可以看成是滤波模板与原始图像对应部分的的卷积运算。

对于2D图像可以进行低通或者高通滤波操作，
低通滤波（LPF）有利于去噪，模糊图像，高通滤波（HPF）有利于找到图像边界。

均值滤波
而opencv有一个专门的平均滤波模板供使用–归一化卷积模板，
所有的滤波模板都是使卷积框覆盖区域所有像素点与模板相乘后得到的值作为中心像素的值。
Opencv中均值模板可以用cv2.blur和cv2.boxFilter,
模板大小是m*n是可以设置的。如果你不想要前面的1/9,可以使用非归一化的模板cv2.boxFilter。
模板大小3*5

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

# 列表
x_list = range(3, 36, 2)

# 参数列表
y_list = [3, 5, 9, 15, 21, 25]

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
            title = '灰度图'
        else:
            # 均值滤波
            show = cv2.blur(gray, (x_list[i], y_list[j - 2]))
            title = "模版(%d,%d)" % (x_list[i], y_list[j - 2])

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
plt.savefig('./images/cv_img_blur_result.jpg')
# 显示绘制后的图片
plt.show()
