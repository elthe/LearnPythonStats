# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
共通基类定义
"""

import json
from common.datecm import DateEncoder
from prettytable import PrettyTable


class BaseObject:
    """
    共通基类（封装共通处理）
    """

    def props(self):
        """
        取得对象当前属性字典
        """
        return obj_to_dict(self)

    def __str__(self):
        """
        取得对象字符串
        """
        return obj_to_json(self)


def obj_to_json(obj):
    """
    对象转JSON字符串
    :param obj:对象
    :return:JSON字符串
    """
    if isinstance(obj, list):
        return obj_list_to_json(obj)

    # 不是字典时转换成字典
    if isinstance(obj, dict):
        obj_dict = obj
    else:
        obj_dict = obj_to_dict(obj)

    # 把属性转成JSON字符串显示
    json_str = json.dumps(obj_dict, indent=4, cls=DateEncoder)
    # 把Unicode编码转成中文
    out_str = json_str.encode('latin-1').decode('unicode_escape')
    return out_str


def obj_list_to_json(obj_list):
    """
    对象列表转JSON字符串
    :param obj_list:对象列表
    :return:JSON字符串
    """
    dict_list = []
    for obj in obj_list:
        obj_dict = obj_to_dict(obj)
        dict_list.append(obj_dict)
    # 把属性转成JSON字符串显示
    json_str = json.dumps(dict_list, indent=4, cls=DateEncoder)
    # 把Unicode编码转成中文
    out_str = json_str.encode('latin-1').decode('unicode_escape')
    return out_str


def obj_to_dict(obj):
    """
    对象转字典
    :param obj:对象
    :return: 字典
    """
    # 字典对象无需再转
    if isinstance(obj, dict):
        return obj

    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        # 只返回数据属性，不包括方法
        if not name.startswith('__') and not callable(value):
            pr[name] = value
    return pr


def get_name_list(obj):
    """
    取得属性名列表
    :param obj:对象
    :return:属性名列表
    """
    if obj is None:
        return None

    # 字典对象直接返回KEY列表
    if isinstance(obj, dict):
        return obj.keys()

    name_list = []
    for name in dir(obj):
        value = getattr(obj, name)
        # 只返回数据属性，不包括方法
        if not name.startswith('__') and not callable(value):
            name_list.append(name)
    return name_list


def get_val_list(obj, name_list):
    """
    取得属性值列表
    :param obj:对象
    :param name_list:属性名列表
    :return:属性值列表
    """
    if obj is None:
        return None

    if name_list is None or len(name_list) == 0:
        return None

    val_list = []
    for name in name_list:
        # 字典和普通对象取值不同
        if isinstance(obj, dict):
            value = obj[name]
        else:
            value = getattr(obj, name)
        val_list.append(value)
    return val_list


def obj_to_table(obj):
    """
    对象转表格
    :param obj:对象
    :return: 表格对象
    """
    if isinstance(obj, list):
        return obj_list_to_table(obj)

    # 设置表格标题
    table = PrettyTable()
    name_list = get_name_list(obj)
    table.field_names = name_list
    # 设置表格值
    val_list = get_val_list(obj, name_list)
    table.add_row(val_list)

    return table


def obj_list_to_table(obj_list):
    """
    对象转表格
    :param obj_list:对象列表
    :return: 表格对象
    """
    # 设置表格标题
    table = PrettyTable()
    name_list = get_name_list(obj_list[0])
    table.field_names = name_list

    # 设置表格值
    for obj in obj_list:
        table.add_row(get_val_list(obj, name_list))

    return table
