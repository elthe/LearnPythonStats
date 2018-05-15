# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Image Filter common api
图片滤镜相关共通函数
"""

import numpy as np

support_filters = [
    'Naive',  # Naive Filter  原图滤波（相当于无变化）
    'Sharpness_Center',  # Sharpness_Center Filter  中心锐化 滤波
    'Sharpness_Edge',  # Sharpness_Edge Filter  边缘锐化 滤波
    'Edge_Detection_360_degree',  # Edge_Detection_360° Filter  360°边缘检测 滤波
    'Edge_Detection_45_degree',  # Edge_Detection_45° Filter  45°边缘检测 滤波
    'Embossing_45_degree',  # Embossing_45° Filter  45°浮雕 滤波
    'Embossing_Asymmetric',  # Embossing_Asymmetric Filter  非对称浮雕 滤波
    'Averaging_Blur',  # Averaging_Blur Filter  均值模糊 滤波
    'Completed_Blur',  # Completed_Blur Filter  完全模糊 滤波
    'Motion_Blur',  # Motion_Blur Filter  运动模糊 滤波
    'Gaussian_Blur',  # Gaussian_Blur Filter  高斯模糊 滤波
    'DIY'  # DIY Filter  自定义 滤波
]


def exist_filter(filter_name):
    """
    是否存在滤镜
    :param filter_name 滤镜名
    :return 是否存在
    """
    return filter_name in support_filters

class Filter:
    def __init__(self, filter_name):
        """
        Choose which filter to be returned
        根据用户指定的 滤波器名称，挑选对应的 滤波器配置
        """
        if filter_name == 'Naive':
            filter_0, filter_1, filter_2 = Naive_Filter()
        elif filter_name == 'Sharpness_Center':
            filter_0, filter_1, filter_2 = Sharpness_Center_Filter()
        elif filter_name == 'Sharpness_Edge':
            filter_0, filter_1, filter_2 = Sharpness_Edge_Filter()
        elif filter_name == 'Edge_Detection_360_degree':
            filter_0, filter_1, filter_2 = Edge_Detection_360_degree_Filter()
        elif filter_name == 'Edge_Detection_45_degree':
            filter_0, filter_1, filter_2 = Edge_Detection_45_degree_Filter()
        elif filter_name == 'Embossing_45_degree':
            filter_0, filter_1, filter_2 = Embossing_45_degree_Filter()
        elif filter_name == 'Embossing_Asymmetric':
            filter_0, filter_1, filter_2 = Embossing_Asymmetric_Filter()
        elif filter_name == 'Averaging_Blur':
            filter_0, filter_1, filter_2 = Averaging_Blur_Filter()
        elif filter_name == 'Completed_Blur':
            filter_0, filter_1, filter_2 = Completed_Blur_Filter()
        elif filter_name == 'Motion_Blur':
            filter_0, filter_1, filter_2 = Motion_Blur_Filter()
        elif filter_name == 'Gaussian_Blur':
            filter_0, filter_1, filter_2 = Gaussian_Blur_Filter()
        elif filter_name == 'DIY':
            filter_0, filter_1, filter_2 = DIY_Filter()
        else:
            print("\n No such Filter !")
            exit(0)
            filter_0, filter_1, filter_2 = No_Exist_Filter()

        self.filter_name = filter_name
        self.filters = [filter_0, filter_1, filter_2]

    def do_filter(self, im_bgr):
        """
        执行滤镜
        :param im_bgr 要处理的BGR图片
        :return 处理后的BGR图片
        """
        h, w, c = im_bgr.shape
        assert c == 3, "Error! Please use the picture of 3 color channels."

        im_new = np.zeros((h, w, c), dtype=np.float)
        for i in range(1, h - 1, 1):
            for j in range(1, w - 1, 1):
                for k in range(3):
                    im_new[i][j][k] = self.conv(im_bgr, self.filters[k], i, j)
        return im_new

    def conv(self, image, filter, image_center_x, image_center_y):
        """
        卷积处理
        :param image 要处理的BGR图片
        :param filter 滤镜
        :param image_center_x X中间点
        :param image_center_y Y中间点
        :return 卷积值
        """
        size = 3
        radius = int((size - 1) / 2)
        view = np.zeros((size, size, 3), dtype=np.float)
        for i in range(size):
            for j in range(size):
                for z in range(3):
                    view[i][j][z] = image[image_center_x - radius + i][image_center_y - radius + j][z] * filter[i][j][z]
        return np.sum(view)


def Naive_Filter():
    """
    Naive Filter
    原图 滤波
    :return:
    """
    filter_0 = np.array([[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, 0], [0, 0, 0]]],
                        dtype=np.int16)
    filter_1 = np.array([[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, 0], [0, 0, 0]]],
                        dtype=np.int16)
    filter_2 = np.array([[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, 1], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, 0], [0, 0, 0]]],
                        dtype=np.int16)
    return filter_0, filter_1, filter_2


def Sharpness_Center_Filter():
    """
    Sharpness_Center Filter
    中心锐化 滤波
    :return:
    """
    filter_0 = np.array([[[-1, 0, 0], [-1, 0, 0], [-1, 0, 0]],
                         [[-1, 0, 0], [9, 0, 0], [-1, 0, 0]],
                         [[-1, 0, 0], [-1, 0, 0], [-1, 0, 0]]],
                        dtype=np.int16)
    filter_1 = np.array([[[0, -1, 0], [0, -1, 0], [0, -1, 0]],
                         [[0, -1, 0], [0, 9, 0], [0, -1, 0]],
                         [[0, -1, 0], [0, -1, 0], [0, -1, 0]]],
                        dtype=np.int16)
    filter_2 = np.array([[[0, 0, -1], [0, 0, -1], [0, 0, -1]],
                         [[0, 0, -1], [0, 0, 9], [0, 0, -1]],
                         [[0, 0, -1], [0, 0, -1], [0, 0, -1]]],
                        dtype=np.int16)
    return filter_0, filter_1, filter_2


def Sharpness_Edge_Filter():
    """
    Sharpness_Edge Filter
    边缘锐化 滤波
    :return:
    """

    filter_0 = np.array([[[1, 0, 0], [1, 0, 0], [1, 0, 0]],
                         [[1, 0, 0], [-7, 0, 0], [1, 0, 0]],
                         [[1, 0, 0], [1, 0, 0], [1, 0, 0]]],
                        dtype=np.int16)
    filter_1 = np.array([[[0, 1, 0], [0, 1, 0], [0, 1, 0]],
                         [[0, 1, 0], [0, -7, 0], [0, 1, 0]],
                         [[0, 1, 0], [0, 1, 0], [0, 1, 0]]],
                        dtype=np.int16)
    filter_2 = np.array([[[0, 0, 1], [0, 0, 1], [0, 0, 1]],
                         [[0, 0, 1], [0, 0, -7], [0, 0, 1]],
                         [[0, 0, 1], [0, 0, 1], [0, 0, 1]]],
                        dtype=np.int16)
    return filter_0, filter_1, filter_2


def Edge_Detection_360_degree_Filter():
    """
    Edge_Detection_360° Filter
    360°边缘检测 滤波
    :return:
    """

    filter_0 = np.array([[[-1, 0, 0], [-1, 0, 0], [-1, 0, 0]],
                         [[-1, 0, 0], [8, 0, 0], [-1, 0, 0]],
                         [[-1, 0, 0], [-1, 0, 0], [-1, 0, 0]]],
                        dtype=np.int16)
    filter_1 = np.array([[[0, -1, 0], [0, -1, 0], [0, -1, 0]],
                         [[0, -1, 0], [0, 8, 0], [0, -1, 0]],
                         [[0, -1, 0], [0, -1, 0], [0, -1, 0]]],
                        dtype=np.int16)
    filter_2 = np.array([[[0, 0, -1], [0, 0, -1], [0, 0, -1]],
                         [[0, 0, -1], [0, 0, 8], [0, 0, -1]],
                         [[0, 0, -1], [0, 0, -1], [0, 0, -1]]],
                        dtype=np.int16)
    return filter_0, filter_1, filter_2


def Edge_Detection_45_degree_Filter():
    """
    Edge_Detection_45°
    Filter  45°边缘检测 滤波
    :return:
    """
    filter_0 = np.array([[[-1, 0, 0], [0, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [2, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, 0], [-1, 0, 0]]],
                        dtype=np.int16)
    filter_1 = np.array([[[0, -1, 0], [0, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, 2, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, 0], [0, -1, 0]]],
                        dtype=np.int16)
    filter_2 = np.array([[[0, 0, -1], [0, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, 2], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, 0], [0, 0, -1]]],
                        dtype=np.int16)
    return filter_0, filter_1, filter_2


def Embossing_45_degree_Filter():
    """
    Embossing_45° Filter
    45°浮雕 滤波
    :return:
    """
    filter_0 = np.array([[[-1, 0, 0], [-1, 0, 0], [0, 0, 0]],
                         [[-1, 0, 0], [1, 0, 0], [1, 0, 0]],
                         [[0, 0, 0], [1, 0, 0], [1, 0, 0]]],
                        dtype=np.int16)
    filter_1 = np.array([[[0, -1, 0], [0, -1, 0], [0, 0, 0]],
                         [[0, -1, 0], [0, 1, 0], [0, 1, 0]],
                         [[0, 0, 0], [0, 1, 0], [0, 1, 0]]],
                        dtype=np.int16)
    filter_2 = np.array([[[0, 0, -1], [0, 0, -1], [0, 0, 0]],
                         [[0, 0, -1], [0, 0, 1], [0, 0, 1]],
                         [[0, 0, 0], [0, 0, 1], [0, 0, 1]]],
                        dtype=np.int16)
    return filter_0, filter_1, filter_2


def Embossing_Asymmetric_Filter():
    """
    Embossing_Asymmetric Filter
    非对称浮雕 滤波
    :return:
    """

    filter_0 = np.array([[[2, 0, 0], [0, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [-1, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, 0], [-1, 0, 0]]],
                        dtype=np.int16)
    filter_1 = np.array([[[0, 2, 0], [0, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, -1, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, 0], [0, -1, 0]]],
                        dtype=np.int16)
    filter_2 = np.array([[[0, 0, 2], [0, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, -1], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, 0], [0, 0, -1]]],
                        dtype=np.int16)
    return filter_0, filter_1, filter_2


def Averaging_Blur_Filter():
    """
    Averaging_Blur Filter  均值模糊 滤波
    :return:
    """

    filter_0 = np.array([[[0, 0, 0], [0.25, 0, 0], [0, 0, 0]],
                         [[0.25, 0, 0], [0, 0, 0], [0.25, 0, 0]],
                         [[0, 0, 0], [0.25, 0, 0], [0, 0, 0]]],
                        dtype=np.float)
    filter_1 = np.array([[[0, 0, 0], [0, 0.25, 0], [0, 0, 0]],
                         [[0, 0.25, 0], [0, 0, 0], [0, 0.25, 0]],
                         [[0, 0, 0], [0, 0.25, 0], [0, 0, 0]]],
                        dtype=np.float)
    filter_2 = np.array([[[0, 0, 0], [0, 0, 0.25], [0, 0, 0]],
                         [[0, 0, 0.25], [0, 0, 0], [0, 0, 0.25]],
                         [[0, 0, 0], [0, 0, 0.25], [0, 0, 0]]],
                        dtype=np.float)
    return filter_0, filter_1, filter_2


def Completed_Blur_Filter():
    """
    Completed_Blur Filter  完全模糊 滤波
    :return:
    """

    filter_0 = np.array([[[1.0 / 9, 0, 0], [1.0 / 9, 0, 0], [1.0 / 9, 0, 0]],
                         [[1.0 / 9, 0, 0], [1.0 / 9, 0, 0], [1.0 / 9, 0, 0]],
                         [[1.0 / 9, 0, 0], [1.0 / 9, 0, 0], [1.0 / 9, 0, 0]]],
                        dtype=np.float)
    filter_1 = np.array([[[0, 1.0 / 9, 0], [0, 1.0 / 9, 0], [0, 1.0 / 9, 0]],
                         [[0, 1.0 / 9, 0], [0, 1.0 / 9, 0], [0, 1.0 / 9, 0]],
                         [[0, 1.0 / 9, 0], [0, 1.0 / 9, 0], [0, 1.0 / 9, 0]]],
                        dtype=np.float)
    filter_2 = np.array([[[0, 0, 1.0 / 9], [0, 0, 1.0 / 9], [0, 0, 1.0 / 9]],
                         [[0, 0, 1.0 / 9], [0, 0, 1.0 / 9], [0, 0, 1.0 / 9]],
                         [[0, 0, 1.0 / 9], [0, 0, 1.0 / 9], [0, 0, 1.0 / 9]]],
                        dtype=np.float)
    return filter_0, filter_1, filter_2


def Motion_Blur_Filter():
    """
    Motion_Blur Filter  运动模糊 滤波
    :return:
    """

    filter_0 = np.array([[[1, 0, 0], [0, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, 0], [1, 0, 0]]],
                        dtype=np.int16)
    filter_1 = np.array([[[0, 1, 0], [0, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, 0], [0, 1, 0]]],
                        dtype=np.int16)
    filter_2 = np.array([[[0, 0, 1], [0, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, 1], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, 0], [0, 0, 1]]],
                        dtype=np.int16)
    return filter_0, filter_1, filter_2


def Gaussian_Blur_Filter():
    """
    Gaussian_Blur Filter  高斯模糊 滤波
    :return:
    """

    filter_0 = np.array([[[1.0 / 36, 0, 0], [4.0 / 36, 0, 0], [1.0 / 36, 0, 0]],
                         [[4.0 / 36, 0, 0], [16.0 / 36, 0, 0], [4.0 / 36, 0, 0]],
                         [[1.0 / 36, 0, 0], [4.0 / 36, 0, 0], [1.0 / 36, 0, 0]]],
                        dtype=np.float)
    filter_1 = np.array([[[0, 1.0 / 36, 0], [0, 4.0 / 36, 0], [0, 1.0 / 36, 0]],
                         [[0, 4.0 / 36, 0], [0, 16.0 / 36, 0], [0, 4.0 / 36, 0]],
                         [[0, 1.0 / 36, 0], [0, 4.0 / 36, 0], [0, 1.0 / 36, 0]]],
                        dtype=np.float)
    filter_2 = np.array([[[0, 0, 1.0 / 36], [0, 0, 4.0 / 36], [0, 0, 1.0 / 36]],
                         [[0, 0, 4.0 / 36], [0, 0, 16.0 / 36], [0, 0, 4.0 / 36]],
                         [[0, 0, 1.0 / 36], [0, 0, 4.0 / 36], [0, 0, 1.0 / 36]]],
                        dtype=np.float)
    return filter_0, filter_1, filter_2


def DIY_Filter():
    """
    Design a filter yourself  自己设计一个滤波器
    :return:
    """

    filter_0 = np.array([[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, 0], [0, 0, 0]]],
                        dtype=np.int16)
    filter_1 = np.array([[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, 0], [0, 0, 0]]],
                        dtype=np.int16)
    filter_2 = np.array([[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, 1], [0, 0, 0]],
                         [[0, 0, 0], [0, 0, 0], [0, 0, 0]]],
                        dtype=np.int16)
    return filter_0, filter_1, filter_2


def No_Exist_Filter():
    """
    When filter name doesn't exist  当滤波器不存在时
    :return:
    """

    filter_0 = np.zeros((3, 3, 3), dtype=np.float)
    filter_1 = np.zeros((3, 3, 3), dtype=np.float)
    filter_2 = np.zeros((3, 3, 3), dtype=np.float)
    return filter_0, filter_1, filter_2
