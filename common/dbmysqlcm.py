#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DB common api
DB相关共通函数
"""

import pymysql

from common.dbbasecm import DbBaseClient
from common import logcm


class DbMysqlClient(DbBaseClient):
    def __init__(self, db_type, db_cfg):
        """
        根据DB类型和设置信息，取得DB连接
        @param db_type: DB类型
        @param db_cfg: DB设置
        @return: 无
        """

        super(DbMysqlClient, self).__init__(db_type, db_cfg)

    def connection(self):
        """
        建立和数据库系统的连接。
        """

        self.conn = pymysql.connect(host=self.cfg['host'], user=self.cfg['user'], passwd=self.cfg['passwd'],
                                    db=self.cfg['db'], port=self.cfg['port'], charset=self.cfg['charset'])
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
        logcm.print_obj(one_data, "one_data")
        return one_data

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
        many_data = self.cursor.fetmany(pos)
        logcm.print_obj(many_data, "many_data")
        return many_data

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
        logcm.print_obj(all_data, "all_data")
        return all_data

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
