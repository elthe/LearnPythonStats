#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
对于图形的平滑与滤波，但从滤波角度来讲，
一般主要的目的都是为了实现对图像噪声的消除，增强图像的效果。
首先介绍二维卷积运算，图像的滤波可以看成是滤波模板与原始图像对应部分的的卷积运算。

对于2D图像可以进行低通或者高通滤波操作，
低通滤波（LPF）有利于去噪，模糊图像，高通滤波（HPF）有利于找到图像边界。
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

# 直接读为灰度图像
img = cv2.imread('./images/cv_flower.jpg', 0)

# 转化数值类型
img1 = np.float32(img)
kernel = np.ones((5, 5), np.float32) / 25

# 统一的2D滤波器cv2.filter2D
# Opencv提供的一个通用的2D滤波函数为cv2.filter2D()，
# 滤波函数的使用需要一个核模板，对图像的滤波操作过程为：
# 将和模板放在图像的一个像素A上，求与之对应的图像上的每个像素点的和，核不同，得到的结果不同，
# 而滤波的使用核心也是对于这个核模板的使用，需要注意的是，该滤波函数是单通道运算的，
# 也就是说对于彩色图像的滤波，需要将彩色图像的各个通道提取出来，对各个通道分别滤波才行。
# 这里说一个与matlab相似的情况，matlab中也有一个类似的滤波函数imfilter,
# 对于滤波函数的应用其实不只在于滤波，对于许多图像的整体处理上，
# 其实都可以用滤波函数来组合实现，得到更快的效果
# cv2.filter2D(src,dst,kernel,auchor=(-1,-1))函数：
# 输出图像与输入图像大小相同
# 中间的数为-1，输出数值格式的相同plt.figure()
dst = cv2.filter2D(img1, -1, kernel)

# 均值滤波
# 而opencv有一个专门的平均滤波模板供使用–归一化卷积模板，
# 所有的滤波模板都是使卷积框覆盖区域所有像素点与模板相乘后得到的值作为中心像素的值。
# Opencv中均值模板可以用cv2.blur和cv2.boxFilter,
# 模板大小是m*n是可以设置的。如果你不想要前面的1/9,可以使用非归一化的模板cv2.boxFilter。
# 模板大小3*5
blur1 = cv2.blur(img, (3, 5))

# 高斯模糊模板
# 现在把卷积模板中的值换一下，不是全1了，换成一组符合高斯分布的数值放在模板里面，
# 比如这时中间的数值最大，往两边走越来越小，构造一个小的高斯包。
# 实现的函数为cv2.GaussianBlur()。
# 对于高斯模板，我们需要制定的是高斯核的高和宽（奇数），
# 沿x与y方向的标准差(如果只给x，y=x，如果都给0，那么函数会自己计算)。
# 高斯核可以有效的出去图像的高斯噪声。
# 当然也可以自己构造高斯核，相关函数：cv2.GaussianKernel().
for i in range(2000):
    # 添加点噪声
    temp_x = np.random.randint(0, img.shape[0])
    temp_y = np.random.randint(0, img.shape[1])
    img[temp_x][temp_y] = 255
blur2 = cv2.GaussianBlur(img, (5, 5), 0)

# 中值滤波模板
# 中值滤波模板就是用卷积框中像素的中值代替中心值，达到去噪声的目的。
# 这个模板一般用于去除椒盐噪声。
# 前面的滤波器都是用计算得到的一个新值来取代中心像素的值，
# 而中值滤波是用中心像素周围（也可以使他本身）的值来取代他，卷积核的大小也是个奇数。
blur3 = cv2.medianBlur(img, 5)

# 双边滤波
# 双边滤波函数为cv2.bilateralFilter()。
# 该滤波器可以在保证边界清晰的情况下有效的去掉噪声。
# 它的构造比较复杂，即考虑了图像的空间关系，也考虑图像的灰度关系。
# 双边滤波同时使用了空间高斯权重和灰度相似性高斯权重，确保了边界不会被模糊掉。
# cv2.bilateralFilter(img,d,’p1’,’p2’)函数有四个参数需要，
# d是领域的直径，后面两个参数是空间高斯函数标准差和灰度值相似性高斯函数标准差。
# 9---滤波领域直径
# 后面两个数字：空间高斯函数标准差，灰度值相似性标准差
blur4 = cv2.bilateralFilter(img, 9, 75, 75)

# 默认彩色，另一种彩色bgr
plt.subplot(3, 2, 1), plt.imshow(img1, 'gray')
plt.subplot(3, 2, 2), plt.imshow(dst, 'gray')
plt.subplot(3, 2, 3), plt.imshow(blur1, 'gray')
plt.subplot(3, 2, 4), plt.imshow(blur2, 'gray')
plt.subplot(3, 2, 5), plt.imshow(blur3, 'gray')
plt.subplot(3, 2, 6), plt.imshow(blur4, 'gray')

# 保存图片
plt.savefig('images/cv_img_filter1_result.jpg')
# 显示绘制后的图片
plt.show()
