# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Image common api
图片相关共通函数
"""

import cv2
import math
import numpy as np

from common import logcm
from common import datecm
from common import imfiltercm
from PIL import Image
from skimage import img_as_ubyte, img_as_float, io, transform


class ImageType:
    """
    图片类型定义
    """
    # 图片文件路径
    IMG_FILE = 'FILE'
    # PIL的图片对象
    IMG_PIL = 'PIL'
    # skimage的图片对象
    IMG_SK = 'SK'
    # opencv的BGR图片对象
    IMG_BGR = 'BGR'
    # opencv的HSV图片对象
    IMG_HSV = 'HSV'
    # opencv的HLS图片对象
    IMG_HLS = 'HLS'
    # opencv的灰度图片
    IMG_GRAY = 'GRAY'


class VideoActionOutput:
    def __init__(self, im_output, img_path, img_no):
        """
        视频动画输出类
        :param im_output: 视频图片输出
        :param img_path: 原始图片路径
        :param img_no: 原始图片编号
        """
        self.output = im_output
        self.img_path = img_path
        self.img_no = img_no
        self.im_bgr = get_bgr_im(img_path, ImageType.IMG_FILE)

        # 人脸侦测
        self.faces = imfiltercm.detect_face(self.im_bgr)
        # 皮肤侦测
        self.im_skin = imfiltercm.detect_skin(self.im_bgr)

    def out_action(self, action_type, val_list, val_ratio=1, **kwargs):
        """
        把指定动画写入视频
        """
        self.output.clear()
        for val in val_list:
            # 输出图片类型
            out_img_type = ImageType.IMG_BGR
            # 当前值
            value = val * val_ratio
            # 标题
            title = action_type

            # 色调动画
            if action_type == "add_hue":
                img = add_img_HSV(self.im_bgr, add_h=value)
            # 饱和度动画
            elif action_type == "change_saturation":
                img = imfiltercm.change_saturation(self.im_bgr, value)
            # 饱和度动画
            elif action_type == "change_darker":
                img = imfiltercm.change_darker(self.im_bgr, value)
            # 放大动画
            elif action_type == "zoom_in":
                img = zoom_in(self.img_path, value)
                out_img_type = ImageType.IMG_PIL
            # 缩小动画
            elif action_type == "zoom_out":
                img = zoom_out(self.img_path, value)
                out_img_type = ImageType.IMG_PIL
            # 旋转动画
            elif action_type == "rotate":
                img = rotate(self.img_path, value, resize=False)
                out_img_type = ImageType.IMG_SK
            # 水平移动动画
            elif action_type == "move_h":
                img = move(self.img_path, move_h=value, back_val=0)
                out_img_type = ImageType.IMG_PIL
            # 竖直移动动画
            elif action_type == "move_v":
                img = move(self.img_path, move_v=value, back_val=0)
                out_img_type = ImageType.IMG_PIL
            # 标记人脸
            elif action_type == "mark_face":
                img = imfiltercm.mark_face(self.im_bgr, self.faces, border=int(value))
            # 人脸美白动画
            elif action_type == "whitening_face":
                img = imfiltercm.whitening_face(self.im_bgr, self.faces, value)
            # 皮肤美白动画
            elif action_type == "whitening_skin":
                img = imfiltercm.whitening_skin(self.im_bgr, self.im_skin, value)
            # 滤镜
            elif action_type == "im_filter":
                img = imfiltercm.im_filter(self.im_bgr, kwargs["filter_name"], value)
                title += "-" + kwargs["filter_name"]

            # 加入图片
            self.output.out_im(img, out_img_type, title=title, img_no=self.img_no)


class VideoImageOutput:
    def __init__(self, video_writer):
        """
        视频图片输出类
        """
        self.video = video_writer
        self.count = 0
        self.last_time = datecm.get_now_time("mini")

    def out_im(self, img, img_type=ImageType.IMG_BGR, title="", img_no=1):
        """
        把图片写入视频。
        :param video_writer: 视频输出器
        :param img: 原始图片或路径
        :param img_type 图片类型（ImageType）
        :param title 标题
        @return: 无
        """
        # 转化成BGR图片
        im_bgr = get_bgr_im(img, img_type)
        # 写入视频
        self.video.write(im_bgr)
        # 计数
        self.count += 1
        # 当前时间
        now_time = datecm.get_now_time("mini")
        # 花费时间
        cost_time = now_time - self.last_time
        self.last_time = now_time
        # 日志
        logcm.print_info(
            "Img-%d : %s No.%d image(%s) write ok in %dms !" % (img_no, title, self.count, img_type, cost_time),
            show_header=False)

    def clear(self):
        """
        清空计数器。
        @return: 无
        """
        self.count = 0
        self.last_time = datecm.get_now_time("mini")


def get_bgr_im(src_img, img_type=ImageType.IMG_BGR):
    """
    根据指定图片类型加载图片为BGR图片
    @:param src_img 原始图片对象或路径
    @:param img_type 图片类型（ImageType）
    @return: BGR图片
    """
    if src_img is None:
        logcm.print_info('Src Image is None!', fg='red')

    im_bgr = None

    # 图片文件
    if img_type == ImageType.IMG_FILE:
        im_bgr = cv2.imread(src_img)

    # PIL图片
    if img_type == ImageType.IMG_PIL:
        im_bgr = cv2.cvtColor(np.asarray(src_img), cv2.COLOR_RGB2BGR)

    # SK图片
    if img_type == ImageType.IMG_SK:
        im_rgb = img_as_ubyte(src_img)
        im_bgr = cv2.cvtColor(im_rgb, cv2.COLOR_RGB2BGR)

    # HSV图片
    if img_type == ImageType.IMG_HSV:
        im_bgr = cv2.cvtColor(src_img, cv2.COLOR_HSV2BGR)

    # HLS图片
    if img_type == ImageType.IMG_HLS:
        im_bgr = cv2.cvtColor(src_img, cv2.COLOR_HLS2BGR)

    # 灰度图片
    if img_type == ImageType.IMG_GRAY:
        im_bgr = cv2.cvtColor(src_img, cv2.COLOR_GRAY2BGR)

    # BGR图片
    if img_type == ImageType.IMG_BGR:
        im_bgr = src_img

    return im_bgr


def im_convert(src_img, type_from=ImageType.IMG_FILE, type_to=ImageType.IMG_BGR, save_path=None):
    """
    图片类型转换方法
    @:param src_img 原始图片对象或路径
    @:param type_from 转换前类型（ImageType）
    @:param type_to 转换后类型（ImageType）
    @:param save_path: 保存路径（转换为文件类型时必须）
    @return: 转换后的图片
    """
    if src_img is None:
        logcm.print_info('Src Image is None!', fg='red')
        return None

    # 如果类型相同直接返回
    if type_from == type_to:
        return src_img

    # 先把图片专为成BGR图片
    im_bgr = get_bgr_im(src_img, type_from)
    if im_bgr is None:
        logcm.print_info('BGR Image Loading Fail!', fg='red')
        return None

    # BGR图片
    if type_to == ImageType.IMG_BGR:
        return im_bgr

    # PIL图片
    if type_to == ImageType.IMG_PIL:
        im_rgb = Image.fromarray(cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB))
        return im_rgb

    # SK图片
    if type_to == ImageType.IMG_SK:
        im_rgb = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB)
        im_sk = img_as_float(im_rgb).astype(np.float64)
        return im_sk

    # HSV图片
    if type_to == ImageType.IMG_HSV:
        im_hsv = cv2.cvtColor(src_img, cv2.COLOR_BGR2HSV)
        return im_hsv

    # HLS图片
    if type_to == ImageType.IMG_HLS:
        im_hls = cv2.cvtColor(src_img, cv2.COLOR_BGR2HLS)
        return im_hls

    # 灰度图片
    if type_to == ImageType.IMG_GRAY:
        im_gray = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
        return im_gray

    # 图片文件
    if type_to == ImageType.IMG_FILE:
        cv2.imwrite(save_path)


def add_img_HSV(img, img_type=ImageType.IMG_BGR, add_h=0, add_s=0, add_v=0,
                ratio_h=1.0, ratio_s=1.0, ratio_v=1.0, dst_type=None, save_path=None):
    """
    修改图片的HSV值。
    HSV分别是色调（Hue），饱和度（Saturation）和明度（Value）。
    在HSV空间中进行调节就避免了直接在RGB空间中调节是还需要考虑三个通道的相关性。
    @:param img 原始图片对象或路径
    @:param img_type 图片类型（ImageType）
    @:param add_h 色调增加量（注意：取值范围是[0, 180)）
    @:param add_s 饱和度增加量（注意：取值范围是[0, 256)）
    @:param add_v 明度增加量（注意：取值范围是[0, 256)）
    @:param ratio_h 色调变化比例（注意：取值范围是[0, 180)）
    @:param ratio_s 饱和度变化比例（注意：取值范围是[0, 256)）
    @:param ratio_v 明度变化比例（注意：取值范围是[0, 256)）
    @:param dst_type 目标图片类型（ImageType），为空则保持类型不变
    @:param save_path: 保存路径（转换为文件类型时必须）
    @return: 处理后的图片
    """

    # 取得HSV图片
    im_hsv = im_convert(img, img_type, ImageType.IMG_HSV)
    # 复制HSV
    im_hsv_dst = im_hsv.copy()

    # 色调处理
    im_hsv_dst[:, :, 0] = (im_hsv_dst[:, :, 0] + add_h) * ratio_h
    # 饱和度处理
    im_hsv_dst[:, :, 1] = (im_hsv_dst[:, :, 1] + add_s) * ratio_s
    # 明度处理
    im_hsv_dst[:, :, 2] = (im_hsv_dst[:, :, 2] + add_v) * ratio_v

    # 目标类型默认为原始类型
    if dst_type is None:
        dst_type = img_type
    # 图片保存
    if save_path is not None:
        im_convert(im_hsv_dst, ImageType.IMG_HSV, ImageType.IMG_FILE, save_path)

    # 目标类型转换
    img_dst = im_convert(im_hsv_dst, ImageType.IMG_HSV, img_type)
    return img_dst


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


def get_sk_im(img):
    """
    根据图片文件路径或图片
    @param img: 图片或路径
    @return: 图片对象
    """
    # 取得图片
    im_sk = io.imread(img) if isinstance(img, str) else img
    return im_sk


def rotate(img, angle, resize=False):
    """
    对原始图片进行旋转后。
    @param img: 原始SK图片或路径
    @param angle: 逆时针角度
    @param resize: 是否变更原来尺寸
    @param save_path: 保存路径（可选）
    @return: 旋转后的SK图片
    """

    im_sk = get_sk_im(img)
    im_sk_new = transform.rotate(im_sk, angle, resize=resize)
    return im_sk_new
