# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
File common api
文件相关共通函数
"""

import os
import codecs
import re

import csv
import xlrd
import shutil

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
        logcm.print_info("Create folder: %s" % path)
        os.makedirs(path)
    # 文件完整路径
    file_path = os.path.join(path, file_name)
    f = codecs.open(file_path, 'w', encoding)
    f.write(content)
    f.close()
    logcm.print_info("Save str file finished. --> %s/%s" % (path, file_name))


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
        logcm.print_info("Create folder: %d" % path)
        os.makedirs(path)
    # 文件完整路径
    file_path = os.path.join(path, file_name)
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

    # 通过文件创建的时候，截取文件所在目录路径
    if by_file:
        (path, file_name) = os.path.split(path)

    # 不存在则创建目标路径
    if not os.path.exists(path):
        os.makedirs(path)


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
        logcm.print_info("File path not exist! %s" % search_path)
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


def load_excel_data(file_path, short_name, sheet_name, title_line, col_titles):
    """
    根据指定路径，Sheet名，标题行，标题列名，读取Excel数据。
    @param file_path: 文件路径
    @param short_name: 文件短名
    @param sheet_name: Sheet名
    @param title_line: 标题行索引
    @param col_titles: 标题列名
    @return: 数据列表
    """

    # 读取Excel
    workbook = xlrd.open_workbook(file_path)
    sheets = workbook.sheet_names()
    if not sheet_name in sheets:
        # 如果没有这个Sheet，则跳过
        logcm.print_info("Sheet不存在 %s - %s" % (short_name, sheet_name))
        return None

    # 读取Sheet
    worksheet = workbook.sheet_by_name(sheet_name)

    # 判断标题行是否在合理范围
    if title_line < 0 or title_line >= worksheet.nrows:
        logcm.print_info("标题行不合理 %d" % title_line)
        return None

    # 标题列
    if not col_titles or len(col_titles) == 0:
        logcm.print_info("标题列未设置 %s" % str(col_titles))
        return None

    # 取得标题行索引
    col_list = []
    for i in range(len(col_titles)):
        title = col_titles[i]
        index = -1
        # 已知字段，查找列
        for j in range(0, worksheet.ncols):
            val = worksheet.cell_value(title_line, j)
            if val == title:
                index = j
                break
        # 索引加入列表
        col_list.append(index)

    # 取得数据
    data_list = []
    for i in range(title_line + 1, worksheet.nrows):
        row_data_list = [short_name]
        # 空字段数
        blank_cnt = 0
        for j in range(len(col_list)):
            index = col_list[j]
            if index >= 0:
                val = worksheet.cell_value(i, index)
                # 加入列数据列表
                row_data_list.append(val)
                # 空字段判断（目前只判断字符串类型）
                if isinstance(val, str) and len(val) == 0:
                    blank_cnt += 1
            else:
                val = ''
                # 加入列数据列表
                row_data_list.append(val)

        # 加入行列表
        if blank_cnt == 0:
            data_list.append(row_data_list)

    return data_list


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
            logcm.print_info("%s not exist!" % src_file)
        else:
            # 分离文件名和路径
            src_path, src_name = os.path.split(src_file)
            # 目标路径
            dest_file = os.path.join(dest_path, src_name)
            # 移动文件
            logcm.print_info("move %s -> %s" % (src_file, dest_file))
            shutil.move(src_file, dest_file)


def copy_files(path_list, dest_path):
    """
    对指定文件列表，复制到指定目录。
    @param path_list: 文件路径列表
    @param dest_path: 目标路径
    @return: 无
    """
    # 创建目标路径
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    # 复制文件
    for src_file in path_list:
        if not os.path.isfile(src_file):
            logcm.print_info("%s not exist!" % src_file)
        else:
            # 分离文件名和路径
            src_path, src_name = os.path.split(src_file)
            # 目标路径
            dest_file = os.path.join(dest_path, src_name)
            # 复制文件
            logcm.print_info("copy %s -> %s" % (src_file, dest_file))
            shutil.copyfile(src_file, dest_file)
