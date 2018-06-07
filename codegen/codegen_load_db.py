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
from jinja2 import Template
from common import filecm

# Oracle数据表模版
ORACLE_TABLE_TPL = """
select A.COLUMN_ID as COLUMN_ID,
       A.COLUMN_NAME as COLUMN_NAME,
       A.DATA_TYPE as DATA_TYPE,
       DECODE(A.DATA_TYPE, 'NUMBER', A.DATA_PRECISION, A.DATA_LENGTH) as COLUMN_LENGTH,
       A.DATA_SCALE as COLUMN_SCALE,
       DECODE(E.UNIQUENESS, 'UNIQUE', 'Y', 'N') as IS_UNIQUE,
       DECODE(E.KEY, 'Y', 'Y', 'N') IS_PK,
       F.COMMENTS as COLUMN_COMMENTS,
       A.NULLABLE as NULLABLE,
       A.DATA_DEFAULT as DEFAULT_VAL
  from USER_TAB_COLUMNS A,
       USER_COL_COMMENTS F,
       (select B.TABLE_NAME,
               B.INDEX_NAME,
               B.UNIQUENESS,
               C.COLUMN_NAME,
               DECODE(D.CONSTRAINT_NAME, null, 'N', 'Y') KEY
          from USER_INDEXES B,
               USER_IND_COLUMNS C,
               (select CONSTRAINT_NAME
                  from USER_CONSTRAINTS
                 where CONSTRAINT_TYPE = 'P') D
         where B.INDEX_NAME = C.INDEX_NAME
           and B.INDEX_NAME = D.CONSTRAINT_NAME(+)) E
 where A.TABLE_NAME = '{{tableName}}'
   and A.TABLE_NAME = E.TABLE_NAME(+)
   and A.COLUMN_NAME = E.COLUMN_NAME(+)
   and A.TABLE_NAME = F.TABLE_NAME
   and A.COLUMN_NAME = F.COLUMN_NAME
 order by A.COLUMN_ID
"""

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

        sql_str = Template(ORACLE_TABLE_TPL, lstrip_blocks=True).render(tableName=table_name)
        result = dbClient.fetchall(sql_str)
        logcm.print_obj(result, "result")

        return result


if __name__ == '__main__':
    loader = CodeGenDBLoader()
    loader.load_oracle_table("T_CONTACTS")
