#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DB common api
DB相关共通函数
"""

import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import cx_Oracle

from common.dbbasecm import DbBaseClient
from common import logcm
from common import classcm


class DbOracleClient(DbBaseClient):
    def __init__(self, db_type, db_cfg):
        """
        根据DB类型和设置信息，取得DB连接
        @param db_type: DB类型
        @param db_cfg: DB设置
        @return: 无
        """

        super(DbOracleClient, self).__init__(db_type, db_cfg)

    def connection(self):
        """
        建立和数据库系统的连接。
        """

        url = '%s:%s/%s' % (self.cfg['host'], self.cfg['port'], self.cfg['db'])
        self.conn = cx_Oracle.connect(self.cfg['user'], self.cfg['passwd'], url)
        # 获取操作游标
        self.cursor = self.conn.cursor()

    def execute(self, sql_command, param={}):
        """
        执行SQL命令
        @param sql_command: SQL命令
        @param param: SQL参数
        @return:
        """

        self.cursor.execute(sql_command, param)

    def executemany(self, sql_command, param):
        """
        执行SQL命令
        @param sql_command: SQL命令
        @param param: SQL参数列表
        @return:
        """

        self.cursor.executemany(sql_command, param)

    def fetchone(self, sql_command, param={}):
        """
        执行SQL命令
        @param sql_command: SQL命令
        @param param: SQL参数
        @return:
        """

        self.cursor.execute(sql_command, param)
        # 获取一条记录
        one_data = self.cursor.fetchone()
        name_list = self.getColumnNames()
        # 转成字典返回
        return classcm.list_to_dict(one_data, name_list)

    def fetchmany(self, sql_command, param={}, pos=0):
        """
        执行SQL命令
        @param sql_command: SQL命令
        @param param: SQL参数
        @param pos: 索引
        @return:
        """

        self.cursor.execute(sql_command, param)
        # 获取多条记录
        many_data = self.cursor.fetchmany(pos)
        name_list = self.getColumnNames()
        # 转成字典列表返回
        return classcm.matrix_to_dict(many_data, name_list)

    def fetchall(self, sql_command, param={}):
        """
        执行SQL命令
        @param sql_command: SQL命令
        @param param: SQL参数
        @return:
        """

        self.cursor.execute(sql_command, param)
        # 获取多条记录
        all_data = self.cursor.fetchall()
        name_list = self.getColumnNames()
        # 转成字典列表返回
        return classcm.matrix_to_dict(all_data, name_list)

    def getColumnNames(self):
        """
        取得列名列表
        :return:列名列表
        """
        columnNameList = [i[0] for i in self.cursor.description]
        return columnNameList

    def getColumns(self, table_name):
        """
        取得指定表的字段列表
        :param table_name:数据表名
        :return: 字段列表
        """
        # Oracle数据表模版
        sql_str = """
        SELECT A.column_id AS column_id,
               A.column_name AS column_name,
               A.data_type AS data_type,
               DECODE(A.data_type, 'NUMBER', A.data_precision, A.data_length) AS column_length,
               A.data_scale AS column_scale,
               DECODE(E.uniqueness, 'UNIQUE', 'Y', 'N') AS is_unique,
               DECODE(E.key, 'Y', 'Y', 'N') is_pk,
               F.comments AS column_comments,
               A.nullable AS nullable,
               A.data_default as default_val
          FROM user_tab_columns A,
               user_col_comments F,
               (SELECT B.table_name,
                       B.index_name,
                       B.uniqueness,
                       C.column_name,
                       DECODE(D.constraint_name, NULL, 'N', 'Y') key
                  FROM user_indexes B,
                       user_ind_columns C,
                       (SELECT constraint_name
                          FROM user_constraints
                         WHERE constraint_type = 'P') D
                 WHERE B.index_name = C.index_name
                   AND B.index_name = D.constraint_name(+)) E
         WHERE A.table_name = :table_name
           AND A.table_name = E.table_name(+)
           AND A.column_name = E.column_name(+)
           AND A.table_name = F.table_name
           AND A.column_name = F.column_name
         ORDER BY A.column_id
        """
        return self.fetchall(sql_str, {'table_name': table_name})

    def commit(self):
        """
        提交事务。
        """
        self.conn.commit()

    def close(self):
        """
        关闭DB连接。
        """
        self.cursor.close()
