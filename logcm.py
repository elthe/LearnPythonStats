#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Log common api
日志输出相关共通函数
"""

from numpy import *


def print_obj(obj, title, full=False):
    """
    print输出对象内容，同时输出描述，类型
    @param obj: 输出对象
    @param title: 对象的标题
    @param full: 全部显示，默认否
    @:return 无
    """

    # 取得对象类型名称
    type_name = get_type_name(obj)

    print('\n')
    print('-' * 100)
    print('      obj : %s' % title)
    print('     type : %s' % type_name)
    # 属性输出
    print_obj_prop(obj, type_name)

    # 开始线
    print('-' * 100)
    # 输出对象数据
    print_obj_data(obj, type_name, full)
    # 结束线
    print('-' * 100)
    return None


def get_type_name(obj):
    """
    取得类型名称
    @param obj : 对象
    @:return 对象类型名
    """

    type_str = '%s' % type(obj)
    type_name = type_str[8:-2]
    return type_name


def print_obj_prop(obj, type_name):
    """
    根据类型输出属性
    @param obj : 输出对象
    @:return 无
    """

    if type_name == 'pandas.core.frame.DataFrame':
        print('     size : %d' % obj.size)
        print('     ndim : %d' % obj.ndim)
        print('    shape : ', end='')
        print(obj.shape)

    if type_name == 'pandas.core.series.Series':
        print('     size : %d' % obj.size)
        print('     ndim : %d' % obj.ndim)
        print('    shape : ', end='')
        print(obj.shape)

    if type_name == 'list':
        print('      len : %d' % len(obj))
        print('     ndim : %d' % array(obj).ndim)
        print('    shape : ', end='')
        print(array(obj).shape)

    if type_name == 'numpy.ndarray':
        print('      len : %d' % len(obj))
        print('     ndim : %d' % obj.ndim)
        print('    shape : ', end='')
        print(obj.shape)

    return None


def print_obj_data(obj, type_name, full):
    """
    print数据对象，根据类型进行特殊处理
    @param obj : 对象
    @param type_name : 类型名
    @param full : 是否全部显示
    @:return 无
    """

    if full == False:
        # 打印列表
        if type_name == 'list':
            if array(obj).ndim > 1:
                return print_matrix_data(obj, 40)
            else:
                return print_list_data(obj, 60)

        if type_name == 'numpy.ndarray':
            if obj.ndim > 1:
                return print_matrix_data(obj.tolist(), 40)
            else:
                return print_list_data(obj.tolist(), 60)

    print(obj)
    return None


def print_list_data(list, max):
    """
    print列表数据对象
    @param list : 列表对象
    @param max : 最大显示数（超过后省略显示）
    @:return 无
    """

    # 小于最大数量时，直接输出
    if len(list) <= max:
        print(list)
        return None
    # 一半
    half = round(max / 2)

    # 截取头尾
    heads = '%s' % list[:half]
    tails = '%s' % list[-1 * half:]

    print('[', end='')
    print(heads[1:-1])
    print(' ... ')
    print(tails[1:-1], end='')
    print(']')
    return None


def print_matrix_data(mat, max):
    """
    print矩阵数据对象
    @param mat : 矩阵对象
    @param max : 最大显示数（超过后省略显示）
    @:return 无
    """

    # 小于最大数量时，直接输出
    if len(mat) <= max:
        print(mat)
        return None
    # 一半
    half = round(max / 2)

    # 截取头尾
    heads = mat[:half]
    tails = mat[-1 * half:]

    print('[')
    for i in range(len(heads)):
        print(heads[i])

    print(' ... ')

    for i in range(len(tails)):
        print(tails[i])
    print(']')
    return None
