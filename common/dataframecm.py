#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dataframe common api
Dataframe相关共通函数
"""

from numpy import *


def insert_diff(df, field_list, diff_num=1, use_log=False):
    """
    把DF数据集指定字段，按照指定差分间隔，计算后插入新的列。
    @param df: 数据集Dataframe
    @param field_list: 字段名数组
    @param diff_num: 差分相隔数
    @param use_log: 使用对数值计算差分
    @:return 处理后的DF数据集
    """

    df_new = df.copy()
    for field_name in field_list:
        if use_log:
            s_diff = np.log(df_new[field_name]).diff(diff_num)[diff_num:]
        else:
            s_diff = df_new[field_name].diff(diff_num)[diff_num:]
        df_new.insert(0, field_name + '_diff_' + str(diff_num), s_diff)
    return df_new


def insert_field_diff(df, field_1, field_2):
    """
    把DF数据集指定字段相减，并把差分值插入新的列。
    @param df: 数据集Dataframe
    @param field_1: 字段名1
    @param field_2: 字段名2
    @:return 处理后的DF数据集
    """
    df_new = df.copy()

    # 计算差分
    s_diff = df_new[field_1] - df_new[field_2]

    # 新的列名
    field_diff = field_1 + '-' + field_2

    # 插入新的列
    df_new.insert(0, field_diff, s_diff)
    return df_new


def insert_z_score(df, field_list):
    """
    把DF数据集指定字段使用z-score标准化，并把值插入新的列。
    @param df: 数据集Dataframe
    @param field_list: 字段名数组
    @:return 处理后的DF数据集
    """

    df_new = df.copy()
    for field_name in field_list:
        # 计算平均值
        mean_val = np.mean(list(df[field_name]))
        # 计算标准差
        std_val = np.std(list(df[field_name]))

        # 计算标准分数（z-score）：一个分数与平均数的差再除以标准差
        # 标准分数可以回答这样一个问题："一个给定分数距离平均数多少个标准差?"
        # 在平均数之上的分数会得到一个正的标准分数，
        # 在平均数之下的分数会得到一个负的标准分数。
        s_z_score = (df[field_name] - mean_val) / std_val

        # 新的列名
        field_z_score = field_name + '_z_score'

        # 插入新的列
        df_new.insert(0, field_z_score, s_z_score)
    return df_new
