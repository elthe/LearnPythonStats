#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Redis使用示例。
"""

from common.rediscm import RedisClient
from common import checkcm
from common import loadcfgcm

# 配置
default_config = {
    'redis1': {
        'host': 'localhost',
        'port': 6379
    },
    'redis2': {
        'host': 'localhost',
        'port': 6379
    }
}

# 加载配置文件
cfg = loadcfgcm.load("net_redis_cfg.json", default_config)

# Redis服务器1
rds1 = RedisClient(cfg['redis1'])
# Redis服务器2
rds2 = RedisClient(cfg['redis2'])

# 字符串值
key1 = "test_key-1"
val1 = "112233"
# 设值示例
rds1.set_val(key1, val1)
# 取值示例
rst1 = rds1.get(key1)
# 确定取出值和存入值是否一致
checkcm.check_equal(val1, rst1, "redis string %s" % key1)

# 数值
key2 = "test_key-2"
val2 = 123
# 设值示例
rds2.set_val(key2, val2)
# 取值示例
rst2 = rds2.get(key2, convert=lambda x: int(x))
# 确定取出值和存入值是否一致
checkcm.check_equal(val2, rst2, "redis number %s" % key2)
