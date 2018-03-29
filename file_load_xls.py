#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EXCEL数据加载
"""

from common import logcm
from common import filecm
from common import datecm

# 根目录
root_dir = "/Users/xxxx/Downloads"
out_file = "output" + datecm.now_time_str() + ".csv"

# 配置
# Excel文件名，可以对应到多个Sheet，每个Sheet有一个标题行。
config_map = {
    # 1-利得资本
    'XXXXXX': [{
        'sheet_name': '明细',
        'title_line': 0,
        'col_titles': ['基金名称', '投资者名称', '客户类型', '证件类型', '证件号码', '????']
    }],
    'YYYYYY': [{
        'sheet_name': '客户明细J',
        'title_line': 0,
        'col_titles': ['????', '客户名称', '客户类型', '证件类型', '证件号码', '持有份额']
    }],
}

# 取得指定目录下的文件列表
path_list = filecm.search_files(root_dir, '.xlsx,.xls', r'^[^~]+')
logcm.print_obj(path_list, "path_list")

# 读取文件数
read_file_cnt = 0
# 读取数据行数
read_line_cnt = 0

# 路径列表
for path in path_list:
    # 短文件名
    short_name = filecm.short_name(path)
    # 根据文件名取得配置列表
    if short_name not in config_map:
        print("==========未找到配置：%s" % short_name)
        continue

    # 配置列表
    cfg_list = config_map[short_name]
    for cfg in cfg_list:
        # 读取数据
        data_list = filecm.load_excel_data(path, short_name, cfg['sheet_name'], cfg['title_line'], cfg['col_titles'])
        if data_list:
            # 写入CSV文件
            filecm.append_csv(out_file, data_list)
            # 计数
            read_file_cnt += 1
            read_line_cnt += len(data_list)
            # 写日志
            print("文件处理完成！ %s 读取条数：%d" % (short_name, len(data_list)))

# 总结报告
print("\n\n处理完成！ 总共读取文件：%d个 读取记录：%d条" % (read_file_cnt, read_line_cnt))
print(out_file)


