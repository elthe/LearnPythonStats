# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
共通基类定义
"""

import datetime
import json
from prettytable import PrettyTable


class BaseJSONEncoder(json.JSONEncoder):
    """
    JSON日期编码类
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.__str__()
        if isinstance(obj, BaseObject):
            return obj_to_dict(obj)
        return json.JSONEncoder.default(self, obj)


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

    def copy_from(self, obj):
        """
        从对象或字典复制值
        :param obj: 对象或字典
        :return: 无
        """
        copy_val(obj, self)


def copy_val(obj_from, obj_to):
    """
    对象或字典之间复制值
    :param obj_from:源对象或字典
    :param obj_to:目标对象或字典
    :return: 无
    """
    if obj_from is None or obj_to is None:
        return

    # 字典对象无需再转
    if isinstance(obj_from, dict):
        dict_from = obj_from
    else:
        dict_from = obj_to_dict(obj_from)

    # 如果目标是字典,直接更新
    if isinstance(obj_to, dict):
        obj_to.update(dict_from)
        return

    # 非字典时,对目标的所有属性循环
    name_list = get_name_list(obj_to)
    for name in name_list:
        # 如果属性名在源对象或字典中存在的话,设置属性值
        if name in dict_from:
            setattr(obj_to, name, dict_from[name])
    return


def obj_to_json(obj):
    """
    对象转JSON字符串
    :param obj:对象
    :return:JSON字符串
    """
    if obj is None:
        return None

    if isinstance(obj, list):
        return obj_list_to_json(obj)

    # 不是字典时转换成字典
    if isinstance(obj, dict):
        obj_dict = obj
    else:
        obj_dict = obj_to_dict(obj)

    # 把属性转成JSON字符串显示
    json_str = json.dumps(obj_dict, indent=4, cls=BaseJSONEncoder)
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
    json_str = json.dumps(dict_list, indent=4, cls=BaseJSONEncoder)
    # 把Unicode编码转成中文
    out_str = json_str.encode('latin-1').decode('unicode_escape')
    return out_str


def obj_to_dict(obj):
    """
    对象转字典
    :param obj:对象
    :return: 字典
    """
    if obj is None:
        return None

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


def matrix_to_dict(matrix, name_list):
    """
    矩阵转字典列表
    :param matrix:矩阵
    :param name_list:名称列表
    :return:字典列表
    """
    if matrix is None or name_list is None:
        return None

    dict_list = []
    for row_list in matrix:
        dict_data = list_to_dict(row_list, name_list)
        dict_list.append(dict_data)
    return dict_list


def list_to_dict(val_list, name_list):
    """
    值和名称列表转字典
    :param val_list:值列表
    :param name_list: 名称列表
    :return: 字典
    """
    if val_list is None or name_list is None:
        return None

    if len(val_list) != len(name_list):
        return None

    # 按照名称和值修改数据字典
    dict_data = {}
    for i in range(len(val_list)):
        key = name_list[i]
        dict_data[key] = val_list[i]
    return dict_data


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
