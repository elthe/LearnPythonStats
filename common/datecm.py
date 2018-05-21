#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Date common api
日期相关共通函数

日期格式字符串说明:
    %y 两位数的年份表示（00-99）
    %Y 四位数的年份表示（000-9999）
    %m 月份（01-12）
    %d 月内中的一天（0-31）
    %H 24小时制小时数（0-23）
    %I 12小时制小时数（01-12）
    %M 分钟数（00=59）
    %S 秒（00-59）
    %a 本地简化星期名称
    %A 本地完整星期名称
    %b 本地简化的月份名称
    %B 本地完整的月份名称
    %c 本地相应的日期表示和时间表示
    %j 年内的一天（001-366）
    %p 本地A.M.或P.M.的等价符
    %U 一年中的星期数（00-53）星期天为星期的开始
    %w 星期（0-6），星期天为星期的开始
    %W 一年中的星期数（00-53）星期一为星期的开始
    %x 本地相应的日期表示
    %X 本地相应的时间表示
    %Z 当前时区的名称

"""

import datetime
import time
from xlrd import xldate_as_tuple
from matplotlib.pylab import date2num, num2date


def check_date_format(date_str, check_format):
    """
    校验日期字符串格式是否和指定格式一致
    :param date_str: 日期字符串
    :param check_format:校验格式
    :return:是否一致
    """
    try:
        # 日期字符串转日期对象
        datetime.datetime.strptime(date_str, check_format)
        return True
    except Exception as e:
        return False


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


def num_to_date(num):
    """
    数字转日期
    :param num: 数字
    :return:日期对象
    """
    return num2date(num)


def xldate_to_date(cell):
    date = datetime(*xldate_as_tuple(cell, 0))
    return date


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


def get_now_time(time_type="second"):
    """
    取得当前时间的时间戳数值。
    @param time_type: 时间类型(origin 原始，second 秒，mini 毫秒)
    @return: 时间数值
    """

    t = time.time()
    if time_type == "origin":
        # 原始时间数据
        return t
    elif time_type == "second":
        # 秒级时间戳
        return int(t)
    elif time_type == "mini":
        # 毫秒级时间戳
        return int(round(t * 1000))
