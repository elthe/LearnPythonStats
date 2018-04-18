# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
check common api
check 相关共通函数
"""

from common import logcm


def check_equal(obj1, obj2, title=""):
    """
    判断两个对象的值是否相等
    @param obj1: 对象1
    @param obj2: 对象2
    @param title: 对象描述
    @return: 是否OK
    """

    ok = (obj1 == obj2)
    if ok:
        logcm.print_info("Assert Ok for %s" % title)
    else:
        logcm.print_info("Assert Equal Fail for %s" % title, high_light=True)
        logcm.print_obj(obj1, title + "-1", show_header=False)
        logcm.print_obj(obj2, title + "-2", show_header=False)
    return ok
