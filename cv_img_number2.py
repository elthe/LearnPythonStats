#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数字图片的训练和识别。
参考代码：https://github.com/LiuXiaolong19920720/opencv-soduko
模块安装：pip install opencv-python
"""

import cv2
import numpy as np

from common import filecm
from common import opencvcm


knn = opencvcm.get_digits_knn()
frame = cv2.imread('./images/cv_number_test2.jpg')
rois, edges, tmp_path = opencvcm.find_rois(frame, 50)
digits = []
id = 0
for r in rois:
    x, y, w, h = r
    id += 1
    digit, th = opencvcm.find_digit_knn(knn, edges[y:y + h, x:x + w], 21, id, tmp_path)
    digits.append(cv2.resize(th, (20, 20)))
    cv2.rectangle(frame, (x, y), (x + w, y + h), (153, 153, 0), 2)
    txt = '%d-%d' % (id, digit)
    cv2.putText(frame, txt, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (127, 0, 255), 2)

newEdges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

# 水平拼接
newFrame = np.hstack((frame, newEdges))
cv2.imshow('frame', newFrame)
cv2.imwrite('./images/cv_img_number2_result.jpg', newFrame)

# 垂直拼接
output = np.vstack(digits)
cv2.imshow('digits', output)
cv2.waitKey(0)

cv2.destroyAllWindows()
