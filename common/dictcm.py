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


def getInt(map, key, default_val=None):
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
    return int(map[key])


def isSame(mapSrc, mapTar):
    """
    判断源字典内容是否和目标字典一样
    :param mapSrc: 源字典
    :param mapTar: 目标字典
    :return: 是否一致
    """
    if mapSrc is None and mapTar is None:
        return None
    if mapSrc is None or mapTar is None:
        return False
    for key in mapTar.keys():
        if key in mapSrc:
            if mapSrc[key] != mapTar[key]:
                return False
        else:
            return False
    return True


def isExist(mapList, map):
    """
    判断字典内容在字典列表中是否存在
    :param mapList: 字典列表
    :param map: 字典
    :return: 是否存在
    """
    if mapList is None or map is None:
        return False
    if len(mapList) == 0:
        return False
    for item in mapList:
        if isSame(item, map):
            return True
    return False


def findKeys(map, searchKey):
    """
    在字典中搜索符合检索条件的KEY列表
    :param map: 字典
    :param searchKey: 检索KEY
    :return: 符合条件的KEY列表
    """
    if map is None or searchKey is None:
        return False

    keys = []
    for key in map.keys():
        pos = key.find(searchKey)
        if pos >= 0:
            keys.append(key)

    return keys
