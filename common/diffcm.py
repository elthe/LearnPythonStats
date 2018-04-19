# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
diff common api
diff 相关共通函数
"""

from common import logcm
from common import loadcfgcm

import difflib


def diff_by_lines(lines1, lines2):
    """
    比较两个字符串列表。
    @param lines1: 字符串列表1
    @param lines2: 字符串列表2
    @return: None
    """

    # differ对象
    differ = difflib.Differ()
    # 比较处理
    diff = differ.compare(lines1, lines2)
    # 转成字符串列表
    diff_list = list(diff)

    # 左侧行号
    line_left = 0
    # 右侧行号
    line_right = 0
    # 行循环
    for i in range(len(diff_list)):
        # 行内容
        line = diff_list[i]

        if line.startswith("-"):
            # 左侧文本打印
            line_num_str = '[%d]' % line_left
            logcm.print_style('%s %s' % (line_num_str, line[2:]), fg='green', bg='black')
            # 左侧行号+1
            line_left += 1
        elif line.startswith("+"):
            # 右侧文本打印
            line_num_str = '[%d]' % line_right
            logcm.print_style('%s %s' % (line_num_str, line[2:]), fg='orange', bg='black')
            # 右侧行号+1
            line_right += 1
        elif line.startswith("?"):
            # 不同点标注
            logcm.print_style('%s %s' % (' ' * len(line_num_str), line[2:]), fg='red', bg='black', end='')
        else:
            # 相同内容行
            logcm.print_style('[%d] %s' % (line_left, line[2:]), color='disable', fg='black', bg='lightgrey')
            logcm.print_style('[%d] %s' % (line_right, line[2:]), color='disable', fg='black', bg='lightgrey')
            # 左右侧行号+1
            line_left += 1
            line_right += 1
