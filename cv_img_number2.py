#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数字图片的训练和识别。
"""

import cv2

from common import cvknncm
from common import datecm
from common import filecm
from common import opencvcm
from common import plotcm

# 临时目录
tmp_path = './temp/cv/digits/' + datecm.now_time_str()
filecm.makedir(tmp_path)

# KNN算法对象（初始化并训练好）
knn = cvknncm.get_hand_digits_knn()
# 载入测试图片
img_test = cv2.imread('./images/cv_img_number2_test.jpg')

# 图片列表
img_list = []
# 标题列表
title_list = []

img_list.append(img_test)
title_list.append('原图+结果')

gray = opencvcm.get_gray(img_test, tmp_path, "", img_list, title_list)
# 读取图片边界
edges = opencvcm.get_edges(gray, 'D-E', None, None, tmp_path, "", img_list, title_list)
# 阈值处理
thresh = opencvcm.get_thresh(edges, 21, cv2.THRESH_BINARY, tmp_path, "", img_list, title_list)
# 查找兴趣点区域
rois = opencvcm.find_rois(thresh)
digits = []
id = 0
for roi in rois:
    (x, y, w, h) = roi
    id += 1
    # 查询兴趣区域对应的数字
    digit, th = cvknncm.find_hand_digit_knn(knn, edges[y:y + h, x:x + w], 21, tmp_path=tmp_path, tmp_key=id)
    digits.append(cv2.resize(th, (20, 20)))

    # 绘制边框到图片上
    cv2.rectangle(img_test, (x, y), (x + w, y + h), (153, 153, 0), 2)

    # 把ID和结果文字输出到图片上
    txt = '%d-%d' % (id, digit)
    cv2.putText(img_test, txt, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (127, 0, 255), 2)

# 把图片一览网格显示并保存
save_path = './images/cv_img_number2_result.jpg'
plotcm.grid_by_list(img_list, title_list, 2, save_path, cell_width=6, cell_height=5.5)
