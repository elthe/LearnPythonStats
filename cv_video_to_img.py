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
    "video_path": "/temp/output.avi",
    "img_root": "/path/to/img",
    "max_count" : 10,
    "fps": 5
}
"""

# 加载配置文件
cfg = loadcfgcm.load("cv_video_to_img.json", default_config)

filecm.makedir(cfg['img_root'])

vc=cv2.VideoCapture(cfg['video_path'])
frame_no=0
count = 0
if vc.isOpened():
    rval,frame=vc.read()
else:
    rval=False
while rval:
    rval,frame=vc.read()
    frame_no= frame_no + 1
    if frame_no % cfg['fps'] == 0:
        count += 1
        cv2.imwrite(cfg["img_root"] + str(count) + '.jpg', frame)

    if count > cfg['max_count']:
        break

    cv2.waitKey(1)
vc.release()