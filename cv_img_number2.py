#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数字图片的训练和识别。
"""

import cv2
import numpy as np

from common import filecm
from common import opencvcm
from common import datecm

# 临时目录
tmp_path = './temp/cv/digits/' + datecm.now_time_str()
filecm.makedir(tmp_path)

# KNN算法对象（初始化并训练好）
knn = opencvcm.get_digits_knn()
# 载入测试图片
img_test = cv2.imread('./images/cv_number_test2.jpg')

# 读取图片边界
edges = opencvcm.get_edges(img_test, tmp_path)
# 阈值处理
thresh = opencvcm.get_thresh(edges, tmp_path, 21)
# 查找兴趣点区域
rois = opencvcm.find_rois(thresh)
digits = []
id = 0
for roi in rois:
    (x, y, w, h) = roi
    id += 1
    # 查询兴趣区域对应的数字
    digit, th = opencvcm.find_digit_knn(knn, edges[y:y + h, x:x + w], 21, id, tmp_path)
    digits.append(cv2.resize(th, (20, 20)))

    # 绘制边框到图片上
    cv2.rectangle(img_test, (x, y), (x + w, y + h), (153, 153, 0), 2)

    # 把ID和结果文字输出到图片上
    txt = '%d-%d' % (id, digit)
    cv2.putText(img_test, txt, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (127, 0, 255), 2)

# 边界图灰度转彩图
newEdges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

# 水平拼接
newFrame = np.hstack((img_test, newEdges))
cv2.imshow('img_test', newFrame)
cv2.imwrite('./images/cv_img_number2_result.jpg', newFrame)

# 垂直拼接
output = np.vstack(digits)
cv2.imshow('digits', output)
cv2.waitKey(0)

cv2.destroyAllWindows()
