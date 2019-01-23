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

    def __del__(self):
        """
        关闭SSH连接
        @return: 无
        """

        # 关闭redis连接
        if self.rds is not None:
            logcm.print_info("Close redis connection.")
            self.rds.connection_pool.disconnect()

    def keys(self, pattern="*"):
        # 取得Key对应值
        logcm.print_info('Redis keys: %s' % pattern)
        key_list = []

        for key in self.rds.keys(pattern):
            # 转换成字符串
            key_list.append(key.decode())

        logcm.print_obj(key_list, "key_list", show_header=False)
        return key_list

    def clear(self, name):
        # 删除Key对应值
        logcm.print_info('Clear name: %s' % name)
        try:
            self.rds.delete(name)
        except Exception as e:
            logcm.print_info("Exception : %s" % e)

    def ttl(self, name):
        # 取得Key剩余时间
        try:
            ttl = self.rds.ttl(name)
        except Exception as e:
            logcm.print_info("Exception : %s" % e)
            ttl = None

        logcm.print_info('TTL %s is %d seconds.' % (name, ttl))
        return ttl

    def get(self, key, convert=None):
        """
        取得Redis中指定Key的值
        @param key: 指定Key
        @param convert: 指定转换方法
        @return: Key对应值
        """

        # 取得Key对应值
        logcm.print_info('Redis Get by key: %s' % key)
        try:
            result = self.rds.get(key)
        except Exception as e:
            logcm.print_info("Exception : %s" % e)
            result = None

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
