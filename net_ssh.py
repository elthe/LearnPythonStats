#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SSH使用示例。
"""

from common import loadcfgcm
from common.netsshcm import SshClient

# 配置
default_config = """
{
    "ip": "10.1.1.101",
    "port": 22,
    "username": "xxxxxxx",
    "password": "xxxx",
    "remoteFile": "/usr/local/logs/xxx.log"
}
"""

# 加载配置文件
cfg = loadcfgcm.load("net_ssh_tail.json", default_config)

# SSH连接
ssh = SshClient(cfg)
ssh.tail_print(cfg['remoteFile'])

# 关闭连接
# sshcm.close_ssh_conn(ssh, sftp)
