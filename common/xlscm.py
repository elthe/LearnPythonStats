# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Excel common api
Excel文件相关共通函数
"""

import os
import xlrd
from common import filecm
from common import logcm
from common import checkcm
from common.classcm import BaseObject
from datetime import datetime
from xlrd import xldate_as_tuple
from xlwt import *


class ExcelDiffInfo(BaseObject):
    """
    Excel不同点类
    """

    def __init__(self, row, col, key, title, val_from, val_to):
        # 行号
        self.row = row
        # 列号
        self.col = col
        # 列号
        self.key = key
        # 标题
        self.title = title
        # 当前值
        self.val_from = val_from
        # 对比值
        self.val_to = val_to


def cmp_excel(left_file_path, right_file_path, sheet_name, title_line, start_line, pk_col, start_col=0,
              ignore_new_line=False):
    """
    比较两个Excel文件指定Sheet,从指定行开始的数据,如果指定主键列值相同,比较数据有无不同.如果主键值不存在,列出所有数据.
    :param left_file_path:左文件路径
    :param right_file_path:右文件路径
    :param sheet_name:Sheet名
    :param title_line:标题行号
    :param start_line:数据开始行号
    :param pk_col:主键列号
    :return:差分列表
    """

    # 读取Sheet
    sheet_left = get_sheet(left_file_path, sheet_name)
    sheet_right = get_sheet(right_file_path, sheet_name)

    is_ok = True
    is_ok &= check_row(sheet_left, title_line, "标题行")
    is_ok &= check_row(sheet_right, title_line, "标题行")
    is_ok &= check_row(sheet_left, start_line, "数据开始行")
    is_ok &= check_row(sheet_right, start_line, "数据开始行")
    is_ok &= check_col(sheet_left, pk_col, "主键列")
    is_ok &= check_col(sheet_right, pk_col, "主键列")
    is_ok &= check_col(sheet_left, start_col, "开始列")
    is_ok &= check_col(sheet_right, start_col, "开始列")
    if not is_ok:
        return

    # 差分列表
    diff_list = []
    for row_left in range(start_line, sheet_left.nrows):
        # 主键值
        pk_val = sheet_left.cell_value(row_left, pk_col)
        if pk_val is None or pk_val == "":
            break

        row_right = find_row_by_pk(sheet_right, pk_col, start_line, pk_val)
        if row_right is not None:
            for col_left in range(start_col, sheet_left.ncols):
                val_left = sheet_left.cell_value(row_left, col_left)
                val_right = sheet_right.cell_value(row_right, col_left)
                if val_left != val_right:
                    title = sheet_left.cell_value(title_line, col_left)
                    diff = ExcelDiffInfo(row_left, col_left, pk_val, title, val_left, val_right)
                    diff_list.append(diff)
        elif not ignore_new_line:
            for col_left in range(start_col, sheet_left.ncols):
                val_left = sheet_left.cell_value(row_left, col_left)
                title = sheet_left.cell_value(title_line, col_left)
                diff = ExcelDiffInfo(row_left, col_left, pk_val, title, val_left, None)
                diff_list.append(diff)

    return diff_list


def find_row_by_pk(sheet, pk_col, start_line, pk_val):
    for row in range(start_line, sheet.nrows):
        val = sheet.cell_value(row, pk_col)
        if val == pk_val:
            return row
    return None


def check_row(sheet, row, title):
    # 判断标题行是否在合理范围
    if row < 0 or row >= sheet.nrows:
        logcm.print_info("%s的行号不合理! 正常范围:[0~%d), 当前值:%d" % (title, sheet.nrows, row), fg='red')
        return False
    return True


def check_col(sheet, col, title):
    # 判断标题行是否在合理范围
    if col < 0 or col >= sheet.ncols:
        logcm.print_info("%s的列号不合理! 正常范围:[0~%d), 当前值:%d" % (title, sheet.ncols, col), fg='red')
        return False
    return True


def get_sheet(file_path, sheet_name):
    """
    取得指定excel文件的Sheet
    :param file_path: Excel文件路径
    :param sheet_name: Sheet名
    :return: Sheet对象
    """
    if not os.path.exists(file_path):
        logcm.print_info("文件不存在! %s" % file_path, fg='red')
        return None

    # 读取Excel
    workbook = xlrd.open_workbook(file_path)
    file_name = filecm.short_name(file_path)
    sheets = workbook.sheet_names()
    if not sheet_name in sheets:
        # 如果没有这个Sheet，则跳过
        logcm.print_info("Sheet[%s]在文件[%s]中不存在!" % (sheet_name, file_name), fg='red')
        return None

    # 读取Sheet
    worksheet = workbook.sheet_by_name(sheet_name)
    return worksheet


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

    # 读取Sheet
    worksheet = get_sheet(file_path, sheet_name)

    # 判断标题行是否在合理范围
    if title_line < 0 or title_line >= worksheet.nrows:
        logcm.print_info("标题行不合理 %d" % title_line, fg='red')
        return None

    # 标题列
    if not col_titles or len(col_titles) == 0:
        logcm.print_info("标题列未设置 %s" % str(col_titles), fg='red')
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


def find_first_key(sheet, key, col_index=0):
    """
    对指定列搜索指定关键词,返回第一个匹配的行索引
    :param sheet: Sheet对象
    :param key: 关键词
    :param col_index: 列索引
    :return:行索引,没找到返回-1
    """
    if sheet is None:
        logcm.print_info("Sheet对象为空!", fg='red')
        return -1

    if key is None or not isinstance(key, str) or len(key) == 0:
        logcm.print_info("要检索的KEY为空!", fg='red')
        return -1

    if col_index < 0 or col_index >= sheet.ncols:
        logcm.print_info("要检索的列索引(%d)不正常!" % col_index, fg='red')
        return -1

    for i in range(sheet.nrows):
        cell_val = sheet.cell_value(i, col_index)
        if cell_val == key:
            return i
    return -1


def find_title_index(sheet, title_line, **kwargs):
    """
    在指定Sheet的指定行,查找每个标题对应的列索引
    :param sheet:Sheet对象
    :param title_line:标题行索引
    :param kwargs:其他参数
    :return:索引字典
    """
    index_map = {}
    for (title, title_key) in kwargs["title_map"].items():
        # 查找标题
        found_title = False
        start_col = colname_to_index(kwargs["start_col"])
        end_col = colname_to_index(kwargs["end_col"])
        for i in range(start_col, end_col + 1):
            val = get_cell_val(sheet, title_line, i)
            if title == val:
                # 记录标题的索引,标记找到
                index_map[title] = i
                found_title = True
                continue
        # 如果找不到,则处理停止
        if not found_title:
            logcm.print_info("在第%d行没找到标题:%s" % (title_line + 1, title), fg='red')
            return None
    return index_map


def load_excel_dict(file_path, sheet_name, title_line=None, data_start_line=None, title_group=None, sub_items=None,
                    start_key=None, end_type="EMPTY"):
    """
    根据指定路径，Sheet名，标题行，数据开始行，标题组设置
    @param file_path: 文件路径
    @param sheet_name: Sheet名
    @param title_line: 标题行索引
    @param data_start_line: 标题行索引
    @param title_group: 标题组设置
    @param sub_items: 子项目设置
    @param start_key: 开始KEY(可以根据开始KEY来查找标题行和数据开始行)
    @param end_type: 终止类型(SORT-NO:下一行非排序数字, EMPTY:下一行全空)
    @return: 数据字典列表
    """

    # 读取Sheet
    worksheet = get_sheet(file_path, sheet_name)

    # 根据开始KEY,初始化标题行和数据开始行
    if start_key is not None:
        start_key_row = find_first_key(worksheet, start_key)
        if start_key_row < 0:
            logcm.print_info("开始KEY没找到! %s" % start_key, fg='red')
            return None
        title_line = start_key_row + 1
        data_start_line = title_line + 1

    # 判断标题行是否在合理范围
    if title_line < 0 or title_line >= worksheet.nrows:
        logcm.print_info("标题行不合理 %d" % title_line, fg='red')
        return None

    # 为每个标题找到对应的列索引.
    for (group_key, group_setting) in title_group.items():
        group_setting["index_map"] = find_title_index(worksheet, title_line, **group_setting)

    # 取得数据
    data_list = []
    for i in range(data_start_line, worksheet.nrows):
        row_data = {}
        # 判断是否到达结束行
        if end_type == "SORT-NO":
            val = worksheet.cell_value(i, 0)
            result = checkcm.check_regex(val, pattern="sort-no", show_error=False)
            # 标记开始行和结束行
            if not result.ok:
                if len(data_list) > 0:
                    data_list[-1]["end_row"] = i - 1
                break
            if val is not None:
                row_data["start_row"] = i
                if len(data_list) > 0:
                    data_list[-1]["end_row"] = i - 1

        # 是否空行
        is_blank = True
        # 对标题组遍历
        for (group_key, group_setting) in title_group.items():
            # 每个分组一个字典
            group_data = load_group_data(worksheet, group_setting["title_map"], group_setting["index_map"], i)
            if group_data is not None:
                row_data[group_key] = group_data
                is_blank = False

        # 遇到空行
        if is_blank:
            if end_type == "EMPTY":
                break
            else:
                row_data["end_row"] = i
                continue
        # 非空行则加入数据列表
        data_list.append(row_data)

    if len(data_list) > 0 and end_type == "SORT-NO" and sub_items is not None:
        for row_data in data_list:
            row_data["subItems"] = load_sub_items(worksheet, sub_items, title_line, row_data["start_row"],
                                                  row_data["end_row"])
            # 返回结果中去掉开始结束行
            row_data.pop("start_row")
            row_data.pop("end_row")

    return data_list


def load_group_data(sheet, title_map, index_map, row_line):
    """
    在指定Sheet中,按照标题设定,标题索引设定,读取指定行数据
    :param sheet:Sheet对象
    :param title_map:标题设定
    :param index_map:索引设定
    :param row_line:指定行
    :return:数据字典对象
    """
    row_data = {}
    is_blank = True
    for (title, title_key) in title_map.items():
        # 根据标题取列索引
        index = index_map[title]
        # 取值
        val = get_cell_val(sheet, row_line, index)
        # 空字段判断（目前只判断字符串类型）
        if len(str(val)) > 0:
            # 设置值及非空行
            row_data[title_key] = val
            is_blank = False

    if is_blank:
        return None
    else:
        return row_data


def load_sub_items(sheet, sub_items, title_line, start_row, end_row):
    """
    加载子项目列表
    :param sheet:Sheet对象
    :param sub_items:子项目定义
    @param title_line: 标题行索引
    :param start_row:开始行
    :param end_row:结束行
    :return:子项目数据对象
    """
    if sheet is None or sub_items is None:
        return None

    # 判断数据行是否在合理范围
    if start_row < 0 or end_row < start_row or end_row >= sheet.nrows:
        logcm.print_info("数据行不合理 %d ~ %d" % (start_row, end_row), fg='red')
        return None

    # 标题索引Map
    index_map = find_title_index(sheet, title_line, **sub_items)
    # 数据开始列
    start_col = colname_to_index(sub_items["start_col"])
    sub_groups = {}
    group_key = None
    for i in range(start_row, end_row + 1):
        start_val = get_cell_val(sheet, i, start_col)
        if start_val in sub_items["group_keys"]:
            group_key = start_val
            sub_groups[group_key] = []
        else:
            group_data = load_group_data(sheet, sub_items["title_map"], index_map, i)
            if group_key is not None and group_data is not None:
                sub_groups[group_key].append(group_data)
    return sub_groups


def get_cell_val(sheet, row, col):
    """
    取得Excel单元格的值
    :param sheet:Sheet对象
    :param row:行编号
    :param col:列编号
    :return:单元格值
    """
    # 表格的数据类型
    cell_type = sheet.cell(row, col).ctype
    cell_val = sheet.cell_value(row, col)
    if cell_type == 2 and cell_val % 1 == 0:
        # 如果是整形
        return int(cell_val)
    elif cell_type == 3:
        # 转成datetime对象
        tp_list = xldate_as_tuple(cell_val, 0)
        date = datetime(*tp_list)
        return date
    elif cell_type == 4:
        # 布尔值
        bool_val = True if cell_val == 1 else False
        return bool_val
    else:
        return cell_val


def colname_to_index(col_name):
    """
    字母列名转成数字索引
    :param col_name:
    :return:
    """
    base = ord("A")
    r = 0
    for i in list(col_name):
        r = r * 26 + ord(i) - base + 1
    return r - 1

# if __name__ == '__main__':
#     print(colname_to_index("A"))
#     print(colname_to_index("Z"))
#     print(colname_to_index("AA"))
#     print(colname_to_index("AZ"))
#     print(colname_to_index("ZZ"))
