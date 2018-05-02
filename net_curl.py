#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Curl使用示例。
"""

from common import loadcfgcm
from common import datecm
from common import filecm
from common import logcm
from common import webcm

# 缺省配置及说明
default_config = """"
{
    "site_list": [
        {
            "url": "http://www.baidu.com/",
            "name": "baidu.txt"
        },
        {
            "url": "http://www.163.com/",
            "name": "163.txt"
        }
    ]
}
"""

# 定义并创建临时目录
tmp_path = './temp/net/curl/' + datecm.now_time_str()
filecm.makedir(tmp_path)

# 加载配置文件
config_map = loadcfgcm.load("net_curl.json", default_config)

# 按照站点一览进行循环
for cfg in config_map["site_list"]:
    result = webcm.curl(cfg["url"], tmp_path, cfg["name"])
    logcm.print_obj(result, "result-%s" % cfg["name"])
