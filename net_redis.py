#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Redis使用示例。
"""

from common import rediscm
from common import checkcm

# Redis服务器1
rds1 = rediscm.get_redis(host="10.1.1.202", port=7002)
key1 = "test_key-1"
# Redis服务器2
rds2 = rediscm.get_redis(host="10.1.1.202", port=7000)
key2 = "test_key-2"

# 字符串值
val1 = "112233"
# 设值示例
rediscm.set_val(key1, val1, rds=rds1)
# 取值示例
rst1 = rediscm.get(key1, rds=rds1)
# 确定取出值和存入值是否一致
checkcm.check_equal(val1, rst1, "redis string %s" % key1)

# 数值
val2 = 123
# 设值示例
rediscm.set_val(key2, val2, rds=rds2)
# 取值示例
rst2 = rediscm.get(key2, rds=rds2, convert=lambda x: int(x))
# 确定取出值和存入值是否一致
checkcm.check_equal(val2, rst2, "redis number %s" % key2)
