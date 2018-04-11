#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自适应阈值
前面看到简单阈值是一种全局性的阈值，只需要规定一个阈值值，整个图像都和这个阈值比较。
而自适应阈值可以看成一种局部性的阈值，通过规定一个区域大小，
比较这个点与区域大小里面像素点的平均值（或者其他特征）的大小关系确定这个像素点是属于黑或者白（如果是二值情况）。
使用的函数为：cv2.adaptiveThreshold（）
该函数需要填6个参数：
    第一个原始图像
    第二个像素值上限
    第三个自适应方法Adaptive Method:
        — cv2.ADAPTIVE_THRESH_MEAN_C ：领域内均值
        — cv2.ADAPTIVE_THRESH_GAUSSIAN_C ：领域内像素点加权和，权重为一个高斯窗口
    第四个值的赋值方法：只有cv2.THRESH_BINARY 和cv2.THRESH_BINARY_INV
    第五个Block size:规定领域大小（一个正方形的领域）
    第六个常数C，阈值等于均值或者加权值减去这个常数（为0相当于阈值 就是求得领域内均值或者加权值）
这种方法理论上得到的效果更好，相当于在动态自适应的调整属于自己像素点的阈值，而不是整幅图像都用一个阈值。
"""

import cv2
import matplotlib.pyplot as plt

# 读取图像
img = cv2.imread('./images/cv_flower2.jpg')

# 灰度转换
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 阈值列表
size_list = range(5, 126, 4)
# 参数列表
param_list = [
    [cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY],
    [cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV],
    [cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY],
    [cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV]
]
# 标题列表
title_list = ['MEAN-BINARY', 'MEAN-INV', 'GAUSSIAN-BINARY', 'GAUSSIAN-INV']

# 多子图绘制
fig, axes = plt.subplots(len(size_list), len(param_list) + 2, sharey=False, sharex=False)
# 设置图片尺寸
fig.set_size_inches(12, len(size_list) * 12 // 7)
# 总标题
fig.suptitle('')
# 设置标题(中文字体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

for i in range(len(size_list)):
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
            show = cv2.adaptiveThreshold(gray, 255, param[0], param[1], size_list[i], 0)
            title = "%s-Block:%d" % (title_list[j - 2], size_list[i])

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
plt.savefig('./images/cv_img_threshold_adpt_result.jpg')
# 显示绘制后的图片
plt.show()
