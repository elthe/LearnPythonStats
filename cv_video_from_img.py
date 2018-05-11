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
from common.opencvcm import ImageType

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
    logcm.print_info("processing photo %d/%d : %s" % (i+1, max_size, path))

    # 调整图片尺寸为视频尺寸
    temp_path = './temp/cv/video-from-img/video_img_%d.jpg' % i
    imagecm.resize(path, cfg['width'], cfg['height'], temp_path, keep_ratio=False)

    # 写入图片到视频
    frame = cv2.imread(temp_path)
    videoWriter.write(frame)

    # 色调动画
    for i in range(1, 5, 1):
        img = opencvcm.add_img_HSV(frame, ImageType.IMG_BGR, add_h=i)
        videoWriter.write(img)

    # 饱和度动画
    for i in range(5, 11, 1):
        img = opencvcm.add_img_HSV(frame, ImageType.IMG_BGR, ratio_s=i / 10)
        videoWriter.write(img)
    # 明度动画
    for i in range(70, 100, 10):
        img = opencvcm.add_img_HSV(frame, ImageType.IMG_BGR, ratio_v=i / 100)
        videoWriter.write(img)

    # 放大动画
    for ratio in range(11, 20, 1):
        img = imagecm.zoom_in(temp_path, ratio / 10)
        videoWriter.write(opencvcm.image_convert(img, ImageType.IMG_PIL))

    # 缩小动画
    for ratio in range(9, 1, -1):
        img = imagecm.zoom_out(temp_path, ratio / 10)
        videoWriter.write(opencvcm.image_convert(img, ImageType.IMG_PIL))

    # 旋转动画
    for i in range(12):
        img2 = io.imread(temp_path)
        img3 = transform.rotate(img2, (i + 1) * 30, resize=False)
        cv_image = opencvcm.image_convert(img3, ImageType.IMG_SK)
        videoWriter.write(cv_image)

    # 移动图片
    for i in range(-1*cfg['width'], cfg['width'], 50):
        img = imagecm.move(temp_path, move_h=i)
        videoWriter.write(opencvcm.image_convert(img, ImageType.IMG_PIL))

    # 移动图片
    for i in range(-1 * cfg['height'], cfg['height'], 50):
        img = imagecm.move(temp_path, move_v=i)
        videoWriter.write(opencvcm.image_convert(img, ImageType.IMG_PIL))

# 发布视频
videoWriter.release()
