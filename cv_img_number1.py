#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数字图片的训练和识别。
参考代码：https://github.com/LiuXiaolong19920720/opencv-soduko
模块安装：pip install opencv-python
"""

import glob as gb
import cv2
import numpy as np

from common import filecm
from common import opencvcm
from common import plotcm
from common import logcm

# 获取numbers文件夹下所有文件路径
img_path = gb.glob("./images/numbers/*")
# 定义并创建临时目录
tmp_path = './temp/cv/number'
filecm.makedir(tmp_path)

# 图片列表
img_list = []
# 标题列表
title_list = []

# KNN算法对象（初始化并训练好）
knn = opencvcm.get_print_number_knn()

# 载入测试图片
img_test = cv2.imread('./images/cv_number_test1.jpg')
img_list.append(img_test)
title_list.append('原图+结果')

# 灰度
gray = opencvcm.get_gray(img_test, tmp_path, "", img_list, title_list)

# 阈值处理
thresh = opencvcm.get_thresh(gray, 200, cv2.THRESH_BINARY_INV, tmp_path, "", img_list, title_list)

# 膨胀
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
dilated = cv2.dilate(thresh, kernel)
img_list.append(dilated)
title_list.append('dilate')

# 轮廓提取
image, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# 提取八十一个小方格
boxes = []
for i in range(len(hierarchy[0])):
    if hierarchy[0][i][3] == 0:
        boxes.append(hierarchy[0][i])

height, width = img_test.shape[:2]
box_h = height / 9
box_w = width / 9
number_boxes = []

## 数独初始化为零阵
soduko = np.zeros((9, 9), np.int32)

for j in range(len(boxes)):
    if boxes[j][2] != -1:
        x, y, w, h = cv2.boundingRect(contours[boxes[j][2]])
        number_boxes.append([x, y, w, h])
        # 对提取的数字进行处理
        number_roi = gray[y:y + h, x:x + w]
        # 统一大小
        resized_roi = cv2.resize(number_roi, (20, 40))
        thresh1 = cv2.adaptiveThreshold(resized_roi, 255, 1, 1, 11, 2)

        ## 归一化像素值
        normalized_roi = thresh1 / 255.

        # 展开成一行让knn识别
        sample1 = normalized_roi.reshape((1, 800))
        sample1 = np.array(sample1, np.float32)

        # knn识别
        retval, results, neigh_resp, dists = knn.findNearest(sample1, 1)
        number = int(results.ravel()[0])

        # 绘制边框到图片上
        cv2.rectangle(img_test, (x, y), (x + w, y + h), (153, 153, 0), 2)

        # 识别结果展示
        cv2.putText(img_test, str(number), (x + w + 1, y + h - 20), 3, 2., (255, 0, 0), 2, cv2.LINE_AA)

        ## 求在矩阵中的位置
        soduko[int(y / box_h)][int(x / box_w)] = number

print(soduko)

# 把图片一览网格显示并保存
save_path = './images/cv_img_number1_result.jpg'
plotcm.grid_by_list(img_list, title_list, 2, save_path, cell_width=6, cell_height=5.5)

