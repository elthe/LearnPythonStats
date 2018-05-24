#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
把EXCEL报送文件转成XML示例
"""

from cncrs.cncrs_convert import CNCRSConverter

# 转换器对象
converter = CNCRSConverter()
# 待转换文件列表
SAMPLE_XLS_LIST = {
    "./input/非居民金融账户涉税信息采集表-C1YINUFUXUEZCI.xlsx",
    "./input/非居民金融账户涉税信息采集表-C2XNUTNMNUZTU3.xlsx",
    "./input/非居民金融账户涉税信息采集表-D9IFI2EUVSQU8Y.xlsx",
}
for xls_path in SAMPLE_XLS_LIST:
    # 测试版
    converter.xls_to_xml(xls_path=xls_path, save_path="./output", test=True)
    # 生产版
    converter.xls_to_xml(xls_path=xls_path, save_path="./output", test=False)
