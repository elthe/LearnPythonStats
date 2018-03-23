#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Stat common api
统计相关共通函数
"""

import statsmodels.api as sm
import numpy as np
import logcm


def plot_acf(ax, slist, diff, unit='天', log=False, pacf=False, show_p=False):
    """
    绘制指定数据序列残差的ACF图或PACF图
    @param ax: 坐标轴
    @param slist: 数据序列
    @param diff: 差分相隔数
    @param unit: 差分单位名（如：天
    @param log: 使用对数值
    @param pacf: 绘制PACF图
    @param show_p: 显示P值
    @:return 无
    """

    # 是否使用对数
    if log:
        # 对数转换
        slist = np.log(slist)
        diff_name = '对数差分'
    else:
        diff_name = '差分'

    # 是否绘制PACF图
    if pacf:
        plot_name = 'PACF图'
    else:
        plot_name = 'ACF图'

    # 设置标题
    title = '%d%s-%s%s' % (diff, unit, diff_name, plot_name)

    # 残差的ACF和PACF图
    slist_diff = slist.diff(diff)[diff:]
    logcm.print_obj(slist_diff, 'series_diff-' + title)
    if pacf:
        sm.graphics.tsa.plot_pacf(slist_diff, ax=ax, title=title)
    else:
        sm.graphics.tsa.plot_acf(slist_diff, ax=ax, title=title)

    # 是否显示P值
    if show_p:
        adftest = sm.tsa.stattools.adfuller(slist_diff)
        p_value = adftest[1]
        logcm.print_obj(p_value, 'p_value')
        # 根据p值是否合格显示成败。
        if p_value < 0.05:
            text = 'p = %f ok!' % adftest[1]
            font = {'color'  : 'g'}
        else:
            text = 'p = %f fail!!' % adftest[1]
            font = {'color'  : 'r'}
        # 输出文字
        ax.text(50, 0.8, text, fontsize=12, verticalalignment="top", fontdict=font,
                horizontalalignment="left")
    return None
