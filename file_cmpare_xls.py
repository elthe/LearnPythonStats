#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EXCEL数据加载
"""

from common import xlscm
from common import loadcfgcm
from common import logcm

# 配置
default_config = """
{

    "left_file_path" : "./temp/xxxxxx.xlsx",
    "right_file_path" : "./temp/yyyyyyy.xlsx",
    "sheet_name" : "XXX表",
    "title_line" : 10,
    "start_line" : 13,
    "pk_col" : 1,
    "start_col" : 2,
    "ignore_new_line": true
}
"""

# 加载配置文件
cfg = loadcfgcm.load("file_compare_xls.json", default_config)

# 取得指定目录下的文件列表
diff_list = xlscm.cmp_excel(**cfg)
logcm.print_obj(diff_list, "diff_list")



