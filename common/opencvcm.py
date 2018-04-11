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
from common import logcm


def get_digits_knn():
    """
    取得训练好的数字识别的KNN对象，如果有缓存文件，优先读取缓存。
    @return: KNN对象
    """

    # 缓存路径及文件设定
    path = './cache/cv'
    file_train = 'digits_knn_train.npy'
    file_label = 'digits_knn_label.npy'
    filecm.makedir(path)

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

        train = []
        # 删除图片边界空白
        for i in range(50):
            for j in range(100):
                cell_img = cells[i][j]
                cell_img2 = resize_by_max_contours(cell_img, 50, 20, 20, 1, 1)
                if j == 0:
                    cv2.imwrite('%s/digits_cell_%d_%d.jpg' % (path, i, j), cell_img2)
                # 计算训练数据，对每个Cell，进行reshape处理，
                # 把图片展开成400列，行数不确定
                train.append(cell_img2.reshape((1, 400)))

        # 训练数据整理为np.array格式
        train = np.array(train).reshape(-1, 400).astype(np.float32)
        # 每个数字500遍
        label = np.repeat(np.arange(10), 500)

        # 保存缓存文件
        np.save(os.path.join(path, file_train), train)
        np.save(os.path.join(path, file_label), label)

    # KNN算法
    knn = cv2.ml.KNearest_create()

    # 训练数据
    knn.train(train, cv2.ml.ROW_SAMPLE, label)

    return knn


def resize_by_max_contours(img, target_width, target_height, min_width=10, min_height=10):
    """
    按照图片中最大轮廓，截取图片并按目标大小返回。
    @:param img 图片
    @:param target_width 目标宽度
    @:param target_height 目标高度
    @:param min_width 轮廓最小宽度
    @:param min_height 轮廓最小高度
    @return: 目标大小的图片
    """

    # 查找图片中的轮廓列表
    rois = find_rois(img, min_width, min_height)

    # 取得面积最大的轮廓
    max_roi = get_max_roi(rois)
    if max_roi is None:
        return None

    # 截取最大轮廓图片
    (x, y, w, h) = max_roi
    img_sub = img[y:y + h, x:x + w]

    # 重置为目标尺寸
    img_target = cv2.resize(img_sub, (target_width, target_height), interpolation=cv2.INTER_AREA)

    return img_target


def get_max_roi(rois):
    """
    取得指定区域列表中面积最大的一个。
    @:param rois 区域列表
    @return:
    """

    # 为空判断
    if rois is None or len(rois) == 0:
        logcm.print_info("Rois is None or Empty!")
        return None

    # 计算最大面积
    max_area = 0
    max_roi = rois[0]
    for roi in rois:
        x, y, w, h = roi
        # 面积 = 宽度 * 高度
        area = w * h
        if area > max_area:
            max_area = area
            max_roi = roi
    return max_roi


def get_edges(img, tmp_path, is_color=True):
    """
    从图片中获取边界图片。
    @:param img 图片
    @:param tmp_path 临时目录
    @:param is_color 是否彩色图片
    @return: 边界图片
    """

    # 灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if is_color else img
    cv2.imwrite(tmp_path + '/get_edges_gray.jpg', gray)

    # 膨胀图像
    dilate = cv2.dilate(gray, None, iterations=2)
    cv2.imwrite(tmp_path + '/get_edges_dilate.jpg', dilate)

    # 腐蚀图像
    erode = cv2.erode(gray, None, iterations=2)
    cv2.imwrite(tmp_path + '/get_edges_erode.jpg', erode)

    # 将两幅图像相减获得边，第一个参数是膨胀后的图像，第二个参数是腐蚀后的图像
    edges = cv2.absdiff(dilate, erode)
    cv2.imwrite(tmp_path + '/get_edges_edges.jpg', edges)
    return edges


def get_thresh(img, tmp_path, thresh_value):
    """
    从图片中阈值图片（黑白图）
    @:param img 图片
    @:param tmp_path 临时目录
    @:param thresh_value 阈值处理的阈值值
    @return: 阈值图片
    """

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
    x = cv2.Sobel(img, cv2.CV_16S, 1, 0)
    y = cv2.Sobel(img, cv2.CV_16S, 0, 1)

    # convertScaleAbs()--转回uint8形式，否则将无法显示图像，而只是一副灰色图像
    # dst = cv2.convertScaleAbs(src[, dst[, alpha[, beta]]])
    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)

    # 组合图像 dst = cv2.addWeighted(src1, alpha, src2, beta, gamma[, dst[, dtype]])
    #   alpha  --  第一幅图片中元素的权重
    #   beta   --  第二个权重
    #   gamma  --  累加到结果上的一个值
    dst = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
    cv2.imwrite(tmp_path + '/get_thresh_dst.jpg', dst)

    # 简单阈值
    ret, thresh = cv2.threshold(dst, thresh_value, 255, cv2.THRESH_BINARY)
    cv2.imwrite(tmp_path + '/get_thresh_thresh.jpg', thresh)
    return thresh


def find_rois(img, min_width=20, min_height=20, min_area=None, min_wh_ratio=None, max_wh_ratio=None):
    """
    从图片中获取外边框在指定大小以上的感兴趣区域（ROI）。
    @:param img 图片
    @:param thresh_value 阈值处理的阈值值
    @:param min_width 最小宽度
    @:param min_height 最小高度
    @:param min_area 最小面积
    @:param min_wh_ratio 最小宽高比
    @:param max_wh_ratio 最大宽高比
    @return: 感兴趣区域列表，边框数据
    """

    img_width = img.shape[0]
    rois = []
    # 查找检测物体的轮廓
    im, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:

        # 最小面积限制
        if min_area is not None:
            # 计算该轮廓的面积
            area = cv2.contourArea(c)
            # 面积小的都筛选掉
            if area < min_area:
                continue

        # 取得轮廓的直边界矩形
        x, y, w, h = cv2.boundingRect(c)
        # 判断最小宽度和高度
        if w > min_width and h > min_height:
            rois.append((x, y, w, h))

        # 最小和最大宽高比限制
        ratio = float(w) / float(h)
        if max_wh_ratio is not None:
            if ratio > max_wh_ratio:
                continue
        if min_wh_ratio is not None:
            if ratio < min_wh_ratio:
                continue

    # 对区域排序，先上线，再左右。
    sorted_rois = sorted(rois, key=lambda t: t[1] * img_width + t[0])

    return sorted_rois

def find_digit_knn(knn, roi, thresh_value, id, tmp_path):
    """
    使用KNN算法，判断感兴趣区域（ROI）中的数字。
    @:param knn KNN对象（已训练过）
    @:param roi 感兴趣区域
    @:param thresh_value 阈值处理的阈值值
    @:param id 当前图片ID
    @return: 结果数字，最终判断用的矩阵
    """

    cv2.imwrite(tmp_path + '/find_digit_knn-%s-roi.jpg' % str(id), roi)

    # 阈值处理
    ret, th = cv2.threshold(roi, thresh_value, 255, cv2.THRESH_BINARY)
    cv2.imwrite(tmp_path + '/find_digit_knn-%s-threshold.jpg' % str(id), th)

    # 重新设置为标准的比较尺寸
    # interpolation - 插值方法。共有5种：
    #   １）INTER_NEAREST - 最近邻插值法
    #   ２）INTER_LINEAR  - 双线性插值法（默认）
    #   ３）INTER_AREA    - 基于局部像素的重采样（resampling using pixel area relation）。
    #       对于图像抽取（image decimation）来说，这可能是一个更好的方法。
    #       但如果是放大图像时，它和最近邻法的效果类似。
    #   ４）INTER_CUBIC   - 基于4x4像素邻域的3次插值法
    #   ５）INTER_LANCZOS4- 基于8x8像素邻域的Lanczos插值
    resize_th = cv2.resize(th, (20, 20), interpolation=cv2.INTER_AREA)
    cv2.imwrite(tmp_path + '/find_digit_knn-%s_resize.jpg' % str(id), resize_th)

    # 矩阵展开成一维并转换为浮点数
    out = resize_th.reshape(-1, 400).astype(np.float32)
    # 通过KNN对象查找最符合的数字
    ret, result, neighbours, dist = knn.findNearest(out, k=5)

    return int(result[0][0]), th


def preprocess(gray):
    """
    图片预处理。
    @:param gray 灰度图
    @return: 预处理后的图
    """

    # # 直方图均衡化
    # equ = cv2.equalizeHist(gray)
    # 高斯平滑
    gaussian = cv2.GaussianBlur(gray, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
    # 中值滤波
    median = cv2.medianBlur(gaussian, 5)
    # Sobel算子，X方向求梯度
    sobel = cv2.Sobel(median, cv2.CV_8U, 1, 0, ksize=3)
    # 二值化
    ret, binary = cv2.threshold(sobel, 170, 255, cv2.THRESH_BINARY)
    # 膨胀和腐蚀操作的核函数
    element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
    element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 7))
    # 膨胀一次，让轮廓突出
    dilation = cv2.dilate(binary, element2, iterations=1)
    # 腐蚀一次，去掉细节
    erosion = cv2.erode(dilation, element1, iterations=1)
    # 再次膨胀，让轮廓明显一些
    dilation2 = cv2.dilate(erosion, element2, iterations=3)

    return dilation2
