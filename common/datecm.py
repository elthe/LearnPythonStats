#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Date common api
日期相关共通函数
"""

import datetime
from matplotlib.pylab import date2num


def date_to_num(dates):
    """
    时间数组转换，字符串转数值
    @param dates: 字符串时间列表
    @return: 数值时间列表
    """
    num_time = []
    for date in dates:
        # 日期字符串转日期对象
        date_time = datetime.datetime.strptime(date, '%Y-%m-%d')
        # 日期对象转数字
        num_date = date2num(date_time)
        num_time.append(num_date)
    return num_time


def now_time_str(format='%Y%m%d%H%M%S'):
    """
    取得当前时间的时间字符串
    @param format: 时间格式
    @return: 时间字符串
    """
    now_time = datetime.datetime.now().strftime(format)
    return now_time
