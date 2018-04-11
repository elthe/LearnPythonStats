#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数字图片的训练和识别。
参考代码：https://github.com/LiuXiaolong19920720/opencv-soduko
模块安装：pip install opencv-python
"""

import cv2
import glob as gb
import matplotlib.pyplot as plt
import numpy as np

from common import filecm
from common import opencvcm

# 获取plates文件夹下所有文件路径
img_path = gb.glob("./images/plates/*")
# 定义并创建临时目录
tmp_path = './temp/cv/plate'
filecm.makedir(tmp_path)

img_list = []
# 标题列表
title_list = ['Image', 'Gray', 'Dilation', 'Plate']

## 对每一张图片进行处理
for path in img_path:
    line_list = []
    img = cv2.imread(path)
    line_list.append(img)

    # 转化成灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    line_list.append(gray)

    # 形态学变换的预处理
    dilation = opencvcm.preprocess(gray)
    line_list.append(dilation)

    # 查找车牌区域
    rois = opencvcm.find_rois(dilation, min_area=2000, min_wh_ratio=2, max_wh_ratio=5)
    img_plate = None
    if len(rois) > 0:
        max_roi = opencvcm.get_max_roi(rois)
        (x, y, w, h) = max_roi
        img_plate = img[y:y + h, x:x + w]

    line_list.append(img_plate)
    img_list.append(line_list)

# 多子图绘制
fig, axes = plt.subplots(len(img_path), 4, sharey=False, sharex=False)
# 设置图片尺寸
fig.set_size_inches(10, len(img_path) * 12 // 7)
# 总标题
fig.suptitle('')
# 设置标题(中文字体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

for i in range(len(img_list)):
    for j in range(len(img_list[i])):
        ax = axes[i][j]
        # 显示图片
        ax.imshow(img_list[i][j], 'gray')
        # 显示标题
        ax.set_title(title_list[j])
        # 隐藏坐标轴
        ax.set_xticks([])
        ax.set_yticks([])

# 调整每隔子图之间的距离
plt.tight_layout()
# 保存图片
plt.savefig('./images/cv_img_plate1_result.jpg')
# 显示绘制后的图片
plt.show()
