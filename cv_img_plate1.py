#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
从汽车图片中找到车牌部分。
"""

import cv2
import glob as gb

from common import filecm
from common import opencvcm
from common import plotcm

# 获取plates文件夹下所有文件路径
img_path = gb.glob("./images/plates/*")
# 定义并创建临时目录
tmp_path = './temp/cv/plate'
filecm.makedir(tmp_path)

# 图片矩阵
img_matrix = []
# 标题矩阵
title_matrix = []

## 对每一张图片进行处理
for path in img_path:
    img_list = []
    title_list = []

    img = cv2.imread(path)
    img_list.append(img)
    filename = filecm.short_name(path)
    title_list.append('原图-%s' % filename)

    # 灰度转换
    gray = opencvcm.get_gray(img, tmp_path, filename, img_list, title_list)
    # 平滑转
    blur = opencvcm.get_blur(gray, True, (3, 3), 5, tmp_path, filename, img_list, title_list)
    # 边缘检测
    sobel = opencvcm.get_sobel(blur, 1, 0, 3, cv2.CV_8U, tmp_path, filename, img_list, title_list)
    # 二值化
    thresh = opencvcm.get_thresh(sobel, 170, cv2.THRESH_BINARY, tmp_path, filename, img_list, title_list)
    # 边界
    kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 7))
    kernel_erode = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
    edges = opencvcm.get_edges(thresh, 'DED-DE', kernel_dilate, kernel_erode, tmp_path, filename, img_list,
                               title_list)

    # 查找车牌区域，指定最小面积，宽高比范围
    rois = opencvcm.find_rois(edges, min_area=2000, min_wh_ratio=2, max_wh_ratio=5)
    img_plate = None
    if len(rois) > 0:
        # 取最大面积区域
        max_roi = opencvcm.get_max_roi(rois)
        (x, y, w, h) = max_roi
        img_plate = img[y:y + h, x:x + w]

    img_list.append(img_plate)
    title_list.append('车牌-%s' % filename)

    img_matrix.append(img_list)
    title_matrix.append(title_list)

# 把图片一览网格显示并保存
save_path = './images/cv_img_plate1_result.jpg'
plotcm.grid_by_matrix(img_matrix, title_matrix, 6, save_path, cell_width=2.5, cell_height=2)
