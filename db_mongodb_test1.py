#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Oracle DB使用示例。
安装驱动说明：
https://cx-oracle.readthedocs.io/en/latest/installation.html#installing-cx-oracle-on-macos
"""

import pandas as pd

from common import loadcfgcm
from common.dbmongocm import DbMongoClient
from common import logcm
from quant.quantcm import QuantCalculator

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


def load_data(set_name, stock_code, start_date, end_date):
    """
    :param set_name: 数据集名
    :param stock_code: 股票代码，例如‘000001.SZ’
    :param start_date: 回测开始日期，例如‘1991-1-30'
    :param end_date: 回测结束日期，例如‘2015-12-31’
    :return: 函数返回其他函数的各参数序列
    """
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
    result = dbClient.find(set_name, query, projection)
    logcm.print_obj(result, "result")
    return result


def load_data_to_quant(stock_code, index_code, start_date, end_date):
    """
    :param stock_code: 股票代码，例如‘000001.SZ’
    :param index_code: 指数代码，例如‘sh000001’
    :param start_date: 回测开始日期，例如‘1991-1-30'
    :param end_date: 回测结束日期，例如‘2015-12-31’
    :return: 函数返回其他函数的各参数序列
    """

    # loading stock data from mongo db
    df_stock = load_data("stock", stock_code, start_date, end_date)
    df_stock['date'] = pd.to_datetime(df_stock['日期'])
    df_stock.set_index('date', inplace=True)
    df_stock.loc[df_stock['涨跌幅(%)'] == '--', '涨跌幅(%)'] = "0.00"
    df_stock['rtn'] = df_stock['涨跌幅(%)'].astype(float);
    df_stock['close'] = df_stock['收盘价(元)'].astype(float);
    df_stock.sort_index(ascending=True, inplace=True)
    df_stock1 = df_stock[['rtn', 'close']]

    # loading index data from mongo db
    df_index = load_data("index", index_code, start_date, end_date)
    df_index['date'] = pd.to_datetime(df_index['日期'])
    df_index.set_index('date', inplace=True)
    df_index.loc[df_index['涨跌幅(%)'] == '--', '涨跌幅(%)'] = "0.00"
    df_index['index_return'] = df_index['涨跌幅(%)'].astype(float);
    df_index['index'] = df_index['收盘价(元)'].astype(float);
    df_index.sort_index(ascending=True, inplace=True)
    df_index1 = df_index[['index_return', 'index']]

    # 数据
    # 拼接数据，对齐datatime项。
    df_merge = pd.concat([df_stock1, df_index1], axis=1)
    df_fixed = df_merge.dropna(how='any')

    # init time lines
    date_line = df_fixed.index
    # capital_line 资产序列，收盘价
    capital_line = df_fixed['close']
    # 收益率序列
    return_line = df_fixed['rtn'] / 100
    # 指数资产序列
    index_line = df_fixed['index']
    # 指数收益率序列
    index_return_line = df_fixed['index_return'] / 100
    return {
        'date_line': date_line,
        'capital_line': capital_line,
        'return_line': return_line,
        'index_line': index_line,
        'index_return_line': index_return_line
    }

# 加载数据
queryresult = load_data_to_quant(stock_code, index_stock_code, start_date, end_date)
# 查询记录为空检验
if (queryresult is not None):
    quant = QuantCalculator(queryresult['date_line'], queryresult['capital_line'], queryresult['return_line'],
                                queryresult['index_line'], queryresult['index_return_line'])
    gen_result, risk_result = quant.calculate_quant()
    logcm.print_obj(gen_result, "gen_result")
    logcm.print_obj(risk_result, "risk_result")

