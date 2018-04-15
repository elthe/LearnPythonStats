#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plot common api
图像绘制相关共通函数
"""

import matplotlib.pyplot as plt
import numpy as np
import math

from common import logcm


def draw_text(ax, x_list, y_list, text, h_align='left', v_align='top', color='black', font_size='12'):
    """
    在坐标轴指定位置，以指定颜色和大小绘制指定文本
    @param ax: 绘画坐标轴
    @param x_list: x坐标一览
    @param y_list: y坐标一览
    @param text: 指定文本
    @param h_align: 指定位置(left,center,right)
    @param v_align: 指定位置(top,middle,bottom)
    @param color: 颜色
    @param font_size: 字体大小
    @:return 无
    """

    # X轴位置
    if h_align == 'left':
        xt = np.min(x_list)

    elif h_align == 'center':
        xt = (np.min(x_list) + np.max(x_list)) / 2

    elif h_align == 'right':
        xt = np.max(x_list)

    # Y轴位置
    if v_align == 'top':
        yt = np.max(y_list)

    elif v_align == 'middle':
        yt = (np.min(y_list) + np.max(y_list)) / 2

    elif v_align == 'bottom':
        yt = np.min(y_list)

    # 开始绘制
    font = {'color': color}
    ax.text(xt, yt, text, fontdict=font,
            fontsize=font_size, verticalalignment=v_align, horizontalalignment=h_align)


def ticks_list_pi(start, end, step=0.5):
    """
    PI的坐标轴标签的值和文本。
    @param start: 开始
    @param end: 结束
    @param step: 不长
    @:return 值列表,文本列表
    """
    pre_list = np.arange(start, end, step)
    data_list = []
    txt_list = []
    for pre in pre_list:
        val = pre * np.pi
        txt = r'%.2f$\pi$' % pre
        data_list.append(val)
        txt_list.append(txt)
    return (data_list, txt_list)


def draw_point_list(ax, x, y, show_line=True, show_label=True, color='gray', line_style=':'):
    """
    在坐标轴中指定坐标列表，绘制点，及对应的辅助线和标签
    @param ax: 绘画坐标轴
    @param x: X坐标列表
    @param y: Y坐标列表
    @param show_line: 显示辅助线
    @param show_label: 显示标签
    @param color: 颜色
    @param line_style: 样式
    @:return 无
    """

    for i in range(len(x)):
        draw_point(ax, x[i], y[i], show_label=show_label, show_line=show_line, color=color, line_style=line_style)


def draw_point(ax, x, y, show_line=True, show_label=True, color='gray', line_style=':'):
    """
    在坐标轴中指定坐标，绘制点，及对应的辅助线和标签
    @param ax: 绘画坐标轴
    @param x: X坐标
    @param y: Y坐标
    @param show_line: 显示辅助线
    @param show_label: 显示标签
    @param color: 颜色
    @param line_style: 样式
    @:return 无
    """
    # 画点
    ax.scatter(x, y, marker='o', color=color)

    # 辅助线
    if show_line:
        draw_h_line(ax, 0, x, y, color=color, line_style=line_style)
        draw_v_line(ax, 0, y, x, color=color, line_style=line_style)
    # 标签
    if show_label:
        label = '(%s, %.1f)' % (str(x), y)
        ax.text(x + 0.1, y - 0.1, label, color=color, verticalalignment="top", horizontalalignment="left")


def draw_h_line(ax, start, end, val, color='gray', line_style='-'):
    """
    在坐标轴中指定范围，绘制水平线
    @param ax: 绘画坐标轴
    @param start: 开始值
    @param end: 终止值
    @param val: 水平值
    @param color: 颜色
    @param line_style: 样式
    @:return 无
    """

    # 绘制Y轴0线
    x = np.arange(start, end, 0.01)
    y = np.repeat(val, len(x))
    line, = ax.plot(x, y, line_style, color=color)


def draw_v_line(ax, start, end, val, color='gray', line_style='-'):
    """
    在坐标轴中指定范围，绘制竖直线
    @param ax: 绘画坐标轴
    @param start: 开始值
    @param end: 终止值
    @param val: 竖直值
    @param color: 颜色
    @param line_style: 样式
    @:return 无
    """

    # 绘制Y轴0线
    y = np.arange(start, end, 0.01)
    x = np.repeat(val, len(y))
    line, = ax.plot(x, y, line_style, color=color)


def draw_func_line(ax, x, func, label, x_lbl, color='gray', line='-'):
    """
    在坐标轴中指定范围，绘制竖直线
    @param ax: 绘画坐标轴
    @param x: x轴值列表
    @param func: 函数
    @param label: 标签
    @param color: 颜色
    @param line: 线条样式
    @:return 无
    """

    # 执行匿名函数，计算Y轴值列表
    y = func(x)
    # 根据XY轴坐标画线
    ax.plot(x, y, line, color=color, label=label)
    # 计算标签的Y坐标
    y_lbl = func(x_lbl)
    # 绘制标签文本
    ax.text(x_lbl + 0.1, y_lbl - 0.1, label, color=color, verticalalignment="top", horizontalalignment="left")


def grid_by_list(img_list, title_list, col_num, save_path, cell_width=2.5, cell_height=2):
    """
    把图片及其标题一览，按照指定列数，绘制成网格，并保存到指定路径。
    @param img_list: 图片列表
    @param title_list: 标题列表
    @param col_num: 指定列数
    @param save_path: 保存路径
    @param cell_width: 格子宽度
    @param cell_height: 格子高度
    @:return 无
    """

    # 检验图片列表是否为空
    if len(img_list) == 0:
        logcm.print_info("Image list is empty!")
        return

    # 检验图片列表和标题列表是否对齐
    if len(img_list) != len(title_list):
        logcm.print_info("Image list must has same length as title list!")
        return

    # 计算需要的行数
    row_num = math.ceil(len(img_list) / col_num)
    # 多子图绘制
    fig, axes = plt.subplots(row_num, col_num, sharey=False, sharex=False)
    # 设置图片尺寸
    fig.set_size_inches(col_num * cell_width, row_num * cell_height)
    # 总标题
    fig.suptitle('')
    # 设置标题(中文字体)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    for i in range(row_num):
        for j in range(col_num):
            index = i * col_num + j
            # 坐标轴
            ax = axes[i][j]
            # 在列表范围，显示图片和标题。
            if index < len(img_list):
                logcm.print_info("showing axes[%d][%d]-%s" % (i, j, title_list[index]))
                # 显示图片
                if img_list[index] is not None:
                    ax.imshow(img_list[index], 'gray')
                # 显示标题
                ax.set_title(title_list[index])
            # 隐藏坐标轴
            ax.axis("off")
            ax.set_xticks([])
            ax.set_yticks([])

    # 调整每隔子图之间的距离
    plt.tight_layout()
    # 保存图片
    plt.savefig(save_path)
    # 显示绘制后的图片
    plt.show()


def grid_by_matrix(img_matrix, title_matrix, col_num, save_path, cell_width=2.5, cell_height=2):
    """
    把图片及其标题矩阵，按照指定列数，绘制成网格，并保存到指定路径。
    @param img_matrix: 图片矩阵
    @param title_matrix: 标题矩阵
    @param col_num: 指定列数
    @param save_path: 保存路径
    @param cell_width: 格子宽度
    @param cell_height: 格子高度
    @:return 无
    """

    # 检验图片矩阵是否为空
    if len(img_matrix) == 0:
        logcm.print_info("Image matrix is empty!")
        return

    # 检验图片矩阵和标题矩阵是否对齐
    if len(img_matrix) != len(title_matrix):
        logcm.print_info("Image matrix must has same rows as title matrix!")
        return
    if len(img_matrix[0]) != len(title_matrix[0]):
        logcm.print_info("Image matrix must has same cols as title matrix!")
        return

    # 矩阵行数
    line_num = len(img_matrix)
    # 计算最大列数
    max_col_num = len(img_matrix[0])
    for line in img_matrix:
        if len(line) > max_col_num:
            max_col_num = len(line)
    # 计算矩阵一行需要的行数
    line_row_num = math.ceil(max_col_num / col_num)
    # 总行数
    row_num = line_num * line_row_num
    # 多子图绘制
    fig, axes = plt.subplots(row_num, col_num, sharey=False, sharex=False)
    # 设置图片尺寸
    fig.set_size_inches(col_num * cell_width, row_num * cell_height)
    # 总标题
    fig.suptitle('')
    # 设置标题(中文字体)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    for i in range(row_num):
        for j in range(col_num):
            # 计算在矩阵中的行列
            row = i // line_row_num
            col = i % line_row_num * col_num + j
            # 坐标轴
            ax = axes[i][j]
            # 在列表范围，显示图片和标题。
            if col < len(img_matrix[row]):
                logcm.print_info("showing axes[%d][%d]-%s" % (row, col, title_matrix[row][col]))
                # 显示图片
                if img_matrix[row][col] is not None:
                    ax.imshow(img_matrix[row][col], 'gray')
                # 显示标题
                ax.set_title(title_matrix[row][col])
            # 隐藏坐标轴
            ax.axis("off")
            ax.set_xticks([])
            ax.set_yticks([])

    # 调整每隔子图之间的距离
    plt.tight_layout()
    # 保存图片
    plt.savefig(save_path)
    # 显示绘制后的图片
    plt.show()
