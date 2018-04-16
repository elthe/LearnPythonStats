#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SMTP邮件发送示例。
"""

from common import loadcfgcm
from common import logcm
from common import mailcm

# 缺省配置及说明
default_server = {
    "host": "smtp.gmail.com",
    "port": 25,
    "user": "test@gmail.com",
    "pwd": "123456",
    "ssl": "True"
}

default_mails = {
    "mail_list": [
        {
            "from": "test@gmail.com",
            "to": "test@gmail.com",
            "subject": "Welcome Home",
            "content": "Hello, my friend, we are looking for you."
        }
    ]
}

# 加载配置文件
cfg = loadcfgcm.load("net_smtp_server.json", default_server)
mails = loadcfgcm.load("net_smtp_mails.json", default_mails)

# 登录服务器
server = mailcm.login_smtp_server(cfg["host"], cfg["port"], cfg["user"], cfg["pwd"], bool(cfg["ssl"]))
logcm.print_obj(server, "server")

# 发送邮件
for mail in mails["mail_list"]:
    result = mailcm.send_mail(server, mail["from"], mail["to"], mail["subject"], mail["content"])
    logcm.print_obj(result, "result-%s" % mail["subject"])

# 退出服务器
server.quit()
