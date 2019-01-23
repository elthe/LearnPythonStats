# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
SSH Pool class
SSH Pool 共通类
"""

from common import dictcm
from common import logcm
from common.netsshcm import SshClient


class SshPool:
    # 客户端Map
    clientMap = {}

    def __init__(self):
        logcm.print_info("SshPool is Init！")

    @staticmethod
    def getSshClient(ssh_config):
        """
        取得SSHClient
        """
        ip = dictcm.get(ssh_config, "ip")
        ssh = dictcm.get(SshPool.clientMap, ip)
        if ssh is None:
            logcm.print_info("SshClient not found for %s！" % ip)
            ssh = SshClient(ssh_config)
            SshPool.clientMap[ip] = ssh
        else:
            ssh.addCount()
            logcm.print_info("SshClient count: %d for %s！" % (ssh.count, ip))

        return ssh

    def __del__(self):
        """
        关闭SSH连接
        @return: 无
        """
        SshPool.clientMap.clear()
        SshPool.clientMap = {}
        logcm.print_info("SshPool is Closed！")
