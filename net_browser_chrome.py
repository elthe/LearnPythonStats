#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
网络测试使用示例。
"""

from common import loadcfgcm
from common.browsercm import BrowserClient

# 配置
default_config = """
{
    "browser_type": "Chrome",
    "url": "https://www.baidu.com/",
    "actionList": [
        {
            "find_type": "id",
            "find_val": "kw",
            "action_type": "set_input",
            "input_val": "翻转"
        },
        {
            "find_type": "id",
            "find_val": "su",
            "action_type": "do_click"
        }
    ]
}
"""

# 加载配置文件
cfg = loadcfgcm.load("net_browser_chrome.json", default_config)

# 测试客户端
client = BrowserClient(cfg["browser_type"])
client.open(cfg["url"])

client.exe_actions(cfg["actionList"])


