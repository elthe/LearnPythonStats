#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Log common api
日志输出相关共通函数
"""

from numpy import *

colors_dict = {
    'reset': '0',
    'bold': '1',
    'disable': '2',
    'underline': '4',
    'reverse': '7',
    'strikethrough': '9',
    'invisible': '8',
}

fg_dict = {
    'black': '30',
    'red': '31',
    'green': '32',
    'orange': '33',
    'blue': '34',
    'purple': '35',
    'cyan': '36',
    'lightgrey': '37',
    'darkgrey': '90',
    'lightred': '91',
    'lightgreen': '92',
    'yellow': '93',
    'lightblue': '94',
    'pink': '95',
    'lightcyan': '96',
}

bg_dict = {
    'black': '40',
    'red': '41',
    'green': '42',
    'orange': '43',
    'blue': '44',
    'purple': '45',
    'cyan': '46',
    'lightgrey': '47'
}


def set_style(color=None, fg=None, bg=None):
    """
    设置特殊输出样式
    @param color: 颜色
    @param fg: 前景色
    @param bg: 背景色
    @:return 有无特殊样式
    """

    has_style = False
    # 颜色
    if color is None:
        clr_k = 'reset'
        clr_v = colors_dict[clr_k]
    elif color in colors_dict:
        clr_k = color
        clr_v = colors_dict[clr_k]
        has_style = True
    else:
        clr_v = color
        has_style = True

    # 前景色
    if fg is not None:
        if fg in fg_dict:
            fg_k = fg
            fg_v = fg_dict[fg_k]
            has_style = True
        else:
            fg_v = fg
            has_style = True
    else:
        fg_v = ''

    # 背景色
    if bg is not None:
        if bg in bg_dict:
            bg_k = bg
            bg_v = bg_dict[bg_k]
            has_style = True
        else:
            bg_v = bg
            has_style = True
    else:
        bg_v = ''

    if has_style:
        # 输出格式
        print('\033[%s;%s;%sm' % (clr_v, fg_v, bg_v))

    return has_style


def print_info(obj, blank_first=True, show_header=True, color=None, fg=None, bg=None):
    """
    print输出信息
    @param obj: 输出信息
    @param blank_first: 开头是否输出空行
    @param show_header: 是否显示头部
    @param color: 颜色
    @param fg: 前景色
    @param bg: 背景色
    @:return 无
    """

    # 显示头部
    if show_header:
        # 输出新的空行
        if blank_first:
            print('\n')
        # 开始线
        print('-' * 100)

    # 输出信息
    print('----\t', end='')

    # 开始特殊显示
    has_style = set_style(color, fg, bg)

    # 输出对象
    print(obj)

    # 结束特殊显示
    if has_style:
        # 清除格式
        print('\033[0m')

    # 结束线
    print('-' * 100)


def print_obj(obj, title, full_show=False, show_header=True, color=None, fg=None, bg=None):
    """
    print输出对象内容，同时输出描述，类型
    @param obj: 输出对象
    @param title: 对象的标题
    @param full_show: 全部显示，默认否
    @param show_header: 是否显示头部
    @param color: 颜色
    @param fg: 前景色
    @param bg: 背景色
    @:return 无
    """

    # 取得对象类型名称
    type_name = get_type_name(obj)

    # 显示头部
    if show_header:
        print('\n')
        print('-' * 100)

    # 开始特殊显示
    has_style = set_style(color, fg, bg)

    print('      obj : %s' % title)
    print('     type : %s' % type_name)
    # 属性输出
    print_obj_prop(obj, type_name)

    # 开始线
    print('-' * 100)
    # 输出对象数据
    print_obj_data(obj, type_name, full_show)

    # 结束特殊显示
    if has_style:
        # 清除格式
        print('\033[0m')

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

    if type_name == 'urllib.request.Request':
        print('      url : %s' % obj.full_url)
        print('     type : %s' % obj.type)
        print('  headers : %s' % obj.headers)
        print('     data : %s' % obj.data)

    if type_name == 'http.client.HTTPResponse':
        print('   status : %d' % obj.status)
        print('  headers : %s' % obj.getheaders())

    return None


def print_obj_data(obj, type_name, full_show):
    """
    print数据对象，根据类型进行特殊处理
    @param obj : 对象
    @param type_name : 类型名
    @param full_show : 是否全部显示
    @:return 无
    """

    if full_show == False:
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


def print_list_data(list_obj, max_num):
    """
    print列表数据对象
    @param list_obj : 列表对象
    @param max_num : 最大显示数（超过后省略显示）
    @:return 无
    """

    # 小于最大数量时，直接输出
    if len(list_obj) <= max_num:
        print(list_obj)
        return None
    # 一半
    half = round(max_num / 2)

    # 截取头尾
    heads = '%s' % list_obj[:half]
    tails = '%s' % list_obj[-1 * half:]

    print('[', end='')
    print(heads[1:-1])
    print(' ... ')
    print(tails[1:-1], end='')
    print(']')
    return None


def print_matrix_data(mat_obj, max_num):
    """
    print矩阵数据对象
    @param mat_obj : 矩阵对象
    @param max_num : 最大显示数（超过后省略显示）
    @:return 无
    """

    # 小于最大数量时，直接输出
    if len(mat_obj) <= max_num:
        print(mat_obj)
        return None
    # 一半
    half = round(max_num / 2)

    # 截取头尾
    heads = mat_obj[:half]
    tails = mat_obj[-1 * half:]

    print('[')
    for i in range(len(heads)):
        print(heads[i])

    print(' ... ')

    for i in range(len(tails)):
        print(tails[i])
    print(']')
    return None
