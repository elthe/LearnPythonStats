# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Mail common api
Mail发送相关共通函数
"""

import os
import pycurl
import random
import urllib
import smtplib
import string

from common import filecm
from common import htmlcm
from common import logcm
from common import urlcm
from urllib import request


def login_smtp_server(host, port, user, pwd, have_ssl=False):
    """
    使用指定的IP，端口，用户及密码，登录到指定SMTP服务器。
    @param host: IP
    @param port: 端口
    @param user: 用户名
    @param pwd: 密码
    @param have_ssl: 使用SSL
    @return:返回邮件服务器链接对象
    """

    # 根据使用SSL与否使用类
    if have_ssl:
        server = smtplib.SMTP_SSL(host, port)
    else:
        server = smtplib.SMTP
        # 链接服务器
        server.connect(host, port)
        server.starttls()

    # 登录
    server.login(user, pwd)
    return server


def send_mail(server, mail_from, mail_to, subject, txt):
    """
    使用指定SMTP服务器，发送邮件
    @param server: 邮件服务器
    @param mail_from: 发件人
    @param mail_to: 收件人
    @param subject: 邮件主题
    @param txt: 邮件内容
    @return: 发送结果
    """

    # 拼接邮件正文
    BODY = string.join((
        "From: %s" % mail_from,
        "To: %s" % mail_to,
        "Subject: %s" % subject,
        "",
        txt
    ), "\r\n")

    return server.sendmail(mail_from, [mail_to], BODY)
