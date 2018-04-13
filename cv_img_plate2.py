import cv2
import glob as gb
import numpy as np
import sys
import os
import json

from numpy.linalg import norm

from common import cvsvmcm
from common import filecm
from common import logcm
from common import plotcm

# SVM模型
svm = cvsvmcm.get_car_plate_svm()

# 获取plates文件夹下所有文件路径
img_path = gb.glob("./images/plates/*")
# 定义并创建临时目录
tmp_path = './temp/cv/plate'
filecm.makedir(tmp_path)

# 图片矩阵
img_matrix = []
# 标题矩阵
title_matrix = []

# 对每一张图片进行处理
for path in img_path:
    img_list = []
    title_list = []

    img = cv2.imread(path)
    img_list.append(img)
    filename = filecm.short_name(path)
    title_list.append('原图-%s' % filename)

    r, roi, color = cvsvmcm.predict(svm, img, tmp_path, filename, img_list, title_list)
    logcm.print_info("%s --> %s" % (path, str(r)))

    img_list.append(roi)
    txt = "".join(r)
    title_list.append('%s车牌-%s' % (color, txt))

    img_matrix.append(img_list)
    title_matrix.append(title_list)

# 把图片一览网格显示并保存
save_path = './images/cv_img_plate2_result.jpg'
plotcm.grid_by_matrix(img_matrix, title_matrix, 5, save_path, cell_width=2.5, cell_height=2)
