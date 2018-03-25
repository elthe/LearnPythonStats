#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dataframe common api
Dataframe相关共通函数
"""

from numpy import *


def opr_diff(df, filed_list, diff_num=1, use_log=False):
    """
    把DF数据集指定字段，按照指定差分间隔，计算后插入新的列。
    @param df: 数据集Dataframe
    @param filed_list: 字段名数组
    @param diff_num: 差分相隔数
    @param use_log: 使用对数值计算差分
    @:return 
    """

    df_new = df.copy()
    for field_name in filed_list:
        if use_log:
            s_diff = np.log(df_new[field_name]).diff(diff_num)[diff_num:]
        else:
            s_diff = df_new[field_name].diff(diff_num)[diff_num:]
        df_new.insert(0, field_name + '_diff_' + str(diff_num), s_diff)
    return df_new
