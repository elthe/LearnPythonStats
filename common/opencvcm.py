# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
OpenCV common api
图像识别相关共通函数

"""

import cv2
import numpy as np

from common import logcm
from common import filecm

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


def find_rois(img, min_width=20, min_height=20, min_area=None, min_wh_ratio=None, max_wh_ratio=None):
    """
    从图片中获取外边框在指定大小以上的感兴趣区域（ROI）。
    @:param img 图片
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
    # 使用cv2.findContours()函数来查找检测物体的轮廓。
    # 参数
    #   第一个参数是寻找轮廓的图像；
    #   第二个参数表示轮廓的检索模式，有四种（本文介绍的都是新的cv2接口）：
    #     cv2.RETR_EXTERNAL 表示只检测外轮廓
    #     cv2.RETR_LIST     检测的轮廓不建立等级关系
    #     cv2.RETR_CCOMP    建立两个等级的轮廓，上面的一层为外边界，里面的一层为内孔的边界信息。
    #                       如果内孔内还有一个连通物体，这个物体的边界也在顶层。
    #     cv2.RETR_TREE     建立一个等级树结构的轮廓。
    #
    #   第三个参数method为轮廓的近似办法
    #     cv2.CHAIN_APPROX_NONE     存储所有的轮廓点，相邻的两个点的像素位置差不超过1，即max（abs（x1 - x2），abs（y2 - y1）） == 1
    #     cv2.CHAIN_APPROX_SIMPLE   压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标，例如一个矩形轮廓只需4个点来保存轮廓信息
    #     cv2.CHAIN_APPROX_TC89_L1，CV_CHAIN_APPROX_TC89_KCOS使用teh - Chinl chain近似算法
    # 返回值
    # cv2.findContours()
    # 函数返回两个值，一个是轮廓本身，还有一个是每条轮廓对应的属性。
    # hierarchy返回值
    # 此外，该函数还可返回一个可选的hiararchy结果，这是一个ndarray，其中的元素个数和轮廓个数相同，每个轮廓contours[i]
    # 对应4个hierarchy元素hierarchy[i][0]
    # ~hierarchy[i][3]，分别表示后一个轮廓、前一个轮廓、父轮廓、内嵌轮廓的索引编号，如果没有对应项，则该值为负数。
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

        # 最小和最大宽高比限制
        ratio = float(w) / float(h)
        if max_wh_ratio is not None:
            if ratio > max_wh_ratio:
                continue
        if min_wh_ratio is not None:
            if ratio < min_wh_ratio:
                continue

        # 判断最小宽度和高度
        if w > min_width and h > min_height:
            rois.append((x, y, w, h))

    # 对区域排序，先上线，再左右。
    sorted_rois = sorted(rois, key=lambda t: t[1] * img_width + t[0])

    return sorted_rois


def get_color(key, map_clr):
    """
    根据关键词，取得颜色，如果不存在，则生成随机颜色。
    @:param key 关键词
    @:param map_clr 颜色字典
    @return: 颜色
    """

    # 初始化
    map_clr = {} if map_clr is None else map_clr
    if key not in map_clr:
        # 生成随机颜色
        map_clr[key] = np.random.randint(0, high=256, size=(3,)).tolist()
    return map_clr[key]


def rect_contours(img, contours, hierarchy, tmp_path=None, tmp_key=None, img_list=None, title_list=None):
    """
    在图片上绘制指定轮廓列表。
    @:param img 图片
    @:param contours 边界列表
    @:param hierarchy 层次信息
    @:param tmp_path 临时目录
    @:param tmp_key 临时关键词
    @:param img_list 图片列表
    @:param title_list 标题列表
    @return: 平滑图片
    """

    # 灰度转彩图，便于查看边框
    img_rect = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img_white = img.copy()
    img_white.fill(255)
    img_white = cv2.cvtColor(img_white, cv2.COLOR_GRAY2BGR)

    # 颜色Map
    map_clr = {}

    # 循环轮廓
    for i in range(len(contours)):
        c = contours[i]
        # 取得颜色
        key = str(hierarchy[i][3])
        color = get_color(key, map_clr)

        # 取得轮廓的直边界矩形
        x, y, w, h = cv2.boundingRect(c)

        # 绘制边框到图片上
        cv2.rectangle(img_rect, (x, y), (x + w, y + h), color, 3)
        # 绘制边框到图片上
        cv2.rectangle(img_white, (x, y), (x + w, y + h), color, 2)
        # 识别结果展示
        txt = '%d' % i
        # 照片/添加的文字/左上角坐标/字体/字体大小/颜色/字体粗细
        cv2.putText(img_white, txt, (x + 2, y + 25), cv2.FONT_HERSHEY_PLAIN, 2.0, (200, 0, 0), 2, cv2.LINE_AA)

    save_tmp(img_rect, "rect_contours", "rect-" + tmp_key, tmp_path, tmp_key, img_list, title_list)
    save_tmp(img_white, "rect_contours", "white-" + tmp_key, tmp_path, tmp_key, img_list, title_list)
    return img_rect


def get_blur(gray, is_gaussian=False, blur_block=(3, 3), median_val=None, tmp_path=None, tmp_key=None, img_list=None,
             title_list=None):
    """
    取得图片平滑处理后的图片。
    @:param gray 灰度图片
    @:param is_gaussian 是否使用高斯
    @:param blur_block 平滑块大小
    @:param median_val 中值滤波的中值
    @:param tmp_path 临时目录
    @:param tmp_key 临时关键词
    @:param img_list 图片列表
    @:param title_list 标题列表
    @return: 平滑图片
    """

    # 函数名
    func_key = "get_blur"

    if is_gaussian:
        # 高斯平滑
        blur = cv2.GaussianBlur(gray, blur_block, 0, 0, cv2.BORDER_DEFAULT)
        save_tmp(blur, func_key, "GaussianBlur", tmp_path, tmp_key, img_list, title_list)
    else:
        # 均值滤波
        blur = cv2.blur(gray, blur_block)
        save_tmp(blur, func_key, "blur", tmp_path, tmp_key, img_list, title_list)

    if median_val is None:
        return blur

    # 中值滤波
    median = cv2.medianBlur(blur, median_val)
    save_tmp(median, func_key, "medianBlur", tmp_path, tmp_key, img_list, title_list)
    return median


def add_weighted(gray, weight_x=0.5, weight_y=0.5, tmp_path=None, tmp_key=None, img_list=None, title_list=None):
    """
    X轴和Y轴按权重组合图像
    @:param gray 图片
    @:param weight_x X轴权重
    @:param weight_y Y轴权重
    @:param tmp_path 临时目录
    @:param tmp_key 临时关键词
    @:param img_list 图片列表
    @:param title_list 标题列表
    @return: 阈值图片
    """

    # 函数名
    func_key = "add_weighted"

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
    x = cv2.Sobel(gray, cv2.CV_16S, 1, 0)
    y = cv2.Sobel(gray, cv2.CV_16S, 0, 1)

    # convertScaleAbs()--转回uint8形式，否则将无法显示图像，而只是一副灰色图像
    # dst = cv2.convertScaleAbs(src[, dst[, weight_x[, weight_y]]])
    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)

    # 组合图像 dst = cv2.addWeighted(src1, weight_x, src2, weight_y, gamma[, dst[, dtype]])
    #   weight_x  --  第一幅图片中元素的权重
    #   weight_y   --  第二个权重
    #   gamma  --  累加到结果上的一个值
    dst = cv2.addWeighted(absX, weight_x, absY, weight_y, 0)
    save_tmp(dst, func_key, "addWeighted", tmp_path, tmp_key, img_list, title_list)

    return dst


def get_sobel(gray, dx, dy, ksize=3, ddepth=-1, tmp_path=None, tmp_key=None, img_list=None, title_list=None):
    """
    从图片中阈值图片（黑白图）
    @:param gray 灰度图片
    @:param dx dy 表示的是示导的阶数，0表示这个方向上没有求导，一般为0，1，2。
    @:param ksize Sobel算子的大小，必须为1、3、5、7。
    @:param ddepth 图像的深度，-1表示采用的是与原图像相同的深度。目标图像的深度必须大于等于原图像的深度。
    @:param tmp_key 临时关键词
    @:param img_list 图片列表
    @:param title_list 标题列表
    @return: 阈值图片
    """

    # 函数名
    func_key = "get_sobel"

    # Sobel算子
    sobel = cv2.Sobel(gray, ddepth, dx, dy, ksize=ksize)
    save_tmp(sobel, func_key, "Sobel(%d,%d)" % (dx, dy), tmp_path, tmp_key, img_list, title_list)

    return sobel


def get_thresh(gray, thresh_value, thresh_type=cv2.THRESH_BINARY, tmp_path=None, tmp_key=None, img_list=None,
               title_list=None):
    """
    从图片中阈值图片（黑白图）
    @:param gray 灰度图片
    @:param thresh_value 阈值处理的阈值值
    @:param thresh_type 阈值处理方式
    @:param tmp_path 临时目录
    @:param tmp_key 临时关键词
    @:param img_list 图片列表
    @:param title_list 标题列表
    @return: 阈值图片
    """

    # 函数名
    func_key = "get_thresh"

    # 简单阈值
    ret, thresh = cv2.threshold(gray, thresh_value, 255, thresh_type)
    save_tmp(thresh, func_key, "threshold", tmp_path, tmp_key, img_list, title_list)

    return thresh


def get_gray(img, tmp_path=None, tmp_key=None, img_list=None, title_list=None):
    """
    从图片中获取灰度图片。
    @:param img 图片
    @:param tmp_path 临时目录
    @:param tmp_key 临时关键词
    @:param img_list 图片列表
    @:param title_list 标题列表
    @return: 灰度图片
    """

    # 灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    save_tmp(gray, "get_gray", "Gray", tmp_path, tmp_key, img_list, title_list)

    return gray


def get_edges(gray, diff_type, kernel_dilate=None, kernel_erode=None, tmp_path=None, tmp_key=None, img_list=None,
              title_list=None):
    """
    从图片中获取边界图片。
    @:param gray 灰度图片
    @:param diff_type 相减方式（D-E, DED-DE）
    @:param kernel_dilate 膨胀核参数
    @:param kernel_erode 腐蚀核参数
    @:param tmp_path 临时目录
    @:param tmp_key 临时关键词
    @:param img_list 图片列表
    @:param title_list 标题列表
    @return: 边界图片
    """

    # 函数名
    func_key = "get_edges"
    # 根据相减方式处理
    if diff_type == 'D-E':
        # 膨胀一次，让轮廓突出
        dilation = cv2.dilate(gray, kernel_dilate, iterations=1)
        save_tmp(dilation, func_key, "dilate-D", tmp_path, tmp_key, img_list, title_list)

        # 腐蚀一次，去掉细节
        erosion = cv2.erode(gray, kernel_erode, iterations=1)
        save_tmp(erosion, func_key, "erode-E", tmp_path, tmp_key, img_list, title_list)

        # 将两幅图像相减获得边，第一个参数是膨胀后的图像，第二个参数是腐蚀后的图像
        edges = cv2.absdiff(dilation, erosion)
        save_tmp(edges, func_key, "absdiff(D-E)", tmp_path, tmp_key, img_list, title_list)

    elif diff_type == 'DED-DE':
        # 膨胀一次，让轮廓突出
        dilation1 = cv2.dilate(gray, kernel_dilate, iterations=1)
        save_tmp(dilation1, func_key, "dilate-D", tmp_path, tmp_key, img_list, title_list)

        # 腐蚀一次，去掉细节
        erosion = cv2.erode(dilation1, kernel_erode, iterations=1)
        save_tmp(erosion, func_key, "erode-DE", tmp_path, tmp_key, img_list, title_list)

        # 再次膨胀，让轮廓明显一些
        dilation = cv2.dilate(erosion, kernel_dilate, iterations=3)
        save_tmp(dilation, func_key, "dilate-DED", tmp_path, tmp_key, img_list, title_list)

        # 将两幅图像相减获得边，第一个参数是膨胀后的图像，第二个参数是腐蚀后的图像
        edges = cv2.absdiff(dilation, erosion)
        save_tmp(edges, func_key, "absdiff(DED-DE)", tmp_path, tmp_key, img_list, title_list)

    return edges


def save_tmp(img, func_key, deal_key, tmp_path=None, tmp_key="", img_list=None, title_list=None):
    """
    保存临时图片
    @:param img 图片
    @:param func_key 函数关键词
    @:param deal_key 处理关键词
    @:param tmp_path 临时目录
    @:param tmp_key 临时关键词
    @:param img_list 图片列表
    @:param title_list 标题列表
    @return: 无
    """

    if img is None:
        return None

    # 保存路径
    if tmp_path is not None:
        save_path = "%s/%s-%s_%s.jpg" % (tmp_path, tmp_key, func_key, deal_key)
        logcm.print_info("Temp file save to %s" % save_path)
        cv2.imwrite(save_path, img)

    # 图片加入列表
    if img_list is not None:
        img_list.append(img)

    # 标题加入列表
    if title_list is not None:
        row_num, col_num = img.shape[:2]
        title = '%s %dx%d' % (deal_key, col_num, row_num)
        title_list.append(title)


def scale_img_file(file_path, scale_width, scale_height):
    """
    缩放指定图片文件到指定大小并覆盖原图
    @:param file_path 图片路径
    @:param scale_width 宽度
    @:param scale_height 高度
    @return: 缩放后的图片
    """

    # 读取图片
    img = cv2.imread(file_path)
    # 缩放图片
    img = cv2.resize(img, (scale_width, scale_height), interpolation=cv2.INTER_CUBIC)
    # 写入图片
    cv2.imwrite(file_path, img)
    return img


def scale_img_folder(folder_path, scale_width, scale_height, ext=".png,.jpg,jpeg", match=None):
    """
    缩放指定图片文件目录下所有图片到指定大小并覆盖原图
    @:param folder_path 指定图片目录
    @:param scale_width 宽度
    @:param scale_height 高度
    @return: 无
    """

    # 对图片目录遍历
    path_list = filecm.search_files(folder_path, ext=ext, match=match)
    # 对所有文件进行缩放
    for file_path in path_list:
        scale_img_file(file_path, scale_width, scale_height)
