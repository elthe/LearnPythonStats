# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Redis common api
Redis相关共通函数
"""

import redis
from common import logcm
from common import loadcfgcm


def get(key, convert=None, rds=None, host=None, port=None):
    """
    取得Redis中指定Key的值
    @param key: 指定Key
    @param convert: 指定转换方法
    @param rds: Redis服务器对象
    @param host: Redis服务器地址
    @param port: Redis服务器端口
    @return: Key对应值
    """

    # 取得Redis服务器
    rds = get_redis(rds, host, port)

    # 取得Key对应值
    logcm.print_info('Redis Get by key: %s' % key)
    result = rds.get(key)

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


def set_val(key, val, rds=None, host=None, port=None):
    """
    设定Redis中指定Key的值
    @param key: 指定Key
    @param val: 指定值
    @param rds: Redis服务器对象
    @param host: Redis服务器地址
    @param port: Redis服务器端口
    @return: 是否成功
    """

    # 取得Redis服务器
    rds = get_redis(rds, host, port)

    # 取得Key对应值
    logcm.print_info('Redis Set: %s --> %s' % (key, val))
    result = rds.set(key, val)
    logcm.print_obj(result, "result", show_header=False)
    # 返回值
    return result


def get_redis(rds=None, host=None, port=None):
    # 如果已经存在，直接返回。
    if rds is not None:
        return rds

    # 如果没有指定host，则从配置读取
    if host is None:
        host, port = load_redis_cfg()
    # 链接Redis服务器
    rds = redis.StrictRedis(host=host, port=port, db=0)
    return rds


def load_redis_cfg():
    """
    取得Redis配置，如果配置文件不存在则初始化
    @return: Redis服务器地址，Redis服务器端口
    """

    default_config = {
        'host': 'localhost',
        'port': 6379
    }
    # 加载配置文件
    cfg = loadcfgcm.load("redis_cfg.json", default_config)
    return cfg["host"], cfg["port"]
