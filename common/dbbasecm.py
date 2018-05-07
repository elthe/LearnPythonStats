#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DB Client Base Class
DB客户端基类
"""

from common import logcm


class DbBaseClient:
    def __init__(self, db_type, db_cfg):
        """
        根据DB类型和设置信息，取得DB连接
        @param db_type: DB类型
        @param db_cfg: DB设置
        @return: 无
        """

        self.db_type = db_type
        self.cfg = db_cfg
        self.connection()

    def connection(self):
        """
        取得DB连接，由各子类实现。
        """
        logcm.print_info("Get Connection ...")

    def commit(self):
        """
        提交事务。
        """
        logcm.print_info("Commit ...")

    def close(self):
        """
        关闭DB连接，由各子类实现。
        """
        logcm.print_info("Close Connection ...")

    def execute(self, sql_command, param={}):
        """
        执行SQL命令
        @param sql_command: SQL命令
        @param param: SQL参数
        @return:
        """
        logcm.print_info("Execute Sql Command %s " % sql_command)
        logcm.print_obj(param, "param")

    def executemany(self, sql_command, param):
        """
        执行SQL命令
        @param sql_command: SQL命令
        @param param: SQL参数列表
        @return:
        """
        logcm.print_info("Execute Sql Command %s " % sql_command)
        logcm.print_obj(param, "param")

    def fetchone(self, sql_command, param={}):
        """
        执行SQL命令
        @param sql_command: SQL命令
        @param param: SQL参数
        @return:
        """
        logcm.print_info("Fetch one with Sql Command %s " % sql_command)
        logcm.print_obj(param, "param")

    def fetchmany(self, sql_command, param={}, pos=0):
        """
        执行SQL命令
        @param sql_command: SQL命令
        @param param: SQL参数
        @param pos: 索引
        @return:
        """

        logcm.print_info("Fetch many with Sql Command %s " % sql_command)
        logcm.print_obj(param, "param")
        logcm.print_obj(pos, "pos")

    def fetchall(self, sql_command, param={}):
        """
        执行SQL命令
        @param sql_command: SQL命令
        @param param: SQL参数
        @return:
        """

        logcm.print_info("Fetch all with Sql Command %s " % sql_command)
        logcm.print_obj(param, "param")

    def __del__(self):
        """
        析构方法
        @return: 无
        """
        self.close()
