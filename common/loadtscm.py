# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Tushare Load Common
TuShare用数据加载共通
"""

import os
import tushare as ts
import pandas as pd

from matplotlib.pylab import date2num
from common import logcm
from common import filecm
from common import datecm


def get_cpi(start_month, end_month):
    """
    取得居民消费价格指数
    @param start_month: 开始月份YYYY.M
    @param end_month: 结束月份YYYY.M
    @return: 指定月份范围的CPI数据集
    """

    # 日期格式
    date_format = '%Y.%m'
    # 文件路径
    file_path = './cache/ts_cpi.csv'
    # 如果存在数据文件，则直接读取
    if os.path.exists(file_path):
        # 读取文件
        df_cpi = pd.read_csv(file_path, dtype={'month': str, 'cpi': float, 'month_num': int})
    else:
        # 取得CPI数据
        df_cpi = ts.get_cpi()
        # 把日期转成Num
        month_num_list = datecm.date_list_to_num(df_cpi["month"], date_format)
        # 插入新的列
        df_cpi.insert(2, 'month_num', month_num_list)
        # 保存到文件
        df_cpi.to_csv(file_path, index=False)

    # 对开始结束日期计算
    start = datecm.date_to_num(start_month, date_format)
    end = datecm.date_to_num(end_month, date_format)
    # 根据开始结束时间数据筛选
    df_result = df_cpi.ix[df_cpi.month_num >= start, :]
    df_result = df_result.ix[df_cpi.month_num <= end, :]

    # 按照日期数值排正序
    df_result = df_result.sort_values(by=['month_num'])
    # 返回数据集
    return df_result


def month_boxoffice(month):
    """
    查询当月票房
    @param month: 查询月份YYYY-M
    @return: 指定月份的票房信息
    """

    # 文件路径
    file_path = './cache/ts_month_boxoffice_%s.csv' % month
    # 如果存在数据文件，则直接读取
    if os.path.exists(file_path):
        # 读取文件
        df_month = pd.read_csv(file_path)
    else:
        # 取得票房数据
        df_month = ts.month_boxoffice(month)
        # 保存到文件
        df_month.to_csv(file_path, index=False)

    return df_month
