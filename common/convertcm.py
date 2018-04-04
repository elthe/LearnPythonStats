#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convert common api
转换相关共通函数
"""


def to_int(from_data_list):
    """
    列表转换成整数
    @param from_data_list: 元数据列表
    @return: 整数列表
    """
    return convert(from_data_list, lambda x: int(x))


def to_float(from_data_list):
    """
    列表转换成浮点数
    @param from_data_list: 元数据列表
    @return: 浮点数列表
    """
    return convert(from_data_list, lambda x: float(x))


def to_str(from_data_list):
    """
    列表转换成字符串
    @param from_data_list: 元数据列表
    @return: 字符串列表
    """
    return convert(from_data_list, lambda x: str(x))


def convert(from_data_list, convert_func):
    """
    把数据列表，按照指定转换方法转换为新的数据列表
    @param from_data_list: 转换前数据列表
    @param convert_func: 转换方法
    @return: 转换方法
    """

    to_data_list = []
    for from_data in from_data_list:
        to_data = convert_func(from_data)
        to_data_list.append(to_data)
    return to_data_list
