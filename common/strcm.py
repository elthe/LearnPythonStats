# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
str common api
字符串相关共通函数
"""


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
