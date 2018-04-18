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

    differ = difflib.Differ()
    diff = differ.compare(lines1, lines2)
    diff_list = list(diff)

    line_left = 0
    line_right = 0
    for i in range(len(diff_list)):
        line = diff_list[i]

        if line.startswith("+"):
            line_num_str = '[%d]' % line_right
            logcm.print_style('%s %s' % (line_num_str, line[2:]), fg='blue')
            line_right += 1
        elif line.startswith("-"):
            line_num_str = '[%d]' % line_left
            logcm.print_style('%s %s' % (line_num_str, line[2:]), fg='purple')
            line_left += 1
        elif line.startswith("?"):
            logcm.print_style('%s %s' % (' ' * len(line_num_str), line[2:]), fg='red', end='')
        else:
            logcm.print_style('[%d] %s' % (line_left, line[2:]), fg='green')
            logcm.print_style('[%d] %s' % (line_right, line[2:]), fg='green')
            line_left += 1
            line_right += 1
