# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
 Client common class
Test客户端共通类

Chrome 浏览器驱动安装
https://sites.google.com/a/chromium.org/chromedriver/getting-started
"""

import json
import time
import os

from common import logcm
from common import strcm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class BrowserClient:
    def __init__(self, browser_type):
        # 根据浏览器类型设置，打开浏览器
        if browser_type == "Chrome":
            # 打开Chrome浏览器
            self.browser = webdriver.Chrome('/opt/chrome/chromedriver')
        elif browser_type == "Firefox":
            fp = webdriver.FirefoxProfile()
            fp.set_preference("browser.download.folderList", 2)
            fp.set_preference("browser.download.manager.showWhenStarting", False)
            fp.set_preference("browser.download.dir", os.getcwd() + "/temp/download/")
            fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
            # 打开Firefox浏览器
            self.browser = webdriver.Firefox(firefox_profile=fp)
        elif browser_type == "Safari":
            # 打开Firefox浏览器
            self.browser = webdriver.Safari()

    def open(self, url, result_type="html", max_win=True, wait_seconds=5):
        """
        打开指定URL
        @param url: 指定URL
        @param result_type: 结果类型（html：HTML文本，text：TEXT文本，json：JSON文本）
        @param max_win: 窗口是否最大化
        @param wait_seconds: 等待秒数
        @return: 结果文本
        """

        logcm.print_info("Open web url %s." % url)
        self.browser.get(url)

        if max_win:
            # 将浏览器最大化显示
            self.browser.maximize_window()

        # 控制间隔时间，等待浏览器反映
        time.sleep(wait_seconds)

        # 根据结果类型，进行处理
        if result_type == "html":
            result = self.browser.page_source

        elif result_type == "text":
            body = self.browser.find_element_by_tag_name('body')
            result = body.text

        elif result_type == "json":
            body = self.browser.find_element_by_tag_name('body')
            # 满足JSON格式时，转换为字典
            if strcm.is_json(body.text):
                result = json.loads(body.text)
            else:
                logcm.print_info("Result : %s." % body.text, fg='red')
                raise Exception("Result is not Json (%s)" % body.text)

        logcm.print_obj(result, "result")
        return result

    def find_element(self, find_type, find_val):
        """
        根据指定查找类型和值查找页面元素
        @param find_type: 查找类型（name，id，xpath, css）
        @param find_val: 查找值
        @return: 元素对象
        """
        if find_type == "name":
            return self.browser.find_element_by_name(find_val)
        if find_type == "id":
            return self.browser.find_element_by_id(find_val)
        if find_type == "xpath":
            return self.browser.find_element_by_xpath(find_val)
        if find_type == "css":
            return self.browser.find_element_by_css_selector(find_val)
        if find_type == "class":
            return self.browser.find_element_by_class_name(find_val)
        if find_type == "link_full":
            return self.browser.find_element_by_link_text(find_val)
        if find_type == "link_part":
            return self.browser.find_element_by_partial_link_text(find_val)

    def set_input(self, find_type, find_val, input_str, do_clear=True):
        """
        向指定输入框，填写指定文本
        @param find_type: 查找类型（name，id，xpath）
        @param find_val: 查找值
        @param input_str: 输入文本
        @param do_clear: 是否先清空
        @return: 无
        """
        input_element = self.find_element(find_type, find_val)
        if do_clear:
            input_element.clear()
        input_element.send_keys(input_str)

    def do_click(self, find_type, find_val, wait_seconds=5):
        """
        根据指定路径找到元素并点击。
        @param find_type: 查找类型（name，id，xpath）
        @param find_val: 查找值
        @param wait_seconds: 等待秒数
        @return: 无
        """

        click_element = self.find_element(find_type, find_val)
        click_element.click()
        # 控制间隔时间，等待浏览器反映
        time.sleep(wait_seconds)

    def right_save(self, find_type, find_val):
        """
        根据指定路径找到元素并点击。
        @param find_type: 查找类型（name，id，xpath）
        @param find_val: 查找值
        @return: 无
        """

        click_element = self.find_element(find_type, find_val)
        # 移动到该元素
        action = ActionChains(self.browser).move_to_element(click_element)
        # 右键点击该元素
        action.context_click(click_element)
        # 点击键盘向下箭头
        action.send_keys(Keys.ARROW_DOWN)
        # 键盘输入V保存图
        action.send_keys('v')
        # 执行保存
        action.perform()

    def exe_actions(self, action_list):
        """
        按照指定动作列表执行操作。
        @param action_list: 动作列表
        @return: 无
        """

        for action in action_list:
            if action["action_type"] == "set_input":
                self.set_input(action["find_type"], action["find_val"], action["input_val"])
            elif action["action_type"] == "do_click":
                self.do_click(action["find_type"], action["find_val"])
            elif action["action_type"] == "right_save":
                elements = self.find_element(action["find_type"], action["find_val"])
                for element in elements:
                    self.right_save(element)

    def close(self):
        """
        关闭浏览器
        @return: 无
        """
        if self.browser:
            self.browser.quit()
