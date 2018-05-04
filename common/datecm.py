#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Date common api
日期相关共通函数
"""

import datetime
from matplotlib.pylab import date2num


def date_list_to_num(dates, format_from='%Y-%m-%d'):
    """
    时间数组转换，字符串转数值
    @param dates: 字符串时间列表
    @param format_from: 字符串源时间格式
    @return: 数值时间列表
    """

    num_time = []
    for date in dates:
        # 日期对象转数字
        num_date = date_to_num(date, format_from)
        num_time.append(num_date)
    return num_time


def date_to_num(date, format_from='%Y-%m-%d'):
    """
    时间数组转换，字符串转数值
    @param date: 字符串时间
    @param format_from: 字符串源时间格式
    @return: 数值时间列表
    """

    # 日期字符串转日期对象
    date_time = datetime.datetime.strptime(date, format_from)
    # 日期对象转数字
    num_date = date2num(date_time)
    return num_date


def date_convert(dates, format_from, format_to):
    """
    时间数组转换，字符串转数值
    @param dates: 字符串时间列表
    @param format_from: 字符串源时间格式
    @param format_to: 字符串目标时间格式
    @return: 转换后字符串时间列表
    """

    date_list = []
    for date in dates:
        # 日期字符串转日期对象
        date_time = datetime.datetime.strptime(date, format_from)
        # 日期对象转数字
        date_new = date_time.strftime(format_to)
        date_list.append(date_new)
    return date_list


def now_time_str(format='%Y%m%d%H%M%S'):
    """
    取得当前时间的时间字符串
    @param format: 时间格式
    @return: 时间字符串
    """

    now_time = datetime.datetime.now().strftime(format)
    return now_time


def get_now_num():
    """
    取得当前时间的时间字符串
    @param format: 时间格式
    @return: 时间字符串
    """

    now_time = datetime.datetime.now()
    return date2num(now_time)
