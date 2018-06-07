#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
把EXCEL文件转成代码的模块信息字典
"""

import sys

from common import logcm
from common import loadcfgcm
from codegen.codegen_mdl import Module, Service, Bean, Code
from common import loadcfgcm
from common.dboraclecm import DbOracleClient

# 配置
default_config = """
{
    "host": "localhost",
    "port": 1521,
    "db": "orcl",
    "user": "root",
    "passwd": "root"
}
"""


class CodeGenDBLoader:
    """
    代码生成-DB加载类
    """

    def __init__(self):
        # 加载配置文件
        self.cfg_db = loadcfgcm.load("codegen_loader_db.json", default_config)

    def load_oracle_table(self, table_name):
        """
        按照配置读取指定数据表名,载入模块数据
        :param table_name: 数据表名
        :return:数据表字典对象
        """
        logcm.print_info("Loading table : %s ..." % table_name)
        # 加载DB数据表模块信息

        # 建立和数据库系统的连接
        dbClient = DbOracleClient("oracle", self.cfg_db)

        result = dbClient.getColumns(table_name)
        logcm.print_obj(result, "result", show_table=True)

        return result


if __name__ == '__main__':
    loader = CodeGenDBLoader()
    loader.load_oracle_table("T_CONTACTS")
