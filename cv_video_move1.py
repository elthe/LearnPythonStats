#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
目标跟踪是对摄像头视频中的移动目标进行定位的过程，有着非常广泛的应用。
实时目标跟踪是许多计算机视觉应用的重要任务，如监控、基于感知的用户界面、增强现实、基于对象的视频压缩以及辅助驾驶等。

有很多实现视频目标跟踪的方法，当跟踪所有移动目标时，帧之间的差异会变的有用；
当跟踪视频中移动的手时，基于皮肤颜色的均值漂移方法是最好的解决方案；当知道跟踪对象的一方面时，模板匹配是不错的技术。

本代码是做一个基本的运动检测
考虑的是“背景帧”与其它帧之间的差异
这种方法检测结果还是挺不错的，但是需要提前设置背景帧，
如果是在室外，光线的变化就会引起误检测，还是很有局限性的。

"""

import cv2
import numpy as np

camera = cv2.VideoCapture(0)  # 参数0表示第一个摄像头
# 判断视频是否打开
if (camera.isOpened()):
    print('Open')
else:
    print('摄像头未打开')

# 测试用,查看视频size
size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print('size:' + repr(size))

es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
kernel = np.ones((5, 5), np.uint8)
background = None

while True:
    # 读取视频流
    grabbed, frame_lwpCV = camera.read()
    # 对帧进行预处理，先转灰度图，再进行高斯滤波。
    # 用高斯滤波进行模糊处理，进行处理的原因：每个输入的视频都会因自然震动、光照变化或者摄像头本身等原因而产生噪声。
    # 对噪声进行平滑是为了避免在运动和跟踪时将其检测出来。
    gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY)
    gray_lwpCV = cv2.GaussianBlur(gray_lwpCV, (21, 21), 0)

    # 将第一帧设置为整个输入的背景
    if background is None:
        background = gray_lwpCV
        continue
    # 对于每个从背景之后读取的帧都会计算其与北京之间的差异，并得到一个差分图（different map）。
    # 还需要应用阈值来得到一幅黑白图像，并通过下面代码来膨胀（dilate）图像，
    # 从而对孔（hole）和缺陷（imperfection）进行归一化处理
    diff = cv2.absdiff(background, gray_lwpCV)
    diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]  # 二值化阈值处理
    diff = cv2.dilate(diff, es, iterations=2)  # 形态学膨胀

    # 显示矩形框
    # 该函数计算一幅图像中目标的轮廓
    image, contours, hierarchy = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        # 对于矩形区域，只显示大于给定阈值的轮廓，所以一些微小的变化不会显示。
        # 对于光照不变和噪声低的摄像头可不设定轮廓最小尺寸的阈值
        if cv2.contourArea(c) < 1500:
            continue
        # 该函数计算矩形的边界框
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('contours', frame_lwpCV)
    cv2.imshow('dis', diff)

    key = cv2.waitKey(1) & 0xFF
    # 按'q'健退出循环
    if key == ord('q'):
        break

# When everything done, release the capture
camera.release()
cv2.destroyAllWindows()
