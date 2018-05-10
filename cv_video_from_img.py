#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
把特定文件夹下的一系列图片做成一个视频，并且每帧出现频率可以调整；
"""

import cv2
import numpy as np
import cv2
from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
from skimage import transform, data, io

import os
import math
from common import loadcfgcm
from common import filecm
from common import imagecm
from common import logcm
from common import opencvcm

# 配置
default_config = """
{
    "img_root": "./images/img",
    "img_ext": ".jpeg",
    "max_count" : 10,
    "fps": 10,
    "save_path": "./temp/output.avi",
    "width": 1024,
    "height": 683
}
"""

# 加载配置文件
cfg = loadcfgcm.load("cv_video_from_img.json", default_config)

# 创建目录
filecm.makedir(cfg['save_path'], True)
filecm.makedir('./temp/cv/video-from-img')

# 新建视频写入类
fourcc = VideoWriter_fourcc(*"MJPG")
videoWriter = cv2.VideoWriter(cfg['save_path'], fourcc, cfg['fps'], (cfg['width'], cfg['height']))

# 取得图片列表
path_list = filecm.search_files(cfg["img_root"], cfg['img_ext'], r'^[^\.]+')
# 取得处理数量
max_size = cfg['max_count']
if max_size > len(path_list):
    max_size = len(path_list)

for i in range(max_size):
    path = path_list[i]

    # 调整图片尺寸为视频尺寸
    temp_path = './temp/cv/video-from-img/video_img_%d.jpg' % i
    temp_path2 = './temp/cv/video-from-img/video_img_%d-2.jpg' % i
    imagecm.resize(path, cfg['width'], cfg['height'], temp_path, keep_ratio=False)

    # 写入图片到视频
    frame = cv2.imread(temp_path)
    videoWriter.write(frame)

    # 通过cv2.cvtColor把图像从BGR转换到HSV
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # HSV分别是色调（Hue），饱和度（Saturation）和明度（Value）。
    # 在HSV空间中进行调节就避免了直接在RGB空间中调节是还需要考虑三个通道的相关性。
    # OpenCV中H的取值是[0, 180)，其他两个通道的取值都是[0, 256)

    turn_green_hsv = img_hsv.copy()
    # H空间中，绿色比黄色的值高一点，所以给每个像素+15，黄色的树叶就会变绿
    for i in range(1, 15, 1):
        turn_green_hsv[:, :, 0] = (turn_green_hsv[:, :, 0] + i) % 180
        turn_green_img = cv2.cvtColor(turn_green_hsv, cv2.COLOR_HSV2BGR)
        videoWriter.write(turn_green_img)

    # 减小饱和度会让图像损失鲜艳，变得更灰
    colorless_hsv = img_hsv.copy()
    for i in range(10, 1, 1):
        colorless_hsv[:, :, 1] = (i / 10) * colorless_hsv[:, :, 1]
        colorless_img = cv2.cvtColor(colorless_hsv, cv2.COLOR_HSV2BGR)
        videoWriter.write(colorless_img)

    # 减小明度为原来一半
    darker_hsv = img_hsv.copy()
    for j in range(10, 1, 1):
        darker_hsv[:, :, 2] = (i / 10) * darker_hsv[:, :, 2]
        darker_img = cv2.cvtColor(darker_hsv, cv2.COLOR_HSV2BGR)
        videoWriter.write(darker_img)

    # 灰度转换
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame2 = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    videoWriter.write(frame2)

    # 放大动画
    for ratio in range(10, 20, 1):
        img = imagecm.zoom_in(temp_path, ratio/10)
        videoWriter.write(opencvcm.image_to_array(img))

    # 缩小动画
    for ratio in range(10, 1, 1):
        img = imagecm.zoom_out(temp_path, ratio/10)
        videoWriter.write(opencvcm.image_to_array(img))

    # 旋转动画
    for i in range(12):
        img2 = io.imread(temp_path)
        img3 = transform.rotate(img2, (i + 1) * 30, resize=False)
        cv_image = opencvcm.skimage_to_array(img3)
        videoWriter.write(cv_image)

# 发布视频
videoWriter.release()
