# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
OpenCV common api
图像识别相关共通函数
"""

import cv2
import math
import numpy as np
import os

from common import filecm
from common import datecm


def get_digits_knn():
    """
    取得训练好的数字识别的KNN对象，如果有缓存文件，优先读取缓存。
    @return: KNN对象
    """

    # 缓存路径及文件设定
    path = './cache/cv'
    file_train = 'digits_knn_train.npy'
    file_label = 'digits_knn_label.npy'

    if filecm.exists(path, file_train):
        # 从缓存文件中加载训练样本和结果
        train = np.load(os.path.join(path, file_train))
        label = np.load(os.path.join(path, file_label))
    else:
        # 从图片中获取训练样本和结果
        img = cv2.imread('./images/cv_digits.png')
        # 灰度转换
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 把图片切割为50*100个Cell
        cells = [np.hsplit(row, 100) for row in np.vsplit(gray, 50)]

        # 计算训练数据，对每个Cell，进行reshape处理，
        # 把图片展开成400列，行数不确定
        train = np.array(cells).reshape(-1, 400).astype(np.float32)

        # 每个数字500遍
        label = np.repeat(np.arange(10), 500)

        # 保存缓存文件
        filecm.makedir(path)
        np.save(os.path.join(path, file_train), train)
        np.save(os.path.join(path, file_label), label)

    # KNN算法
    knn = cv2.ml.KNearest_create()

    # 训练数据
    knn.train(train, cv2.ml.ROW_SAMPLE, label)

    return knn


def find_rois(img, thresh_value, min_width=10, min_height=10):
    """
    从图片中获取外边框在指定大小以上的感兴趣区域（ROI）。
    @:param img 图片
    @:param thresh_value 阈值处理的阈值值
    @return: 感兴趣区域列表，边框数据
    """

    img_width = img.shape[0]

    tmp_path = './temp/cv/digits/' + datecm.now_time_str()
    filecm.makedir(tmp_path)

    rois = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(tmp_path + '/find_rois_gray.jpg', gray)

    # 膨胀图像
    dilate = cv2.dilate(gray, None, iterations=2)
    cv2.imwrite(tmp_path + '/find_rois_dilate.jpg', dilate)

    # 腐蚀图像
    erode = cv2.erode(gray, None, iterations=2)
    cv2.imwrite(tmp_path + '/find_rois_erode.jpg', erode)

    # 将两幅图像相减获得边，第一个参数是膨胀后的图像，第二个参数是腐蚀后的图像
    edges = cv2.absdiff(dilate, erode)
    cv2.imwrite(tmp_path + '/find_rois_edges.jpg', edges)

    # Sobel算子:是一种带有方向性的滤波器，
    #   cv2.CV_16S -- Sobel 函数求完导数后会有负值和大于255的值，
    #   而原图像是uint8（8位无符号数据），所以在建立图像时长度不够，会被截断，所以使用16位有符号数据。
    #   dst = cv2.Sobel(src, ddepth, dx, dy[, dst[, ksize[, scale[, delta[, borderType]]]]])
    #   src     - - 原图像
    #   ddepth  - - 图像的深度，-1表示采用的是与原图像相同的深度。目标图像的深度必须大于等于原图像的深度。
    #   dx dy   - - 表示的是示导的阶数，0表示这个方向上没有求导，一般为0，1，2。
    # 【可选参数】
    #   dst     - - 目标图像，与原图像（src）据有相同的尺寸和通道
    #   ksize   - - Sobel算子的大小，必须为1、3、5、7。
    #   scale   - - 缩放导数的比例常数，默认情况下没有伸缩系数
    #   delta   - - 一个可选的增量，将会加到最终的dst中，同样，默认情况下没有额外的值加到dst中
    # borderType - - 判断图像边界的模式。这个参数默认值为cv2.BORDER_DEFAULT。
    x = cv2.Sobel(edges, cv2.CV_16S, 1, 0)
    y = cv2.Sobel(edges, cv2.CV_16S, 0, 1)

    # convertScaleAbs()--转回uint8形式，否则将无法显示图像，而只是一副灰色图像
    # dst = cv2.convertScaleAbs(src[, dst[, alpha[, beta]]])
    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)

    # 组合图像 dst = cv2.addWeighted(src1, alpha, src2, beta, gamma[, dst[, dtype]])
    #   alpha  --  第一幅图片中元素的权重
    #   beta   --  第二个权重
    #   gamma  --  累加到结果上的一个值
    dst = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
    cv2.imwrite(tmp_path + '/find_rois_dst.jpg', dst)

    # 简单阈值
    ret, thresh = cv2.threshold(dst, thresh_value, 255, cv2.THRESH_BINARY)
    cv2.imwrite(tmp_path + '/find_rois_thresh.jpg', thresh)

    # 查找检测物体的轮廓
    im, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        # 取得轮廓的直边界矩形
        x, y, w, h = cv2.boundingRect(c)
        # 判断最小宽度和高度
        if w > min_width and h > min_height:
            rois.append((x, y, w, h))

    # 对区域排序，先上线，再左右。
    sorted_rois = sorted(rois, key=lambda t: t[1] * img_width + t[0])

    return sorted_rois, edges, tmp_path


def find_digit_knn(knn, roi, thresh_value, id, tmp_path):
    """
    使用KNN算法，判断感兴趣区域（ROI）中的数字。
    @:param knn KNN对象（已训练过）
    @:param roi 感兴趣区域
    @:param thresh_value 阈值处理的阈值值
    @:param id 当前图片ID
    @return: 结果数字，最终判断用的矩阵
    """

    # 重新设置为标准的比较尺寸
    resize_roi = cv2.resize(roi, (20, 20))
    cv2.imwrite(tmp_path + '/find_digit_knn_resize-%s.jpg' % str(id), resize_roi)

    # 阈值处理
    ret, th = cv2.threshold(resize_roi, thresh_value, 255, cv2.THRESH_BINARY)
    # th = cv2.adaptiveThreshold(resize_roi, 255, 1, 1, 11, 2)
    cv2.imwrite(tmp_path + '/find_digit_knn_threshold-%s.jpg' % str(id), th)

    # 矩阵展开成一维并转换为浮点数
    out = th.reshape(-1, 400).astype(np.float32)
    # 通过KNN对象查找最符合的数字
    ret, result, neighbours, dist = knn.findNearest(out, k=5)

    return int(result[0][0]), th
