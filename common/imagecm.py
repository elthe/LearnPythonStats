# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Image common api
图片相关共通函数
"""

from PIL import Image


def get_size(img_path):
    """
    根据图片文件路径取得图片尺寸
    @param img_path: 图片路径
    @return: 图片尺寸
    """

    img = Image.open(img_path)
    return img.size


def is_landscape(img_path):
    """
    根据图片文件路径判断是否横版图片
    @param img_path: 图片路径
    @return: 是否横版图片
    """

    # 图片尺寸
    (width, height) = get_size(img_path)
    # 如果宽度大于高度，则为横版图片
    return width > height


def resize(img_path, dst_width, dst_height, save_path, keep_ratio=True):
    """
    把图片对象压缩成目标大小，可以保持比例。
    @param img_path: 图片路径
    @param dst_width: 目标宽度
    @param dst_height: 目标高度
    @param save_path: 保存路径
    @param keep_ratio: 保持比例
    @return: 处理后的图片对象
    """

    # 打开图片
    img = Image.open(img_path)
    # 图片尺寸
    (width, height) = img.size
    # 如果目标大小
    if dst_width < 0 or dst_height < 0:
        print('dest with or height is < 0!')
        return None

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

    # 调整图片尺寸, 并保存
    print('dest size is (%d, %d)' % (dst_width, dst_height))
    img.resize((dst_width, dst_height), Image.ANTIALIAS).save(save_path, quality=100)
