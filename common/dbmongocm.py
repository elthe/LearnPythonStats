#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DB common api
DB相关共通函数
"""

import pandas as pd
import pymongo as pg

from common.dbbasecm import DbBaseClient
from common import logcm


class DbMongoClient(DbBaseClient):
    def __init__(self, db_type, db_cfg):
        """
        根据DB类型和设置信息，取得DB连接
        @param db_type: DB类型
        @param db_cfg: DB设置
        @return: 无
        """

        super(DbMongoClient, self).__init__(db_type, db_cfg)

    def connection(self):
        """
        建立和数据库系统的连接。
        """

        # 建立和数据库系统的连接,指定host及port参数
        client = pg.MongoClient(self.cfg['host'], self.cfg['port'])
        # 连接mydb数据库,账号密码认证
        self.db = client[self.cfg['db']]
        self.db.authenticate(self.cfg['user'], self.cfg['passwd'])

    def find(self, set_name, query, projection, sort=None):
        """
        执行查找命令
        @param query: 检索对象
        @param projection: SQL参数
        @param sort: 排序
        @return:
        """

        collection = self.db[self.cfg['collection'][set_name]]
        cursor = collection.find(query, projection=projection, sort=sort)
        try:
            df = pd.DataFrame(list(cursor))
            return df
        except Exception as e:
            logcm.print_info('DB Exception : %s' % e, fg='red')
