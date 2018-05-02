#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
OPS使用示例。
"""

from common import loadcfgcm
from common import logcm
from common import diffcm
from common.netopscm import OpsClient

# 配置
default_config = """
{
    "dev": {
        "ip": "10.1.1.101",
        "port": 8080,
        "sys_name": "xxx",
        "sys_env": "dev",
        "encoding": "utf-8",
    },
    "test": {
        "ip": "10.1.1.102",
        "port": 8080,
        "sys_name": "xxx",
        "sys_env": "dev",
        "encoding": "utf-8",
    }
}
"""

# 加载配置文件
cfg = loadcfgcm.load("net_ops_cfg.json", default_config)

# 加载配置
ops_dev = OpsClient(cfg['dev'])
ops_test = OpsClient(cfg['test'])

# 读取开发环境OPS设置
dict_dev = ops_dev.load()
logcm.print_obj(dict_dev, "dict_dev")

# 读取测试环境OPS设置
dict_test = ops_test.load()
logcm.print_obj(dict_test, "dict_test")

# 比较OPS设置
diffcm.diff_by_dict(dict_dev, dict_test)

# 在开发环境OPS上增加新的键值
ops_dev.add("test_add01", "xyz")
dict_dev2 = ops_dev.load()

# 比较修改前后OPS设置
diffcm.diff_by_dict(dict_dev, dict_dev2)

# 在开发环境OPS上更新键值
ops_dev.update("test_add01", "abc")
dict_dev3 = ops_dev.load()

# 比较修改前后OPS设置
diffcm.diff_by_dict(dict_dev2, dict_dev3)

# 在开发环境OPS上删除键值
ops_dev.remove("test_add01")
dict_dev4 = ops_dev.load()

# 比较修改前后OPS设置
diffcm.diff_by_dict(dict_dev3, dict_dev4)
