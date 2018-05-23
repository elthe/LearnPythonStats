# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Excel common api
Excel文件相关共通函数
"""

import xlrd

from common import filecm
from common import logcm
from datetime import datetime
from xlrd import xldate_as_tuple


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
        logcm.print_info("Sheet不存在 %s - %s" % (short_name, sheet_name), fg='red')
        return None

    # 读取Sheet
    worksheet = workbook.sheet_by_name(sheet_name)

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


def load_excel_dict(file_path, sheet_name, title_line, data_start_line, title_group):
    """
    根据指定路径，Sheet名，标题行，数据开始行，标题组设置
    @param file_path: 文件路径
    @param sheet_name: Sheet名
    @param title_line: 标题行索引
    @param data_start_line: 标题行索引
    @param title_group: 文件短名
    @return: 数据字典列表
    """

    # 读取Excel
    workbook = xlrd.open_workbook(file_path)
    sheets = workbook.sheet_names()
    file_name = filecm.short_name(file_path)
    if not sheet_name in sheets:
        # 如果没有这个Sheet，则跳过
        logcm.print_info("Sheet不存在 %s - %s" % (file_name, sheet_name), fg='red')
        return None

    # 读取Sheet
    worksheet = workbook.sheet_by_name(sheet_name)

    # 判断标题行是否在合理范围
    if title_line < 0 or title_line >= worksheet.nrows:
        logcm.print_info("标题行不合理 %d" % title_line, fg='red')
        return None

    # 为每个标题找到对应的列索引.
    for (group_key, group_setting) in title_group.items():
        group_setting["index_map"] = {}
        for (title, title_key) in group_setting["title_map"].items():
            # 查找标题
            found_title = False
            start_col = colname_to_index(group_setting["start_col"])
            end_col = colname_to_index(group_setting["end_col"])
            for i in range(start_col, end_col + 1):
                val = get_cell_val(worksheet, title_line, i)
                if title == val:
                    # 记录标题的索引,标记找到
                    group_setting["index_map"][title] = i
                    found_title = True
                    continue
            # 如果找不到,则处理停止
            if not found_title:
                logcm.print_info("标题没找到 %s-%s" % (group_key, title), fg='red')
                return None

    logcm.print_obj(title_group, "title_group", show_json=True)

    # 取得数据
    data_list = []
    for i in range(data_start_line, worksheet.nrows):
        row_data = {}
        # 是否空行
        is_blank = True
        # 对标题组遍历
        for (group_key, group_setting) in title_group.items():
            # 每个分组一个字典
            row_data[group_key] = {}
            for (title, title_key) in group_setting["title_map"].items():
                # 根据标题取列索引
                index = group_setting["index_map"][title]
                # 取值
                val = get_cell_val(worksheet, i, index)
                # 空字段判断（目前只判断字符串类型）
                if len(str(val)) > 0:
                    # 设置值及非空行
                    row_data[group_key][title_key] = val
                    is_blank = False

        # 遇到空行,则停止取数
        if is_blank:
            break
        # 非空行则加入数据列表
        data_list.append(row_data)

    return data_list


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


if __name__ == '__main__':
    print(colname_to_index("A"))
    print(colname_to_index("Z"))
    print(colname_to_index("AA"))
    print(colname_to_index("AZ"))
    print(colname_to_index("ZZ"))
