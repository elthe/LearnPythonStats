# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Test Client common class
Test客户端共通类

Chrome 浏览器驱动安装
https://sites.google.com/a/chromium.org/chromedriver/getting-started
"""

import json

from common.browsercm import BrowserClient
from common import cryptcm
from common import datecm
from common import filecm
from common import logcm


class NetTestClient:
    def __init__(self, test_config):
        self.cfg = test_config
        # 公私钥字符串
        self.pub_key_str = filecm.read_str('./cache/crypt', 'public.key', "utf-8")
        self.token = None
        self.client = BrowserClient("Chrome")

    def check_result(self, result):
        """
        检验Result，如果访问失败，抛出异常。
        @param result: 访问结果
        @return: 是否成功
        """

        if "code" in result and result["code"] == "0":

            logcm.print_info("Result is ok.")
            return True
        elif "mCode" in result and result["mCode"] == "0":

            logcm.print_info("Result is ok.")
            return True
        else:
            msg = result["message"] if "message" in result else None
            msg = result["mMsg"] if "mMsg" in result else msg
            logcm.print_info("Result is error! %s" % msg, fg='red')
            return False

    def login(self, username, password):
        """
        使用指定用户名和密码，访问登录URL
        @param username: 用户名
        @param password: 密码
        @return: Token字符串
        """

        # 参数替换
        param = self.cfg["login_param"]
        param["userName"] = username
        param["passWord"] = password
        # 访问URL
        result = self.get_web_content(self.cfg["login_url"], param)
        # 检查结果
        if not self.check_result(result):
            return False
        # 返回Token
        self.token = result.data.token
        logcm.print_info("token : %s" % self.token)
        return True

    def default_login(self):
        """
        使用默认用户名和密码，访问登录URL
        @return: Token字符串
        """

        return self.login(self.cfg['username'], self.cfg['password'])

    def get_header(self, token_in_header=True):
        """
        取得WEB访问Header
        @param token_in_header: Token在Header中
        @return: Header对象
        """

        # Header对象
        header = {
            "terminal": self.cfg["terminal"],
            "appType": self.cfg["appType"],
            "appVersionNo": self.cfg["appVersionNo"],
            "accessTerminal": self.cfg["accessTerminal"],
            "reqTime": datecm.get_now_num()
        }
        # 在Header中存放Token
        if token_in_header and self.token is not None:
            header["token"] = self.token
        logcm.print_obj(header, "header")
        return header

    def get_web_content(self, url, param, token_in_header=True):
        """
        使用指定参数，访问URL
        @param url: URL
        @param param: 参数对象
        @param token_in_header: Token在Header中
        @return: URL返回内容
        """

        # 文本编码
        encoding = self.cfg['encoding']
        header = self.get_header(token_in_header)

        # 添加Token参数
        if not token_in_header and self.token is not None:
            param["token"] = self.token

        # 对象转JSON字符串
        logcm.print_obj(param, "param")
        param_json = json.dumps(param, separators=(',', ':'), ensure_ascii=False)
        # 加密
        encrypt_bytes = cryptcm.rsa_encrypt(self.pub_key_str, param_json.encode(encoding))
        encrypt_str = encrypt_bytes.hex()

        # 做成URL
        web_url = "%s/%s?data=%s" % (self.cfg["server"], url, encrypt_str)
        logcm.print_obj(web_url, "web_url")

        # 打开Browser浏览器
        content = self.client.open(web_url, "json")
        return content
