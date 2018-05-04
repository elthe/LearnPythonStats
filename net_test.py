#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
网络测试使用示例。
"""

from common import loadcfgcm
from common.nettestcm import NetTestClient

# 配置
default_config = """
{
    "server": "http://xxxx.xxxx.com.cn/xxx-gw",
    "login_url": "xxxx/xxxLogin.app",
    "login_param": "{'userName':'[username]','passWord':'[password]'}",
    "username": "xxxx",
    "password": "123456",    
    "terminal": "APP",
    "appType": "ios",
    "appVersionNo": "1.0",
    "accessTerminal": "---JUNIT----",
    "encoding": "utf-8",
    "test_uri": "xxxx/xxxxxxx.app",
    "test_param": {"listType":"TJ","pageSize":"10"} 
}
"""

# 加载配置文件
cfg = loadcfgcm.load("net_test.json", default_config)

# 测试客户端
client = NetTestClient(cfg)
isOk = client.default_login()

# 测试URL
uri = cfg["test_uri"]
param = cfg["test_param"]
content = client.get_web_content(uri, param, True)
