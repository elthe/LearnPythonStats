#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Date common api
日期相关共通函数
"""

import datetime
from matplotlib.pylab import date2num


def date_to_num(dates):
    num_time = []
    for date in dates:
        # 日期字符串转日期对象
        date_time = datetime.datetime.strptime(date, '%Y-%m-%d')
        # 日期对象转数字
        num_date = date2num(date_time)
        num_time.append(num_date)
    return num_time
