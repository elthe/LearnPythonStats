# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
str common api
字符串相关共通函数
"""

import json
import re
import urllib
import uuid


def uuid():
    """
    UUID字符串
    @return: 全局唯一标识符字符串
    """
    return uuid.uuid1()


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


def bytes2str(input_bytes, encoding="utf-8"):
    """
    字节数组转字符串，优先使用指定编码，其次是用GBK编码，最后使用ASCII码
    @param input_bytes: 输入字节数组
    @param encoding:指定编码
    @return: 字符串
    """

    try:
        out_str = str(input_bytes, encoding=encoding)
        return out_str
    except:
        try:
            out_str = str(input_bytes, encoding='gbk')
            return out_str
        except:
            return "%s" % input_bytes


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


def contains_keys(check_str, key_list):
    """
    判断指定字符串是否包含关键词列表中的关键词
    :param check_str: 判断字符串
    :param key_list: 关键词列表
    :return: True/False
    """
    if check_str is None or key_list is None:
        return False

    for key in key_list:
        if check_str.find(key) >= 0:
            return True

    return False


def remove_space(input_str):
    """
    删除冗余空格
    :param input_str: 输入字符串
    :return: 删除冗余空格后的字符串
    """
    if input_str is None:
        return None

    return " ".join(input_str.split())


def escape_param_str(input_str, add_slash=True):
    """
    把/符号，替换成\/方式
    :param input_str: 输入字符串
    :param add_slash:
    :return: 替换后的字符串
    """
    if input_str is None:
        return None

    if input_str == "$":
        return input_str

    # 把空格等符号还原
    out_str = urllib.parse.unquote(input_str)

    if not add_slash:
        return out_str

    # 把斜杠符号转义
    if out_str.find("/") >= 0:
        out_str = out_str.replace("/", "\\/")

    return "/" + out_str + "/"
