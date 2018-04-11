#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简单阈值
简单阈值当然是最简单，选取一个全局阈值，然后就把整幅图像分成了非黑即白的二值图像了。
函数为cv2.threshold()
这个函数有四个参数，
    第一个原图像，
    第二个进行分类的阈值，
    第三个是高于（低于）阈值时赋予的新值，
    第四个是一个方法选择参数，常用的有：
        • cv2.THRESH_BINARY（黑白二值）
        • cv2.THRESH_BINARY_INV（黑白二值反转）
        • cv2.THRESH_TRUNC （得到的图像为多像素值）
        • cv2.THRESH_TOZERO
        • cv2.THRESH_TOZERO_INV
该函数有两个返回值，
    第一个retVal（得到的阈值值（在后面一个方法中会用到）），
    第二个就是阈值化后的图像。
"""

import cv2
import matplotlib.pyplot as plt

# 读取图像
img = cv2.imread('./images/cv_flower2.jpg')

# 灰度转换
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 阈值列表
thresh_list = range(10, 250, 10)
# 参数列表
param_list = [cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV, cv2.THRESH_TRUNC, cv2.THRESH_TOZERO, cv2.THRESH_TOZERO_INV]
# 标题列表
title_list = ['BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']

# 多子图绘制
fig, axes = plt.subplots(len(thresh_list), len(param_list) + 2, sharey=False, sharex=False)
# 设置图片尺寸
fig.set_size_inches(12, len(thresh_list) * 12 // 7)
# 总标题
fig.suptitle('')
# 设置标题(中文字体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

for i in range(len(thresh_list)):
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
            ret, show = cv2.threshold(gray, thresh_list[i], 255, param)
            title = "%s-阈值:%d" % (title_list[j - 2], thresh_list[i])

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
plt.savefig('./images/cv_img_threshold_result.jpg')
# 显示绘制后的图片
plt.show()
