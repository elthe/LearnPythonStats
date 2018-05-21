# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
check common api
check 相关共通函数
"""

from common import logcm
from common import dictcm
from common import datecm
from common.classcm import BaseObject


class CheckRule(BaseObject):
    """
    校验规则类
    """

    def __init__(self, key, title, rule, **kwargs):
        # 关键词
        self.key = key
        # 标题
        self.title = title
        # 规则名
        self.rule = rule
        # 扩展参数
        self.args = kwargs


class CheckResult(BaseObject):
    """
    校验结果类
    """

    def __init__(self, ok, msg=None):
        # 是否OK
        self.ok = ok
        # 错误消息
        self.msg = msg


def check_obj_by_list(obj, check_list):
    """
    对对象按照校验列表进行校验
    :param obj:对象
    :param check_list:校验列表
    :return:(是否OK,错误消息列表)
    """
    is_ok_all = True
    msg_list = []
    for chk_rule in check_list:
        result = check_obj(obj, chk_rule)
        if not result.ok:
            is_ok_all = False
            msg_list.append(result.msg)
    return CheckResult(is_ok_all, msg_list)


def check_obj(obj, chk):
    """
    对对象的属性进行校验
    :param obj: 对象
    :param chk: 校验规则
    :return: (是否OK,错误消息)
    """

    if chk is None:
        return CheckResult(False, "校验规则未指定!")

    val = dictcm.get(obj, chk.key)
    if chk.rule == "length":
        return check_len(val, chk.title, **chk.args)
    elif chk.rule == "notnull":
        return check_notnull(val, chk.title, **chk.args)
    elif chk.rule == "in_list":
        return check_in_list(val, chk.title, **chk.args)
    elif chk.rule == "date":
        return check_date(val, chk.title, **chk.args)

    return CheckResult(True)


def check_date(obj, title="", check_format=None, fix_month=None, fix_day=None, fix_year=None, max_year=None,
               min_year=None, max_month=None, min_month=None, max_day=None, min_day=None):
    """
    非空校验
    :param obj: 对象
    :param title: 标题
    :param check_format: 日期格式
    :return:(是否OK,错误消息)
    """
    if obj is None:
        return CheckResult(True)

    if isinstance(obj, str) and check_format is not None:
        # 校验日期格式
        is_ok = datecm.check_date_format(obj, check_format)
        if not is_ok:
            msg = "%s不符合要求的日期格式:%s!" % (title, check_format)
            logcm.print_info(msg, fg='red')
            return CheckResult(False, msg)

    # if isinstance(obj, float):
    #     date = datecm.xldate_to_date(obj)


    return CheckResult(True)


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
        logcm.print_info("Assert Equal Fail for %s" % title, color='bold', fg='red')
        logcm.print_obj(obj1, title + "-1", show_header=False)
        logcm.print_obj(obj2, title + "-2", show_header=False)
    return ok


def check_in_list(obj, title="", range_list=None):
    """
    存在校验
    :param obj: 对象
    :param title: 标题
    :param range_list: 列表
    :return:(是否OK,错误消息)
    """
    if obj is None or range_list is None:
        return CheckResult(True)
    if obj not in range_list:
        msg = "%s不在允许值范围内!(允许值:%s,当前值:%s)" % (title, range_list, obj)
        logcm.print_info(msg, fg='red')
        return CheckResult(False, msg)
    return CheckResult(True)


def check_notnull(obj, title=""):
    """
    非空校验
    :param obj: 对象
    :param title: 标题
    :return:(是否OK,错误消息)
    """
    if obj is None or len(str(obj)) == 0:
        msg = "%s不能为空!" % title
        logcm.print_info(msg, fg='red')
        return CheckResult(False, msg)

    return CheckResult(True)


def check_len(obj, title="", max_len=None, min_len=None, fix_len=None):
    """
    长度校验(最小,最大,固定长度)
    :param obj: 对象
    :param title: 标题
    :param max_len:最大长度
    :param min_len:最小长度
    :param fix_len:固定长度
    :return: (是否OK,错误消息)
    """
    obj_len = len(obj)
    if fix_len is not None:
        if obj_len != fix_len:
            msg = "%s长度为%d,与要求的固定长度%d不同!" % (title, obj_len, fix_len)
            logcm.print_info(msg, fg='red')
            return CheckResult(False, msg)

    if max_len is not None:
        if obj_len > max_len:
            msg = "%s长度为%d,超过了要求的最大长度%d!" % (title, obj_len, max_len)
            logcm.print_info(msg, fg='red')
            return CheckResult(False, msg)

    if min_len is not None:
        if obj_len < min_len:
            msg = "%s长度为%d,小于要求的最小长度%d!" % (title, obj_len, min_len)
            logcm.print_info(msg, fg='red')
            return CheckResult(False, msg)

    return CheckResult(True)
