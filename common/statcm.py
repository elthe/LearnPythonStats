#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Stat common api
统计相关共通函数
---- 概念解释 ----
【平稳性处理】平稳性是时间序列分析的前提条件，故我们需要对不平稳的序列进行处理将其转换成平稳的序列。
            对数变换，平滑法、差分、分解
 【对数变换】对数变换主要是为了减小数据的振动幅度，使其线性规律更加明显，
           对数变换相当于增加了一个惩罚机制，数据越大其惩罚越大，数据越小惩罚越小。
  【平滑法】根据平滑技术的不同，平滑法具体分为移动平均法和指数平均法，
           移动平均即利用一定时间间隔内的平均值作为某一期的估计值，而指数平均则是用变权的方法来计算均值
    【差分】时间序列最常用来剔除周期性因素的方法当属差分了，它主要是对等周期间隔的数据进行线性求减
    【分解】所谓分解就是将时序数据分离成不同的成分。比如将时序数据分离成长期趋势、季节趋势和随机成分。
"""

import pandas as pd
import statsmodels.api as sm
import numpy as np

from numpy import *
from pandas import Series
from common import logcm
from common import plotcm


def plot_acf(ax, s_list, diff_num, unit='天', use_log=False, plt_pacf=False, show_p=False):
    """
    绘制指定数据序列残差的ACF图或PACF图
    @param ax: 坐标轴
    @param s_list: 数据序列
    @param diff_num: 差分相隔数
    @param unit: 差分单位名（如：天
    @param use_log: 使用对数值
    @param plt_pacf: 绘制PACF图
    @param show_p: 显示P值
    @:return 无
    """

    # 是否使用对数
    if use_log:
        # 对数转换
        s_list = np.log(s_list)
        diff_name = '对数差分'
    else:
        diff_name = '差分'

    # 是否绘制PACF图
    if plt_pacf:
        plot_name = 'PACF图'
    else:
        plot_name = 'ACF图'

    # 设置标题
    title = '%d%s-%s%s' % (diff_num, unit, diff_name, plot_name)

    # 残差的ACF和PACF图
    s_diff = s_list.diff(diff_num)[diff_num:]
    logcm.print_obj(s_diff, 'series_diff-' + title)
    if plt_pacf:
        sm.graphics.tsa.plot_pacf(s_diff, ax=ax, title=title)
    else:
        sm.graphics.tsa.plot_acf(s_diff, ax=ax, title=title)

    # 是否显示P值
    if show_p:
        adf_result = sm.tsa.stattools.adfuller(s_diff)
        p_value = adf_result[1]
        logcm.print_obj(p_value, 'p_value')
        # 根据p值是否合格显示成败。
        if p_value < 0.05:
            text = 'p = %f ok!' % adf_result[1]
            font = {'color': 'g'}
        else:
            text = 'p = %f fail!!' % adf_result[1]
            font = {'color': 'r'}
        # 输出文字
        ax.text(50, 0.8, text, fontsize=12, verticalalignment="top", fontdict=font,
                horizontalalignment="left")
    return None


def adf_test(s_list, diff_num, use_log=False, full_show=False):
    """
    取得指定数据序列残差的ADF测试
    @param s_list: 数据序列
    @param diff_num: 差分相隔数
    @param use_log: 使用对数值
    @param full_show: 取得完整报告
    @:return 完整报告或单独p值
    """

    # 是否使用对数
    if use_log:
        # 对数转换
        s_list = np.log(s_list)
    # 计算差分
    s_diff = s_list.diff(diff_num)[diff_num:]
    # ADF检测
    test_result = sm.tsa.stattools.adfuller(s_diff)
    # 返回ADF检测报告
    if full_show:
        # 完整报告
        output = pd.DataFrame(index=['Test Statistic Value',
                                     "p-value",
                                     "Lags Used",
                                     "Number of Observations Used",
                                     "Critical Value(1%)",
                                     "Critical Value(5%)",
                                     "Critical Value(10%)"], columns=['value'])
        output['value']['Test Statistic Value'] = test_result[0]
        output['value']['p-value'] = test_result[1]
        output['value']['Lags Used'] = test_result[2]
        output['value']['Number of Observations Used'] = test_result[3]
        output['value']['Critical Value(1%)'] = test_result[4]['1%']
        output['value']['Critical Value(5%)'] = test_result[4]['5%']
        output['value']['Critical Value(10%)'] = test_result[4]['10%']
        # 输出报告
        logcm.print_obj(output, 'output')
        return output
    else:
        return test_result[1]


def to_series(obj):
    """
    把指定对象转换为数据序列
    @param obj: 指定对象
    @:return Series数据序列
    """

    # 取得对象类型名称
    type_name = logcm.get_type_name(obj)

    if type_name == 'pandas.core.series.Series':
        return obj

    if type_name == 'list':
        if array(obj).ndim == 1:
            return Series(obj)
        else:
            return Series(array(obj).reshape(len(obj)))

    if type_name == 'numpy.ndarray':
        if obj.ndim == 1:
            return Series(obj)
        else:
            return Series(obj.reshape(len(obj)))

    return None


def corr_test(s_list1, s_list2):
    """
    取得两个指定数据序列的相关系数和相关程度
    @param s_list1: 数据序列1
    @param s_list2: 数据序列2
    @:return 相关系数,相关程度描述
    """

    # 强制类型转换为Series
    s_list1 = to_series(s_list1)
    s_list2 = to_series(s_list2)

    # 计算相关系数
    corr = s_list1.corr(s_list2)

    # 根据相关系数判断程度
    if corr >= 0.8:
        corr_level = '高度相关'
    elif corr >= 0.5:
        corr_level = '中度相关'
    elif corr >= 0.3:
        corr_level = '低度相关'
    else:
        corr_level = '不相关'

    # 同时返回两个值
    return corr, corr_level


def scatter_corr(ax, x, y, title, h_align='left', v_align='top', color='black', marker='o'):
    """
    在坐标轴中绘制散点，绘制相关系数和程度
    @param ax: 绘画坐标轴
    @param x: x轴值列表
    @param y: y轴值列表
    @param title: 标题
    @param color: 颜色
    @param marker: 样式
    @param h_align: 指定位置(left,center,right)
    @param v_align: 指定位置(top,middle,bottom)
    @:return 无
    """

    # 散点图
    ax.scatter(x, y, color=color, marker=marker)
    # 设置标题
    ax.set_title(title)
    # 显示相关系数
    corr, corr_level = corr_test(x, y)
    text = '相关系数 : %f\n相关程度 : %s' % (corr, corr_level)
    plotcm.draw_text(ax, x, y, text,
                     color=color, font_size='9', v_align=v_align, h_align=h_align)
