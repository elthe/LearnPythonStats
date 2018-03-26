# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
File common api
文件相关共通函数
"""

import os
import codecs


def save_str(content, encoding, path, file_name):
    """
    保存字符串到文件
    @param content: 字符串内容
    @param encoding: 字符串编码
    @param path: 文件路径
    @param file_name: 文件名
    @return: 无
    """

    # 本地文件路径如果不存在，自动创建
    if not os.path.exists(path):
        print("Create folder: " + path)
        os.makedirs(path)
    # 文件完整路径
    file_path = str(path + '/' + file_name)
    f = codecs.open(file_path, 'w', encoding)
    f.write(content)
    f.close()


def save_data(data, path, file_name):
    """
    保存数据到本地文件
    @param data: 数据内容
    @param path: 文件路径
    @param file_name: 文件名
    @return: 无
    """

    # 本地文件路径如果不存在，自动创建
    if not os.path.exists(path):
        print("Create folder: " + path)
        os.makedirs(path)
    # 文件完整路径
    file_path = str(path + "/" + file_name)
    with open(file_path, "wb") as file:
        file.write(data)


def exists(path, file_name):
    """
    判断本地文件是否存在
    @param path: 文件路径
    @param file_name: 文件名
    @return: True/False
    """

    # 本地文件路径如果不存在，返回False
    if not os.path.exists(path):
        return False
    # 文件完整路径
    file_path = str(path + "/" + file_name)
    return os.path.exists(file_path)


def read_lines(path, file_name, encoding):
    """
    读取文件到字符串数组
    @param path: 文件路径
    @param file_name: 文件名
    @param encoding: 字符编码
    @return: 字符串数组
    """

    file_path = path + '/' + file_name
    file = codecs.open(file_path, 'r', encoding)
    lines = [line.strip() for line in file]
    file.close()
    return lines


def read_str(path, file_name, encoding):
    """
    读取文件到字符串
    @param path: 文件路径
    @param file_name: 文件名
    @param encoding: 字符编码
    @return: 字符串
    """

    lines = read_lines(path, file_name, encoding)
    all_str = '\n'.join(lines)
    return all_str
