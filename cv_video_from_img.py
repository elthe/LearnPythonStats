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
from common.imagecm import ImageType, VideoImageOutput, VideoActionOutput

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
im_output = VideoImageOutput(videoWriter)

# 取得图片列表
path_list = filecm.search_files(cfg["img_root"], cfg['img_ext'], r'^[^\.]+')
# 取得处理数量
max_size = cfg['max_count']
if max_size > len(path_list):
    max_size = len(path_list)

# 减速列表
slow_move_h = imagecm.slow_down(-1 * cfg['width'], 0, 10)
slow_move_v = imagecm.slow_down(-1 * cfg['height'], 0, 10)
# 加速列表
speed_move_h = imagecm.speed_up(0, cfg['width'], 10)
speed_move_v = imagecm.speed_up(0, cfg['height'], 10)
# 压缩
speed_zip = imagecm.speed_up(0.01, 1.0, 10)
slow_zip = imagecm.slow_down(1.0, 0.01, 10)
# 放大
speed_zoom = imagecm.speed_up(1.0, 2.5, 10)
# 缩小
slow_zoom = imagecm.slow_down(1.0, 0.01, 10)
# 旋转
slow_rotate = imagecm.slow_down(1, 360, 12)
speed_rotate = imagecm.speed_up(1, 360, 12)

for i in range(max_size):
    path = path_list[i]
    logcm.print_info("processing photo %d/%d : %s" % (i + 1, max_size, path))
    im_output.clear()

    # 调整图片尺寸为视频尺寸
    temp_path = './temp/cv/video-from-img/video_img_%d.jpg' % i
    imagecm.resize(path, cfg['width'], cfg['height'], temp_path, keep_ratio=False)

    # 动画输出器
    action_output = VideoActionOutput(im_output, temp_path, (i + 1))

    # # 色调动画
    # action_output.out_action("add_hue", range(1, 5, 1))
    #
    # # 饱和度动画
    # action_output.out_action("change_saturation", range(-50, 50, 10))
    #
    # # 明度动画
    # action_output.out_action("change_darker", range(-100, 100, 20))

    # 放大动画
    action_output.out_action("zoom_in", speed_zoom)
    action_output.out_action("hold", range(5))
    # 缩小动画
    action_output.out_action("zoom_out", slow_zoom)

    # 水平压缩动画
    action_output.out_action("zip_h", slow_zip)
    action_output.out_action("zip_h", speed_zip)

    # 竖直压缩动画
    action_output.out_action("zip_v", slow_zip)
    action_output.out_action("zip_v", speed_zip)

    # 旋转动画
    action_output.out_action("rotate", slow_rotate)
    action_output.out_action("hold", range(5))
    action_output.out_action("rotate", speed_rotate)

    # 移动图片(水平)
    action_output.out_action("move_h", slow_move_h)
    action_output.out_action("hold", range(5))
    action_output.out_action("move_h", speed_move_h)

    # 移动图片(竖直)

    action_output.out_action("move_v", slow_move_v)
    action_output.out_action("hold", range(5))
    action_output.out_action("move_v", speed_move_v)

    # # 标记人脸
    # action_output.out_action("mark_face", range(10, 30, 4), 0.1)
    # # 人脸美白动画
    # action_output.out_action("whitening_face", range(0, 50, 2))
    # # 皮肤美白动画
    # action_output.out_action("whitening_skin", range(0, 50, 2))
    #
    # # 滤镜名称列表
    # filter_list = ["pencil_gray", "pencil_color", "stylize", "detail_enhance", "edge_preserve"]
    # # 滤镜参数调节动画
    # for name in filter_list:
    #     action_output.out_action("im_filter", range(0, 10, 1), filter_name=name)

# 发布视频
videoWriter.release()
