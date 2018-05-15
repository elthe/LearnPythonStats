# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Image Operation common api
图片处理相关共通函数
"""

import cv2
import numpy as np


def change_saturation(im_bgr, value):
    """
    调整图片饱和度
    :param im_bgr: BGR图片
    :param value: 设定值（-50～50）
    @return: 调整后的BGR图片
    """

    im_hls = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2HLS)
    if value > 2:
        im_hls[:, :, 2] = np.log(im_hls[:, :, 2] / 255 * (value - 1) + 1) / np.log(value + 1) * 255
    if value < 0:
        im_hls[:, :, 2] = np.uint8(im_hls[:, :, 2] / np.log(- value + np.e))
    im_bgr_new = cv2.cvtColor(im_hls, cv2.COLOR_HLS2BGR)
    return im_bgr_new


def change_darker(im_bgr, value):
    """
    调整图片明度
    :param im_bgr: BGR图片
    :param value: 设定值（-100～100）
    @return: 调整后的BGR图片
    """

    img_hsv = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2HLS)
    if value > 3:
        img_hsv[:, :, 1] = np.log(img_hsv[:, :, 1] / 255 * (value - 1) + 1) / np.log(value + 1) * 255
    if value < 0:
        img_hsv[:, :, 1] = np.uint8(img_hsv[:, :, 1] / np.log(- value + np.e))
    im_bgr_new = cv2.cvtColor(img_hsv, cv2.COLOR_HLS2BGR)
    return im_bgr_new


def detect_face(im_bgr):
    """
    人脸识别
    :param im_bgr: BGR图片
    @return: 人脸信息
    """
    face_cascade = cv2.CascadeClassifier('./data/ui/haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return faces


def detect_skin(im_bgr):
    """
    皮肤识别
    :param im_bgr: BGR图片
    @return: 皮肤信息
    """
    rows, cols, channels = im_bgr.shape
    im_skin = np.zeros(im_bgr.shape)
    for r in range(rows):
        for c in range(cols):
            B = im_bgr.item(r, c, 0)
            G = im_bgr.item(r, c, 1)
            R = im_bgr.item(r, c, 2)
            if (abs(R - G) > 15) and (R > G) and (R > B):
                if (R > 95) and (G > 40) and (B > 20) and (max(R, G, B) - min(R, G, B) > 15):
                    im_skin[r, c] = (1, 1, 1)
                elif (R > 220) and (G > 210) and (B > 170):
                    im_skin[r, c] = (1, 1, 1)
    return im_skin


def dermabrasion(im_bgr, im_skin, value1=3, value2=2):
    """
    皮肤磨皮处理
    :param im_bgr: BGR图片
    :param im_skin: 皮肤信息
    :param value1: 精细度（0～10）
    :param value2: 程度（0～10）
    @return: 处理后BGR图片
    """

    if value1 == 0 and value2 == 0:
        return 0
    if value2 == 0:
        value2 = 2
    if value1 == 0:
        value1 = 3

    dx = value1 * 5
    fc = value1 * 12.5
    p = 50
    temp1 = cv2.bilateralFilter(im_bgr, dx, fc, fc)
    temp2 = (temp1 - im_bgr + 128)
    temp3 = cv2.GaussianBlur(temp2, (2 * value2 - 1, 2 * value2 - 1), 0, 0)
    temp4 = im_bgr + 2 * temp3 - 255
    dst = np.uint8(im_bgr * ((100 - p) / 100) + temp4 * (p / 100))

    imgskin_c = np.uint8(-(im_skin - 1))

    im_new = np.uint8(dst * im_skin + im_bgr * imgskin_c)
    return im_new


def whitening_skin(im_bgr, im_skin, value=30):
    """
    美白算法(皮肤识别)
    :param im_bgr: BGR图片
    :param im_skin: 皮肤信息
    :param value: 程度（0～50）
    @return: 处理后BGR图片
    """

    im_new = np.zeros(im_bgr.shape, dtype='uint8')
    im_new = im_bgr.copy()
    midtones_add = np.zeros(256)

    for i in range(256):
        midtones_add[i] = 0.667 * (1 - ((i - 127.0) / 127) * ((i - 127.0) / 127))

    lookup = np.zeros(256, dtype="uint8")

    for i in range(256):
        red = i
        red += np.uint8(value * midtones_add[red])
        red = max(0, min(0xff, red))
        lookup[i] = np.uint8(red)

    rows, cols, channals = im_bgr.shape
    for r in range(rows):
        for c in range(cols):

            if im_skin[r, c, 0] == 1:
                im_new[r, c, 0] = lookup[im_new[r, c, 0]]
                im_new[r, c, 1] = lookup[im_new[r, c, 1]]
                im_new[r, c, 2] = lookup[im_new[r, c, 2]]
    return im_new


def whitening_face(im_bgr, faces, value=30):
    """
    美白算法(人脸识别)
    :param im_bgr: BGR图片
    :param faces: 人脸信息
    :param value: 程度（0～50）
    @return: 处理后BGR图片
    """

    im_new = np.zeros(im_bgr.shape, dtype='uint8')
    im_new = im_bgr.copy()
    midtones_add = np.zeros(256)

    for i in range(256):
        midtones_add[i] = 0.667 * (1 - ((i - 127.0) / 127) * ((i - 127.0) / 127))

    lookup = np.zeros(256, dtype="uint8")

    for i in range(256):
        red = i
        red += np.uint8(value * midtones_add[red])
        red = max(0, min(0xff, red))
        lookup[i] = np.uint8(red)

    if faces == ():
        rows, cols, channels = im_bgr.shape
        for r in range(rows):
            for c in range(cols):
                im_new[r, c, 0] = lookup[im_new[r, c, 0]]
                im_new[r, c, 1] = lookup[im_new[r, c, 1]]
                im_new[r, c, 2] = lookup[im_new[r, c, 2]]

    else:
        x, y, w, h = faces[0]
        rows, cols, channels = im_bgr.shape
        x = max(x - (w * np.sqrt(2) - w) / 2, 0)
        y = max(y - (h * np.sqrt(2) - h) / 2, 0)
        w = w * np.sqrt(2)
        h = h * np.sqrt(2)
        rows = min(rows, y + h)
        cols = min(cols, x + w)
        for r in range(int(y), int(rows)):
            for c in range(int(x), int(cols)):
                im_new[r, c, 0] = lookup[im_new[r, c, 0]]
                im_new[r, c, 1] = lookup[im_new[r, c, 1]]
                im_new[r, c, 2] = lookup[im_new[r, c, 2]]

        processWidth = int(max(min(rows - y, cols - 1) / 8, 2))
        for i in range(1, processWidth):
            alpha = (i - 1) / processWidth
            for r in range(int(y), int(rows)):
                im_new[r, int(x) + i - 1] = np.uint8(
                    im_new[r, int(x) + i - 1] * alpha + im_bgr[r, int(x) + i - 1] * (1 - alpha))
                im_new[r, int(cols) - i] = np.uint8(
                    im_new[r, int(cols) - i] * alpha + im_bgr[r, int(cols) - i] * (1 - alpha))
            for c in range(int(x) + processWidth, int(cols) - processWidth):
                im_new[int(y) + i - 1, c] = np.uint8(
                    im_new[int(y) + i - 1, c] * alpha + im_bgr[int(y) + i - 1, c] * (1 - alpha))
                im_new[int(rows) - i, c] = np.uint8(
                    im_new[int(rows) - i, c] * alpha + im_bgr[int(rows) - i, c] * (1 - alpha))
    return im_new


def gamma_trans(im_bgr, value):
    """
    Gamma矫正
    :param im_bgr: BGR图片
    :param value: 设定值（-10～10）
    @return: 处理后BGR图片
    """
    gamma = (value + 10) / 10
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    im_new = cv2.LUT(im_bgr, gamma_table)
    return im_new


def reminiscene(im_bgr, value):
    """
    怀旧滤镜
    :param im_bgr: BGR图片
    :param value: 设定值（0～1）
    @return: 处理后BGR图片
    """

    if value == 0:
        return im_bgr

    rows, cols, channals = im_bgr.shape
    im_new = im_bgr.copy()
    for r in range(rows):
        for c in range(cols):
            B = im_new.item(r, c, 0)
            G = im_new.item(r, c, 1)
            R = im_new.item(r, c, 2)
            im_new[r, c, 0] = np.uint8(min(max(0.272 * R + 0.534 * G + 0.131 * B, 0), 255))
            im_new[r, c, 1] = np.uint8(min(max(0.349 * R + 0.686 * G + 0.168 * B, 0), 255))
            im_new[r, c, 2] = np.uint8(min(max(0.393 * R + 0.769 * G + 0.189 * B, 0), 255))
    return im_new


def woodcut(im_bgr, value):
    """
    木刻滤镜
    :param im_bgr: BGR图片
    :param value: 设定值（0～50）
    @return: 处理后BGR图片
    """
    if im_bgr is None:
        return 0
    if value == 0:
        return im_bgr
    im_gray = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2GRAY)
    value = 70 + value
    rows, cols = im_gray.shape
    for r in range(rows):
        for c in range(cols):
            if im_gray[r, c] > value:
                im_gray[r, c] = 255
            else:
                im_gray[r, c] = 0
    im_new = cv2.cvtColor(im_gray, cv2.COLOR_GRAY2BGR)
    return im_new


def im_filter(im_bgr, filter_name, value):
    """
    使用指定滤镜对图片进行处理
    :param im_bgr: BGR图片
    :param filter_name: 滤镜名
    :param value: 设定值（0～10）
    :param gray: 取得灰度图
    @return: 处理后BGR图片
    """
    if im_bgr is None:
        return 0
    if value == 0:
        return im_bgr
    value = value * 0.05

    # 铅笔灰度滤镜
    if filter_name == "pencil_gray":
        im_gray, im_color = cv2.pencilSketch(im_bgr, sigma_s=50, sigma_r=value, shade_factor=0.04)
        im_new = cv2.cvtColor(im_gray, cv2.COLOR_GRAY2BGR)

    # 铅笔彩色滤镜
    if filter_name == "pencil_color":
        im_gray, im_new = cv2.pencilSketch(im_bgr, sigma_s=50, sigma_r=value, shade_factor=0.04)

    # 风格化滤镜
    if filter_name == "stylize":
        im_new = cv2.stylization(im_bgr, sigma_s=50, sigma_r=value)

    # 细节增强滤镜
    if filter_name == "detail_enhance":
        im_new = cv2.detailEnhance(im_bgr, sigma_s=50, sigma_r=value)

    # 边缘保持
    if filter_name == "edge_preserve":
        im_new = cv2.edgePreservingFilter(im_bgr, flags=1, sigma_s=50, sigma_r=value)

    return im_new


def mark_face(im_bgr, faces=None, bdcolor=(255, 0, 0), border=1):
    """
    标记人脸
    :param im_bgr: BGR图片
    :param faces: 人脸信息
    :param bdcolor: 边框色
    :param border: 边框宽度
    @return: 处理后BGR图片
    """
    if im_bgr is None:
        return None
    # 获取人脸信息
    if faces is None:
        faces = detect_face(im_bgr)
    im_new = im_bgr.copy()
    for (x, y, w, h) in faces:
        im_new = cv2.rectangle(im_new, (x, y), (x + w, y + h), bdcolor, border)
    return im_new
