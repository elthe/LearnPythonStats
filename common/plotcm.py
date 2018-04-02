#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plot common api
图像绘制相关共通函数
"""

import matplotlib.pyplot as plt
import numpy as np


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
