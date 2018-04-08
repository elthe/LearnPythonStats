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

# 直接读为灰度图像
img = cv2.imread('./images/cv_flower.jpg', 0)

ret, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
ret, thresh2 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
ret, thresh3 = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)
ret, thresh4 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)
ret, thresh5 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO_INV)

titles = ['img', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
for i in range(6):
    plt.subplot(2, 3, i + 1), plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])


# 保存图片
plt.savefig('images/cv_img_threshold1_result.jpg')
# 显示绘制后的图片
plt.show()
