# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Redis common api
Redis相关共通函数
"""

import redis
from common import logcm
from common import loadcfgcm


class RedisClient:
    def __init__(self, redis_config):
        self.cfg = redis_config
        # config {
        # host: Redis服务器地址
        # port: Redis服务器端口
        # }
        self.connect()

    def connect(self):
        # 链接Redis服务器
        self.rds = redis.StrictRedis(host=self.cfg['host'], port=self.cfg['port'], db=0)

    def get(self, key, convert=None):
        """
        取得Redis中指定Key的值
        @param key: 指定Key
        @param convert: 指定转换方法
        @return: Key对应值
        """

        # 取得Key对应值
        logcm.print_info('Redis Get by key: %s' % key)
        result = self.rds.get(key)

        # 不存在时
        if result is None:
            logcm.print_obj(result, "result", show_header=False)
            return None

        # 转换成字符串
        result = result.decode()

        # 无转换时直接返回
        if convert is None:
            logcm.print_obj(result, "result", show_header=False)
            return result

        # 执行转换
        result = convert(result)
        logcm.print_obj(result, "result", show_header=False)
        return result

    def set_val(self, key, val):
        """
        设定Redis中指定Key的值
        @param key: 指定Key
        @param val: 指定值
        @return: 是否成功
        """

        # 取得Key对应值
        logcm.print_info('Redis Set: %s --> %s' % (key, val))
        result = self.rds.set(key, val)
        logcm.print_obj(result, "result", show_header=False)
        # 返回值
        return result
