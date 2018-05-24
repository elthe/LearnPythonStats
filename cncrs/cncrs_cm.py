#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CNCRS 非居民金融账户涉税信息报送处理共通
"""


def convert(convert_key, val_from, val_map=None):
    """
    根据数据转换字典进行转换.
    :param convert_key:转换KEY
    :param val_from:转换前的值
    :param val_map:数据转换字典
    :return:转换后的值
    """
    if val_from is None or convert_key is None:
        return ""

    # 国家代码,取前两位
    if convert_key == "country":
        return val_from[0:2]
    # 日期转换
    if convert_key == "date":
        return val_from.strftime("%Y-%m-%d")
    # KEY-NAME
    if convert_key == "key-name":
        return val_from.split("-")[0]

    # 转换
    if val_map and convert_key in val_map:
        if val_from in val_map[convert_key]:
            val_to = val_map[convert_key][val_from]
            return val_to
    return ""


def get_message_type_indic(new_data=True, no_data=False):
    """
    取得申报数据类型
    :param new_data: 是否新数据
    :param no_data:是否无申报
    :return:
    """
    if new_data:
        # 新数据
        return "CRS701"
    else:
        if not no_data:
            # 修改或删除数据
            return "CRS702"
        else:
            # 零申报
            return "CRS703"
