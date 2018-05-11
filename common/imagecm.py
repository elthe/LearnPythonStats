# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Image common api
图片相关共通函数
"""

import math
from PIL import Image
from common import logcm


def get_im(img):
    """
    根据图片文件路径或图片
    @param img: 图片或路径
    @return: 图片对象
    """
    # 取得图片
    im = Image.open(img) if isinstance(img, str) else img
    return im


def get_size(img):
    """
    根据图片取得图片尺寸
    @param img: 图片或路径
    @return: 图片尺寸
    """

    im = get_im(img)
    return im.size


def is_landscape(img):
    """
    根据图片文件路径判断是否横版图片
    @param img_path: 图片或路径
    @return: 是否横版图片
    """

    # 图片尺寸
    (width, height) = get_im(img).size
    # 如果宽度大于高度，则为横版图片
    return width > height


def resize(img, dst_width, dst_height, save_path=None, keep_ratio=True):
    """
    把图片对象压缩成目标大小，可以保持比例。
    @param img: 图片或路径
    @param dst_width: 目标宽度
    @param dst_height: 目标高度
    @param save_path: 保存路径
    @param keep_ratio: 保持比例
    @return: 处理后的图片对象
    """

    # 取得图片
    im = get_im(img)

    # 图片尺寸
    (width, height) = im.size
    # 如果目标大小
    if dst_width < 0 or dst_height < 0:
        logcm.print_info('dest with or height is < 0!', fg='red')
        return im

    if keep_ratio:
        # 取得宽度和高度的转换比率
        ratio_width = width / dst_width
        ratio_height = height / dst_height
        if ratio_width > ratio_height:
            # 宽度压缩比例较小时
            dst_height = round(height / ratio_width)
        elif ratio_width < ratio_height:
            # 高度压缩比例较小时
            dst_width = round(width / ratio_height)

    # 调整图片尺寸
    # logcm.print_info('dest size is (%d, %d)' % (dst_width, dst_height))
    im_resize = im.resize((dst_width, dst_height), Image.ANTIALIAS)
    # 保存图片
    if save_path is not None:
        im_resize.save(save_path, quality=100)
    return im_resize


def flip(img, flip_h=True, flip_v=False, save_path=None):
    """
    把图片左右上下互换并保存。
    @param img: 图片或路径
    @param save_path: 保存路径
    @param flip_h: 水平互换
    @param flip_v: 垂直互换
    @return: 处理后的图片对象
    """

    # 打开图片
    im = get_im(img)

    if flip_h:
        # 左右互换
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    if flip_v:
        # 上下互换
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
    # 保存图片
    if save_path is not None:
        im.save(save_path, quality=100)

    return im


def empty_img(mode, width, height, val='255'):
    """
    生成指定大小的空白图片。
    @param mode: 图片模式
    @param width: 图片宽度
    @param height: 图片高度
    @param val: 填充像素值
    @return: 空白图片
    """
    if len(mode) == 1:  # L, 1
        new_background = (val)
    if len(mode) == 3:  # RGB
        new_background = (val, val, val)
    if len(mode) == 4:  # RGBA, CMYK
        new_background = (val, val, val, val)

    img = Image.new(mode, (width, height), new_background)
    return img


def paste_center(img_bottom, img_top):
    """
    把顶层图片粘贴在底层图片上。
    @param img_bottom: 底层图片
    @param img_top: 顶层图片
    @return: 无
    """
    if img_bottom is None:
        logcm.print_info("Bottom image is None!", fg='red')
    if img_top is None:
        logcm.print_info("Top image is None!", fg='red')

    top_width, top_height = img_top.size
    bottom_width, bottom_height = img_bottom.size
    # 计算居中粘贴时，左上角坐标
    x1 = int(math.floor((bottom_width - top_width) / 2))
    y1 = int(math.floor((bottom_height - top_height) / 2))

    img_bottom.paste(img_top, (x1, y1, x1 + top_width, y1 + top_height))


def resize_canvas(img, canvas_width, canvas_height, back_val=255, save_path=None):
    """
    重新设置画布大小，原始图片居中显示
    @param img: 原始图片或路径
    @param canvas_width: 底层图片
    @param canvas_height: 顶层图片
    @param back_val: 背景色值（0-255）
    @param save_path: 保存路径（可选）
    @return: 重新设置画布后的图片
    """

    if canvas_width < 0 or canvas_width < 0:
        logcm.print_info('Canvas with or height is < 0!', fg='red')
    # 取得图片
    im = get_im(img)
    # 生成新图片
    new_image = empty_img(im.mode, canvas_width, canvas_height, back_val)
    # 居中粘贴
    paste_center(new_image, im)
    # 保存图片
    if save_path is not None:
        new_image.save(save_path)
    return new_image


def zoom_in(img, ratio=1.1, save_path=None):
    """
    对原始图片居中放大指定倍数后裁切为原始大小
    @param img: 原始图片或路径
    @param ratio: 放大比例
    @param save_path: 保存路径（可选）
    @return: 放大后的图片
    """
    if ratio <= 1.0:
        logcm.print_info('Zoom in ratio must > 1.0!', fg='red')
    # 取得图片
    im = get_im(img)
    # 图片原始尺寸
    (width, height) = im.size
    # 放大图片
    new_width = int(width * ratio)
    new_height = int(height * ratio)
    im = resize(im, new_width, new_height)
    # 计算居中剪切时，左上角坐标
    x = int(math.floor((new_width - width) / 2))
    y = int(math.floor((new_height - height) / 2))
    # 剪切
    im_zoom = im.crop((x, y, x + width, y + height))
    # 保存图片
    if save_path is not None:
        im_zoom.save(save_path)
    return im_zoom


def zoom_out(img, ratio=0.9, save_path=None):
    """
    对原始图片居中缩小指定倍数后画布仍为原始大小
    @param img: 原始图片或路径
    @param ratio: 缩小比例
    @param save_path: 保存路径（可选）
    @return: 放大后的图片
    """
    if ratio >= 1.0:
        logcm.print_info('Zoom out ratio must < 1.0!', fg='red')
    # 取得图片
    im = get_im(img)
    # 图片原始尺寸
    (width, height) = im.size
    # 缩小图片
    new_width = int(width * ratio)
    new_height = int(height * ratio)
    im = resize(im, new_width, new_height)
    # 重设画布大小
    im_zoom = resize_canvas(im, width, height, 0)

    # 保存图片
    if save_path is not None:
        im_zoom.save(save_path)
    return im_zoom


def move(img, move_h=0, move_v=0, back_val=255, save_path=None):
    """
    对原始图片进行移动后画布仍为原始大小
    @param img: 原始图片或路径
    @param move_h: 水平移动值
    @param move_v: 竖直移动值
    @param back_val: 背景色值（0-255）
    @param save_path: 保存路径（可选）
    @return: 移动后的图片
    """
    if img is None:
        logcm.print_info('Image is None!', fg='red')
    # 取得图片
    im = get_im(img)
    # 图片原始尺寸
    (width, height) = im.size
    # 图片移动量范围限制
    if move_h > width:
        move_h = width
    if move_h + width < 0:
        move_h = -1 * width
    if move_v > height:
        move_v = height
    if move_v + height < 0:
        move_v = -1 * height

    # 生成新图片
    new_image = empty_img(im.mode, width, height, back_val)
    # 粘贴图片到移动后的位置
    new_image.paste(im, (move_h, move_v, move_h + width, move_v + height))

    # 保存图片
    if save_path is not None:
        new_image.save(save_path)
    return new_image
