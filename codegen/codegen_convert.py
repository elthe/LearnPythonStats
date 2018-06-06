#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
代码生成模版转换共通
"""

import re
from common import diffcm
from common import logcm
from common import filecm


def convert_freemarker_path(fm_path):
    """
    把指定目录下的模版文件中的Freemark语法，同一替换成Jinjia2语法
    :param fm_path: 指定目录
    :return:无
    """
    path_list = filecm.search_files(fm_path, ".tpl,.json,.ftl")
    for tpl_path in path_list:
        fm_str = filecm.read_str(file_name=tpl_path)
        jj_str = freemarker_to_jinjia2(fm_str)
        diffcm.diff_by_text(fm_str, jj_str)
        filecm.save_str(jj_str, file_name=tpl_path)


def freemarker_to_jinjia2(fm_str):
    """
    Freemarker模版转换成Jinjia2模版
    :param fm_str: Freemarker模版文本
    :return: Jinjia2模版文本
    """
    # 变量转换 ${config.xxxx} -> {{config.xxxx}}
    p = re.compile(r'\$\{([^\{\}]+)\}')
    out_str = re.sub(p, r'{{\1}}', fm_str)

    # if转换
    # <#if (...) > -> {% if ... %}
    p = re.compile(r'<#if *\(([^<>]+)\) *>')
    out_str = re.sub(p, r'{% if \1 %}', out_str)
    # </#if> -> {% endif %}
    out_str = out_str.replace("</#if>", "{% endif %}")
    # <#if x_has_next>
    p = re.compile(r'<#if *[^<>]+has_next *>')
    out_str = re.sub(p, r'{% if not loop.last %}', out_str)


    # list转换
    # <#list ... as .. > -> {% for .. in ... %}
    p = re.compile(r'<#list *([^ ]+) +as +([^ ]+) *>')
    out_str = re.sub(p, r'{% for \2 in \1 %}', out_str)
    # </#if> -> {% endif %}
    out_str = out_str.replace("</#list>", "{% endfor %}")

    # ?处理清除
    # {{...?..}} -> {{...}}
    p = re.compile(r'\{\{([^\{\}\?]+)\?([^\{\}\?]+)\}\}')
    out_str = re.sub(p, r'{{\1}}', out_str)

    return out_str


if __name__ == '__main__':
    # fm_str = filecm.read_str(file_name="./template/xls_to_interface/tpl_config.json")
    tpl_path = "./template/xls_to_interface/service/core_java_test_service.tpl"
    fm_str = filecm.read_str(file_name=tpl_path)
    jj_str = freemarker_to_jinjia2(fm_str)
    diffcm.diff_by_text(fm_str, jj_str)
    filecm.save_str(jj_str, file_name=tpl_path)
    # convert_freemarker_path("./template/xls_to_interface/")
    # core_java_test_service

