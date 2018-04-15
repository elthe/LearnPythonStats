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
from common import cvfacecm
from common import filecm
from common import logcm

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

# 模型
face_model = cvfacecm.get_face_detect()

# 定义并创建临时目录
tmp_path = './temp/cv/faces'
filecm.makedir(tmp_path)

while True:
    # 读取视频流
    grabbed, frame_lwpCV = camera.read()

    vis, rects = cvfacecm.detect(face_model, frame_lwpCV, tmp_path, "video")
    logcm.print_obj(vis, "vis")

    cvfacecm.draw_rects(frame_lwpCV, rects, (255, 0, 0))
    cv2.imshow('contours', frame_lwpCV)

    key = cv2.waitKey(1) & 0xFF
    # 按'q'健退出循环
    if key == ord('q'):
        break

# When everything done, release the capture
camera.release()
cv2.destroyAllWindows()
