# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
check common api
check 相关共通函数
"""

import re

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


# 规则表达式字典
REGEX_MAP = {
    "country": r"[A-Z]{2}\([^\(\)]+\)",
    "key-name": r"[A-Z0-9]+-",
    "sort-no": r"[0-9]{3}"
}


def load_check_map(chk_cfg):
    """
    载入校验规则字典
    :param chk_cfg: 校验配置对象
    :return: 规则字典
    """
    chk_rule_map = {}
    for (cfg_key, cfg_list) in chk_cfg.items():
        cfg_rule_list = []
        for cfg_item in cfg_list:
            rule_list = load_check_list(cfg_item)
            cfg_rule_list += rule_list
        chk_rule_map[cfg_key] = cfg_rule_list
    return chk_rule_map


def load_check_list(cfg_item):
    """
    根据校验配置,取得校验规则列表
    :param cfg_item: 校验配置项
    :return:校验规则列表
    """
    rule_list = []
    for name in cfg_item["rules"]:
        args = dictcm.get(cfg_item["rule_args"], name, {})
        rule = CheckRule(cfg_item["key"], cfg_item["title"], name, **args)
        rule_list.append(rule)
    return rule_list


def check_obj_by_list(obj, check_list):
    """
    对对象按照校验列表进行校验
    :param obj:对象
    :param check_list:校验列表
    :return:校验结果对象
    """
    is_ok_all = True
    msg_list = []
    for chk_rule in check_list:
        result = check_obj(obj, chk_rule)
        if not result.ok:
            is_ok_all = False
            msg_list.append(result.msg)
    return CheckResult(is_ok_all, '\n'.join(msg_list))


def check_obj(obj, chk):
    """
    对对象的属性进行校验
    :param obj: 对象
    :param chk: 校验规则
    :return: 校验结果对象
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
    elif chk.rule == "number":
        return check_number(val, chk.title, **chk.args)
    elif chk.rule == "regex":
        return check_regex(val, chk.title, **chk.args)

    return CheckResult(True)


def check_date(obj, title="", check_format=None, **kwargs):
    """
    非空校验
    :param obj: 对象
    :param title: 标题
    :param check_format: 日期格式
    :return:校验结果对象
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

    # 取得日期值
    date_val = datecm.to_date(obj, check_format)
    if date_val is None:
        return CheckResult(True)

    # 年月日判断
    key_list = ["year", "month", "day"]
    name_list = ["年份", "月份", "日"]
    date_list = [date_val.year, date_val.month, date_val.day]
    for i in range(len(key_list)):
        key = key_list[i]
        val = date_list[i]
        name = name_list[i]
        # 固定值判断
        chk_val = dictcm.get(kwargs, "fix_" + key)
        if chk_val is not None and val != chk_val:
            msg = "%s的%s为%d,与要求的固定值%d不同!" % (title, name, val, chk_val)
            logcm.print_info(msg, fg='red')
            return CheckResult(False, msg)
        # 最小值判断
        chk_val = dictcm.get(kwargs, "min_" + key)
        if chk_val is not None and val < chk_val:
            msg = "%s的%s为%d,小于要求的最小值%d!" % (title, name, val, chk_val)
            logcm.print_info(msg, fg='red')
            return CheckResult(False, msg)
        # 最大值判断
        chk_val = dictcm.get(kwargs, "max_" + key)
        if chk_val is not None and val > chk_val:
            msg = "%s的%s为%d,大于要求的最大值%d!" % (title, name, val, chk_val)
            logcm.print_info(msg, fg='red')
            return CheckResult(False, msg)

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
    :return:校验结果对象
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
    :return:校验结果对象
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
    :return: 校验结果对象
    """
    if obj is None:
        return CheckResult(True)

    # 如果不是字符串类型,强制转换成字符串后校验
    if not isinstance(obj, str):
        obj = str(obj)

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


def check_number(obj, title="", max_val=None, min_val=None, fix_val=None):
    """
    数值校验(最小,最大,固定值)
    :param obj: 对象
    :param title: 标题
    :param max_val:最大值
    :param min_val:最小值
    :param fix_val:固定值
    :return: 校验结果对象
    """
    if obj is None:
        return CheckResult(True)

    if fix_val is not None:
        if obj != fix_val:
            msg = "%s值为%d,与要求的固定值%d不同!" % (title, obj, fix_val)
            logcm.print_info(msg, fg='red')
            return CheckResult(False, msg)

    if max_val is not None:
        if obj > max_val:
            msg = "%s值为%d,超过了要求的最大值%d!" % (title, obj, max_val)
            logcm.print_info(msg, fg='red')
            return CheckResult(False, msg)

    if min_val is not None:
        if obj < min_val:
            msg = "%s值为%d,小于要求的最小值%d!" % (title, obj, min_val)
            logcm.print_info(msg, fg='red')
            return CheckResult(False, msg)

    return CheckResult(True)


def check_regex(obj, title="", pattern=None, show_error=True):
    """
    规则表达式校验
    :param obj: 对象
    :param title: 标题
    :param pattern:规则表达式
    :param show_error:是否显示错误
    :return: 校验结果对象
    """
    if obj is None:
        return CheckResult(True)

    if not isinstance(obj, str):
        msg = "%s值为非字符串!" % title
        if show_error:
            logcm.print_info(msg, fg='red')
        return CheckResult(False, msg)

    if len(obj) == 0:
        return CheckResult(True)

    if pattern is not None and pattern in REGEX_MAP:
        ptn = re.compile(REGEX_MAP[pattern])
        if not ptn.match(obj):
            msg = "%s值为%s,不符合要求的规则表达式:%s!" % (title, obj, pattern)
            if show_error:
                logcm.print_info(msg, fg='red')
            return CheckResult(False, msg)

    return CheckResult(True)
