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
