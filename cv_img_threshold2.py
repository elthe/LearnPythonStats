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

# 直接读为灰度图像
img = cv2.imread('./images/cv_flower.jpg', 0)

ret, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                            cv2.THRESH_BINARY, 11, 2)
th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                            cv2.THRESH_BINARY, 11, 2)
images = [img, th1, th2, th3]
plt.figure()
for i in range(4):
    plt.subplot(2, 2, i + 1), plt.imshow(images[i], 'gray')

# 保存图片
plt.savefig('images/cv_img_threshold2_result.jpg')
# 显示绘制后的图片
plt.show()
