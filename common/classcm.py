# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
共通基类定义
"""

import json


class BaseObject:
    """
    共通基类（封装共通处理）
    """
    def props(self):
        """
        取得对象当前属性字典
        """
        pr = {}
        for name in dir(self):
            value = getattr(self, name)
            # 只返回数据属性，不包括方法
            if not name.startswith('__') and not callable(value):
                pr[name] = value
        return pr

    def __str__(self):
        """
        取得对象字符串
        """
        dict = self.props()
        # 把属性转成JSON字符串显示
        return json.dumps(dict, indent=4)
