# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
str common api
字符串相关共通函数
"""

import json
import re


def pad_after(input_str, padding_size, padding_char=" "):
    """
    字符串末尾补齐
    @param input_str: 输入字符串
    @param padding_size: 对齐宽度
    @param padding_char: 补齐字符
    @return: 补齐后的字符串
    """

    adding_num = padding_size - len(input_str) % padding_size
    suffix_str = padding_char * adding_num
    return input_str + suffix_str


def is_json(input_str):
    """
    判断字符串是否JSON格式
    @param input_str: 输入字符串
    @return: 是否JSON格式
    """

    try:
        json.loads(input_str)
    except ValueError:
        return False
    return True


def upper_first(input_str):
    """
    首字母转大写
    @param input_str: 输入字符串
    @return: 转换后的字符串
    """
    if input_str is None:
        return ""

    if not isinstance(input_str, str):
        return ""

    if len(input_str) > 1:
        out_str = input_str[0].upper() + input_str[1:]
    else:
        out_str = input_str.upper()

    return out_str


def camel_to_under(camel_str):
    """
    驼峰字符串转下划线字符串
    如：aaaBbbCcc -> aaa_bbb_ccc
    :param camel_str:驼峰字符串
    :return:下划线字符串
    """
    if camel_str is None:
        return ""

    if not isinstance(camel_str, str):
        return ""

    # 匹配正则，匹配小写字母和大写字母的分界位置
    p = re.compile(r'([a-z]|\d)([A-Z])')
    # 这里第二个参数使用了正则分组的后向引用
    sub = re.sub(p, r'\1_\2', camel_str).lower()
    return sub


def under_to_camel(under_str):
    """
    下划线形式字符串转成驼峰形式
    如：aaa_bbb_ccc -> aaaBbbCcc
    :param under_str: 下划线形式字符串
    :return: 驼峰形式字符串
    """
    if under_str is None:
        return ""

    if not isinstance(under_str, str):
        return ""

    # 这里re.sub()函数第二个替换参数用到了一个匿名回调函数，
    # 回调函数的参数x为一个匹配对象，返回值为一个处理后的字符串
    sub = re.sub(r'(_\w)', lambda x: x.group(1)[1].upper(), under_str)
    return sub
