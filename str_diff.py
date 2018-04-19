#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
字符串对比示例
"""

from common import diffcm
from common import filecm

# 字符串比较
text1 = """
text1:
This module provides classes and functions for comparing sequences.
including HTML and context and unified diffs.
difflib Document v7.411
add string
kk
pp
"""
text2 = """
text2:
This module provides classes and functions for Comparing sequences.
including HTML and context and unified diffs.
difflib document v7.522
kk
add2
pp
dd...d..
"""
diffcm.diff_by_text(text1, text2)

# 文件对比
text_path1 = './temp/file/file_diff1.txt'
text_path2 = './temp/file/file_diff2.txt'
filecm.save_str(text1, file_name=text_path1)
filecm.save_str(text2, file_name=text_path2)
diffcm.diff_by_file(text_path1, text_path2)

