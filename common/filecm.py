# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
File common api
文件相关共通函数
"""

import codecs
import csv
import os
import re
import shutil
import datetime


from common import logcm


def extension(path):
    """
    根据文件路径取得后缀名
    @param path: 文件路径
    @return: 文件后缀名
    """
    (file_path, file_name) = os.path.split(path)
    (short_name, extension) = os.path.splitext(file_name)
    return extension


def short_name(path):
    """
    根据文件路径取得短文件名（不含路径和后缀）
    @param path: 文件路径
    @return: 短文件名
    """
    (file_path, file_name) = os.path.split(path)
    (short_name, extension) = os.path.splitext(file_name)
    return short_name


def save_str(content, encoding='utf-8', path=None, file_name=None):
    """
    保存字符串到文件
    @param content: 字符串内容
    @param encoding: 字符串编码
    @param path: 文件路径
    @param file_name: 文件名
    @return: 无
    """

    # 文件名为空返回空
    if file_name is None:
        logcm.print_info("File name is empty.", fg='red')
        return None

    # 路径不为空，路径拼接
    if path is not None:
        makedir(path)
        file_path = os.path.join(path, file_name)
    else:
        makedir(file_name, by_file=True)
        file_path = file_name

    # 文件完整路径
    f = codecs.open(file_path, 'w', encoding)
    f.write(content)
    f.close()
    logcm.print_info("Save str file finished. --> %s/%s" % (path, file_name))


def save_data(data, path=None, file_name=None):
    """
    保存数据到本地文件
    @param data: 数据内容
    @param path: 文件路径
    @param file_name: 文件名
    @return: 无
    """

    # 文件名为空返回空
    if file_name is None:
        logcm.print_info("File name is empty.", fg='red')
        return None

    # 路径不为空，路径拼接
    if path is not None:
        makedir(path)
        file_path = os.path.join(path, file_name)
    else:
        makedir(file_name, by_file=True)
        file_path = file_name

    # 文件完整路径
    with open(file_path, "wb") as file:
        file.write(data)
    logcm.print_info("Save data file finished. --> %s/%s" % (path, file_name))


def append_csv(csv_path, data_list):
    """
    把数据列表追加写入到csv文件
    @param csv_path: 文件路径
    @param data_list: 数据列表
    @return: 无
    """

    # 打开CSV文件
    out = open(csv_path, "a", newline="")
    # 启动CSV写入
    csv_writer = csv.writer(out, dialect="excel")
    # 遍历写入行
    for row in data_list:
        csv_writer.writerow(row)

    logcm.print_info("Append csv file finished. --> %s" % csv_path)
    return None


def exists(path_check, file_name):
    """
    判断本地文件是否存在
    @param path_check: 文件路径
    @param file_name: 文件名
    @return: True/False
    """

    # 本地文件路径如果不存在，返回False
    if not os.path.exists(path_check):
        return False

    # 文件完整路径
    file_path = os.path.join(path_check, file_name)
    return os.path.exists(file_path)


def makedir(path, by_file=False):
    """
    确保目标路径存在，不存在则创建。
    @param path: 目标路径
    @param by_file: 通过文件的路径创建
    @return: 无
    """

    # 路径为空，返回
    if path is None:
        return

    # 通过文件创建的时候，截取文件所在目录路径
    if by_file:
        (path, file_name) = os.path.split(path)

    # 不存在则创建目标路径
    if not os.path.exists(path):
        logcm.print_info("Create folder: %s" % path)
        os.makedirs(path)


def read_lines(path=None, file_name=None, encoding="utf-8"):
    """
    读取文件到字符串数组
    @param path: 文件路径
    @param file_name: 文件名
    @param encoding: 字符编码
    @return: 字符串数组
    """

    # 文件名为空返回空
    if file_name is None:
        logcm.print_info("File name is empty.", fg='red')
        return None

    # 路径不为空，路径拼接
    if path is not None:
        file_path = os.path.join(path, file_name)
    else:
        file_path = file_name

    # 文件不存在，返回空
    if not os.path.exists(file_path):
        logcm.print_info("File not found. %s" % file_path, fg='red')
        return None

    # 读取文件
    file = codecs.open(file_path, 'r', encoding)
    # 行字符串列表
    lines = [line.strip() for line in file]
    file.close()
    return lines


def read_str(path=None, file_name=None, encoding="utf-8"):
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


def read_bytes(path=None, file_name=None):
    """
    读取文件到字节数组
    @param path: 文件路径
    @param file_name: 文件名
    @return: 字节数组
    """
    # 文件名为空返回空
    if file_name is None:
        logcm.print_info("File name is empty.", fg='red')
        return None

    # 路径不为空，路径拼接
    if path is not None:
        file_path = os.path.join(path, file_name)
    else:
        file_path = file_name

    # 读取字节数组
    file_object = open(file_path, 'rb')
    bytes = file_object.read()
    return bytes


def search_files(search_path, ext=None, match=None):
    """
    对指定目录进行文件检索，返回满足条件的文件路径一览。
    @param search_path: 检索路径
    @param ext: 文件扩展名，逗号分隔，如果为空，则返回所有文件。
    @param match: 文件名的规则表达式（可选）
    @return: 文件路径一览
    """

    # 判断路径是否cun在
    if not os.path.exists(search_path):
        logcm.print_info("File path not exist! %s" % search_path, fg='red')
        return None

    # 后缀名如果有指定，生成允许列表
    ext_list = ext.split(',') if ext else None

    # 路径列表
    path_list = []
    for (root, dirs, files) in os.walk(search_path):
        for file_name in files:
            # 允许列表如果有内容
            if ext_list:
                # 文件后缀
                (short_name, extension) = os.path.splitext(file_name)
                # 后缀不在允许列表中，则跳过
                if extension not in ext_list:
                    continue

            # 规则表达式匹配
            if match:
                # 不匹配，则跳过
                if not re.match(match, file_name):
                    continue

            # 文件路径
            file_path = os.path.join(root, file_name)
            path_list.append(file_path)

    # 返回路径列表
    return path_list


def move_files(path_list, dest_path):
    """
    对指定文件列表，移动到指定目录。
    @param path_list: 文件路径列表
    @param dest_path: 目标路径
    @return: 无
    """
    # 创建目标路径
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    # 移动文件
    for src_file in path_list:
        if not os.path.isfile(src_file):
            logcm.print_info("%s not exist!" % src_file, fg='red')
        else:
            # 分离文件名和路径
            src_path, src_name = os.path.split(src_file)
            # 目标路径
            dest_file = os.path.join(dest_path, src_name)
            # 移动文件
            logcm.print_info("move %s -> %s" % (src_file, dest_file))
            shutil.move(src_file, dest_file)


def copy_files(path_list, dest_path, skeep_exist=False):
    """
    对指定文件列表，复制到指定目录。
    @param path_list: 文件路径列表
    @param dest_path: 目标路径
    @param skeep_exist: 跳过已经存在的文件
    @return: 无
    """
    # 创建目标路径
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    # 复制文件
    for src_file in path_list:
        if not os.path.isfile(src_file):
            logcm.print_info("%s not exist!" % src_file, fg='red')
        else:
            # 分离文件名和路径
            src_path, src_name = os.path.split(src_file)
            # 目标路径
            dest_file = os.path.join(dest_path, src_name)
            # 跳过已经存在的文件
            if skeep_exist and os.path.exists(dest_file):
                continue
            # 复制文件
            logcm.print_info("copy %s -> %s" % (src_file, dest_file))
            shutil.copyfile(src_file, dest_file)


def remove(path=None, file_name=None):
    """
    删除文件
    @param path: 文件路径
    @param file_name: 文件名
    @return: 无
    """

    # 判断文件是否存在
    file_path = os.path.join(path, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        logcm.print_info("文件不存在:%s" % file_path)


def last_update_time(path=None, file_name=None):
    """
    最近更新时间
    @param path: 文件路径
    @param file_name: 文件名
    @return: 无
    """

    # 判断文件是否存在
    file_path = os.path.join(path, file_name)
    if os.path.exists(file_path):
        statinfo = os.stat(file_path)
        updateTime = datetime.datetime.fromtimestamp(statinfo.st_mtime)
        return updateTime
    else:
        logcm.print_info("文件不存在:%s" % file_path)
        return None
