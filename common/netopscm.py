# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
OPS Client common class
OPS客户端共通类
"""

from common import logcm
from common import webcm
from common import htmlcm


class OpsClient:
    def __init__(self, ops_config):
        self.cfg = ops_config

    def get_url(self, method, key=None, val=None):
        """
        根据当前方法，取得URL
        @param method: 取值范围：（add, load, update, del）
        @param key: 设置键
        @param val: 设置值
        @return: URL
        """

        if method == 'add':
            url = "http://%s:%d/ops/zk?method=zkAdd&nameList=%s&envList=%s&inputKeyAdd=%s&inputValueAdd=%s" % (
                self.cfg["ip"], self.cfg['port'], self.cfg['sys_name'], self.cfg['sys_env'], key, val)

        elif method == 'load':
            url = "http://%s:%d/ops/zk?method=zkLoad&nameList2=%s&envList2=%s&" % (
                self.cfg["ip"], self.cfg['port'], self.cfg['sys_name'], self.cfg['sys_env'])

        elif method == 'update':
            url = "http://%s:%d/ops/zk?method=zkSetData&nameList3=%s&envList3=%s&inputKey=%s&inputValue=%s" % (
                self.cfg["ip"], self.cfg['port'], self.cfg['sys_name'], self.cfg['sys_env'], key, val)

        elif method == 'del':
            url = "http://%s:%d/ops/zk?method=zkDelData&nameList4=%s&envList4=%s&inputKey=%s&inputValue=%s" % (
                self.cfg["ip"], self.cfg['port'], self.cfg['sys_name'], self.cfg['sys_env'], key, val)

        logcm.print_info("ops link url is : %s " % url)
        return url

    def load(self):
        """
        取得所有设定值
        @return: 设定值的键值字典
        """

        logcm.print_info("Loading all ops values ...")
        # 取得访问URL
        url = self.get_url('load')

        # OPS服务器的设定画面访问
        html = webcm.read_url(url, self.cfg['encoding'])
        soup = htmlcm.to_soup(html)
        ops_map = {}

        # OPS网页的表格解析
        trs = soup.select("body table tr")
        for i in range(1, len(trs)):
            tr = trs[i]
            tds = tr.select("td")
            if len(tds) == 4:
                key = tds[2].string
                val = tds[3].string
                ops_map[key] = val

        return ops_map

    def add(self, key, val):
        """
        在指定OPS服务器上，添加新的键值
        @param key: 设置键
        @param val: 设置值
        @return: 无
        """

        logcm.print_info("Add ops value (key : %s, val : %s )" % (key, val))

        # 取得访问URL
        url = self.get_url('add', key, val)

        # 请求OPS服务器
        webcm.read_url(url, self.cfg['encoding'])

    def update(self, key, val):
        """
        在指定OPS服务器上，更新指定的键值
        @param key: 设置键
        @param val: 设置值
        @return: 无
        """

        logcm.print_info("Update ops value (key : %s, val : %s )" % (key, val))

        # 取得访问URL
        url = self.get_url('update', key, val)

        # 请求OPS服务器
        webcm.read_url(url, self.cfg['encoding'])

    def remove(self, key):
        """
        在指定OPS服务器上，删除指定的键
        @param key: 设置键
        @return: 无
        """

        logcm.print_info("Remove ops key (key : %s)" % key)

        # 取得访问URL
        url = self.get_url('del', key)

        # 请求OPS服务器
        webcm.read_url(url, self.cfg['encoding'])
