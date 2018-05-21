# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
dict common api
字典相关共通函数
"""

from common import logcm


def get(map, key, default_val=None):
    """
    从字典按指定KEY取值,如果为空则返回默认值
    :param map: 字典
    :param key: 指定KEY
    :param default_val: 默认值
    :return: 值
    """
    # 为空判断
    if map is None or key is None:
        logcm.print_info("Map or key is None!", fg='red')
        return default_val
    # KEY是否存在
    if key not in map:
        return default_val
    # 返回值
    return map[key]
