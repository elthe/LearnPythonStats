#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Redis使用示例。
"""

from common import rediscm
from common import assertcm

# Rdis服务器设置
host = "10.1.1.202"
port = 7002
rds = rediscm.get_redis(None, host, port)

# 字符串值
key = "test_key1"
val = "test_value"
# 设值示例
rst1 = rediscm.set_val(key, val, rds=rds)
# 取值示例
rst2 = rediscm.get(key, rds=rds)
# 确定取出值和存入值是否一致
assertcm.check_equal(val, rst2, "redis string val")

# 数值
key = "test_key2"
val = 12
# 设值示例
rst1 = rediscm.set_val(key, val,rds=rds)
# 取值示例
rst2 = rediscm.get(key, rds=rds)
# 确定取出值和存入值是否一致
assertcm.check_equal(val, rst2, "redis number val")
