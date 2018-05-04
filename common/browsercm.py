# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Test Client common class
Test客户端共通类

Chrome 浏览器驱动安装
https://sites.google.com/a/chromium.org/chromedriver/getting-started
"""

import json

from common import logcm
from common import strcm
from selenium import webdriver


def open_by_chrome(url, result_type="html"):
    """
    使用Chrome浏览器，打开指定URL
    @param url: 指定URL
    @param result_type: 结果类型（html：HTML文本，text：TEXT文本，json：JSON文本）
    @return: 结果文本
    """

    # 打开Chrome浏览器
    browser = webdriver.Chrome('/opt/chrome/chromedriver')
    logcm.print_info("Open web url %s." % url)
    browser.get(url)

    # 根据结果类型，进行处理
    if result_type == "html":
        result = browser.page_source

    elif result_type == "text":
        body = browser.find_element_by_tag_name('body')
        result = body.text

    elif result_type == "json":
        body = browser.find_element_by_tag_name('body')
        # 满足JSON格式时，转换为字典
        if strcm.is_json(body.text):
            result = json.loads(body.text)
        else:
            logcm.print_info("Result : %s." % body.text, fg='red')
            raise Exception("Result is not Json (%s)" % body.text)

    logcm.print_obj(result, "result")
    browser.quit()
    return result
