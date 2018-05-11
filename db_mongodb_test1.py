#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Oracle DB使用示例。
安装驱动说明：
https://cx-oracle.readthedocs.io/en/latest/installation.html#installing-cx-oracle-on-macos
"""

from common import loadcfgcm
from common.dbmongocm import DbMongoClient
from common import logcm

# 配置
default_config = """
{
    "host": "localhost",
    "port": 27017,
    "db": "xxxx",
    "user": "root",
    "passwd": "root",
    "collection": {
        "stock" : "ts.xxxx",
        "index" : "ts.xxxx"
    }
}
"""

# 加载配置文件
cfg = loadcfgcm.load("db_mongodb_test1.json", default_config)

# 建立和数据库系统的连接
dbClient = DbMongoClient("mongodb", cfg)

# mongodb query code
stock_code = "000001.SZ"
fund_code = '110022'
index_stock_code = "399300.SZ"
start_date = "2015-02-20"
end_date = "2018-03-13"

query = {
    "代码": stock_code,
    "日期": {
        "$gte": start_date,
        "$lte": end_date
    }
}
projection = {
    "_id": 0.0,
    "日期": 1.0,
    "代码": 1.0,
    "收盘价(元)": 1.0,
    "涨跌幅(%)": 1.0
}

result = dbClient.find("stock", query, projection)
logcm.print_obj(result, "result")
