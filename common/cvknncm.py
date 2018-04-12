# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
OpenCV common api
图像识别相关共通函数
"""

import cv2
import glob as gb
import math
import numpy as np
import os

from common import filecm
from common import logcm
from common import opencvcm

def get_hand_digits_knn():
    """
    取得训练好的手写数字识别的KNN对象，如果有缓存文件，优先读取缓存。
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
                cell_img2 = resize_by_max_contours(cell_img, 20, 20, 1, 1)
                # if j == 0:
                #    cv2.imwrite('%s/digits_cell_%d_%d.jpg' % (path, i, j), cell_img2)
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


def get_print_number_knn():
    """
    取得训练好的打印数字识别的KNN对象，如果有缓存文件，优先读取缓存。
    @return: KNN对象
    """

    # 缓存路径及文件设定
    path = './cache/cv'
    file_train = 'number_knn_train.npy'
    file_label = 'number_knn_label.npy'
    filecm.makedir(path)

    if filecm.exists(path, file_train):
        # 从缓存文件中加载训练样本和结果
        train = np.load(os.path.join(path, file_train))
        label = np.load(os.path.join(path, file_label))
    else:
        # 从图片中获取训练样本和结果
        # 获取numbers文件夹下所有文件路径
        img_path = gb.glob("./images/numbers/*")
        # 定义并创建临时目录
        tmp_path = './temp/cv/number'
        filecm.makedir(tmp_path)

        label = []
        train = []

        func_key = "get_print_number_knn"
        ## 对每一张图片进行处理
        for file_path in img_path:
            # 文件短名称
            name = filecm.short_name(file_path)
            # 读取图片
            img = cv2.imread(file_path)

            # 颜色空间转换（转换成灰度图）
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            save_tmp(gray, func_key, "gray", tmp_path, name)

            # 高斯模糊
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            save_tmp(blur, func_key, "GaussianBlur", tmp_path, name)

            # 自适应阈值可以看成一种局部性的阈值，通过规定一个区域大小，
            thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
            save_tmp(thresh, func_key, "adaptiveThreshold", tmp_path, name)

            # 查找检测物体的轮廓。
            image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            height, width = img.shape[:2]
            ## 图片第一行和第二行数字
            list1 = []
            list2 = []
            for cnt in contours:
                # 直边界矩形
                [x, y, w, h] = cv2.boundingRect(cnt)

                # 根据轮廓矩形的宽度和高度筛识别出数字所在区域
                if w > 30 and h > (height / 4):
                    ## 按y坐标分行
                    if y < (height / 2):
                        list1.append([x, y, w, h])  ## 第一行
                    else:
                        list2.append([x, y, w, h])  ## 第二行

            ## 按x坐标排序，上面已经按y坐标分行
            list1_sorted = sorted(list1, key=lambda t: t[0])
            list2_sorted = sorted(list2, key=lambda t: t[0])

            for i in range(5):
                [x1, y1, w1, h1] = list1_sorted[i]
                [x2, y2, w2, h2] = list2_sorted[i]
                ## 切割出每一个数字
                number_roi1 = gray[y1:y1 + h1, x1:x1 + w1]  # Cut the img_test to size
                number_roi2 = gray[y2:y2 + h2, x2:x2 + w2]  # Cut the img_test to size

                ## 对图片进行大小统一和预处理
                resized_roi1 = cv2.resize(number_roi1, (20, 40))
                thresh1 = cv2.adaptiveThreshold(resized_roi1, 255, 1, 1, 11, 2)
                resized_roi2 = cv2.resize(number_roi2, (20, 40))
                thresh2 = cv2.adaptiveThreshold(resized_roi2, 255, 1, 1, 11, 2)

                j = i + 6
                if j == 10:
                    j = 0

                # 保存数字图片
                save_tmp(thresh1, func_key, "adaptiveThreshold", tmp_path, name + "-" + str(i + 1))
                save_tmp(thresh2, func_key, "adaptiveThreshold", tmp_path, name + "-" + str(j))

                ## 归一化
                normalized_roi1 = thresh1 / 255.
                normalized_roi2 = thresh2 / 255.

                ## 把图片展开成一行，然后保存到samples
                ## 保存一个图片信息，保存一个对应的标签
                train.append(normalized_roi1.reshape((1, 800)))
                label.append(float(i + 1))
                train.append(normalized_roi2.reshape((1, 800)))
                label.append(j)

        # 训练数据整理为np.array格式
        train = np.array(train).reshape(-1, 800).astype(np.float32)
        label = np.array(label).astype(np.float32)

        # 保存缓存文件
        np.save(os.path.join(path, file_train), train)
        np.save(os.path.join(path, file_label), label)

    # KNN算法
    knn = cv2.ml.KNearest_create()

    # 训练数据
    knn.train(train, cv2.ml.ROW_SAMPLE, label)

    return knn

def find_digit_knn(knn, roi, thresh_value, tmp_path=None, tmp_key=None):
    """
    使用KNN算法，判断感兴趣区域（ROI）中的数字。
    @:param knn KNN对象（已训练过）
    @:param roi 感兴趣区域
    @:param thresh_value 阈值处理的阈值值
    @:param tmp_path 临时目录
    @:param tmp_key 临时关键词
    @return: 结果数字，最终判断用的矩阵
    """

    # 函数名
    func_key = "find_digit_knn"
    opencvcm.save_tmp(roi, func_key, "roi", tmp_path, tmp_key)

    # 阈值处理
    ret, th = cv2.threshold(roi, thresh_value, 255, cv2.THRESH_BINARY)
    opencvcm.save_tmp(th, func_key, "threshold", tmp_path, tmp_key)

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
    opencvcm.save_tmp(resize_th, func_key, "resize", tmp_path, tmp_key)

    # 矩阵展开成一维并转换为浮点数
    out = resize_th.reshape(-1, 400).astype(np.float32)
    # 通过KNN对象查找最符合的数字
    ret, result, neighbours, dist = knn.findNearest(out, k=5)

    return int(result[0][0]), th

