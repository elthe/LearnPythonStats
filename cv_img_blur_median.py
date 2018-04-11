#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
对于图形的平滑与滤波，但从滤波角度来讲，
一般主要的目的都是为了实现对图像噪声的消除，增强图像的效果。
首先介绍二维卷积运算，图像的滤波可以看成是滤波模板与原始图像对应部分的的卷积运算。

对于2D图像可以进行低通或者高通滤波操作，
低通滤波（LPF）有利于去噪，模糊图像，高通滤波（HPF）有利于找到图像边界。

中值滤波模板
中值滤波模板就是用卷积框中像素的中值代替中心值，达到去噪声的目的。
这个模板一般用于去除椒盐噪声。
前面的滤波器都是用计算得到的一个新值来取代中心像素的值，
而中值滤波是用中心像素周围（也可以使他本身）的值来取代他，卷积核的大小也是个奇数。

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
y_list = [0]

# 多子图绘制
fig, axes = plt.subplots(len(x_list), len(y_list) + 2, sharey=False, sharex=False)
# 设置图片尺寸
fig.set_size_inches(5, len(x_list) * 12 // 7)
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
            # 中值滤波
            show = cv2.medianBlur(gray, x_list[i])
            title = "中值(%d)" % (x_list[i])

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
plt.savefig('./images/cv_img_blur_median_result.jpg')
# 显示绘制后的图片
plt.show()
