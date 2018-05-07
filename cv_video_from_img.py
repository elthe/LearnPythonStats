#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
把特定文件夹下的一系列图片做成一个视频，并且每帧出现频率可以调整；
"""

import cv2
import numpy as np
import cv2
from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
import os
import math
from common import loadcfgcm
from common import filecm
from common import imagecm

# 配置
default_config = """
{
    "img_root": "/path/to/img",
    "max_count" : 10,
    "fps": 5,
    "save_path": "/temp/output.avi",
    "width": 1200,
    "height": 1200
}
"""

# 加载配置文件
cfg = loadcfgcm.load("cv_video_from_img.json", default_config)

filecm.makedir(cfg['save_path'], True)

fourcc = VideoWriter_fourcc(*"MJPG")
videoWriter = cv2.VideoWriter(cfg['save_path'], fourcc, cfg['fps'], (cfg['width'], cfg['height']))

path_list = filecm.search_files(cfg["img_root"], '.jpg', r'^[^\.]+')
max_size = cfg['max_count']
if max_size > len(path_list):
    max_size = len(path_list)

for i in range(max_size):
    path = path_list[i]

    # 调整图片尺寸为视频尺寸
    temp_path = './temp/cv/video-from_image/video_img_%d.jpg' % i
    imagecm.resize(path, cfg['width'], cfg['height'], temp_path, keep_ratio=False)

    frame = cv2.imread(temp_path)
    videoWriter.write(frame)

videoWriter.release()