#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
把特定文件夹下的一系列图片做成一个视频，并且每帧出现频率可以调整；
"""

import cv2

from common import filecm
from common import imagecm
from common import imfiltercm
from common import loadcfgcm
from common import logcm
from common.imagecm import ImageType, VideoImageOutput

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
fourcc = cv2.VideoWriter_fourcc(*"MJPG")
videoWriter = cv2.VideoWriter(cfg['save_path'], fourcc, cfg['fps'], (cfg['width'], cfg['height']))
output = VideoImageOutput(videoWriter)

# 取得图片列表
path_list = filecm.search_files(cfg["img_root"], cfg['img_ext'], r'^[^\.]+')
# 取得处理数量
max_size = cfg['max_count']
if max_size > len(path_list):
    max_size = len(path_list)

for i in range(max_size):
    path = path_list[i]
    logcm.print_info("processing photo %d/%d : %s" % (i + 1, max_size, path))
    output.clear()

    # 调整图片尺寸为视频尺寸
    temp_path = './temp/cv/video-from-img/video_img_%d.jpg' % i
    imagecm.resize(path, cfg['width'], cfg['height'], temp_path, keep_ratio=False)

    # 写入图片到视频
    frame = cv2.imread(temp_path)
    output.write(frame)

    # 色调动画
    for i in range(1, 5, 1):
        img = imagecm.add_img_HSV(frame, ImageType.IMG_BGR, add_h=i)
        output.write(img)

    # 饱和度动画
    for i in range(-50, 50, 10):
        img = imfiltercm.change_saturation(frame, i)
        output.write(img)

    # 明度动画
    for i in range(-100, 100, 20):
        img = imfiltercm.change_saturation(frame, i)
        output.write(img)

    # 放大动画
    for ratio in range(11, 20, 1):
        img = imagecm.zoom_in(temp_path, ratio / 10)
        output.write(img, ImageType.IMG_PIL)

    # 缩小动画
    for ratio in range(9, 1, -1):
        img = imagecm.zoom_out(temp_path, ratio / 10)
        output.write(img, ImageType.IMG_PIL)

    # 旋转动画
    for i in range(12):
        im_sk = imagecm.rotate(temp_path, (i + 1) * 30, resize=False)
        output.write(im_sk, ImageType.IMG_SK)

    # 移动图片
    for i in range(-1 * cfg['width'], cfg['width'], 100):
        img = imagecm.move(temp_path, move_h=i)
        output.write(img, ImageType.IMG_PIL)

    # 移动图片
    for i in range(-1 * cfg['height'], cfg['height'], 100):
        img = imagecm.move(temp_path, move_v=i)
        output.write(img, ImageType.IMG_PIL)

    # 标记人脸
    faces = imfiltercm.detect_face(frame)
    img_face = imfiltercm.mark_face(frame, faces, border=2)
    for i in range(5):
        output.write(img_face)

    # 人脸美白动画
    for i in range(0, 50, 2):
        img = imfiltercm.whitening_face(img_face, faces, i)
        output.write(img)

    # 皮肤
    im_skin = imfiltercm.detect_skin(frame)
    # 皮肤美白动画
    for i in range(0, 50, 2):
        img = imfiltercm.whitening_skin(frame, im_skin, i)
        output.write(img)

# 发布视频
videoWriter.release()
