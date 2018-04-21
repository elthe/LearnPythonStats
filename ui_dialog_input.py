#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dialog使用示例。
"""

from PyQt5.QtWidgets import QApplication

from common.widgetcm import MakeInputDialog

input_list = [
    {
        "type": "text",
        "title": "项目名称",
        "desc": "输入项目名称:",
        "init": "PyQt5",
        "button": "..."
    },
    {
        "type": "select",
        "title": "项目性质",
        "desc": "请选择项目性质:",
        "init": "外包",
        "button": "...",
        "sel_list": ["外包", "自研"],
    },
    {
        "type": "int",
        "title": "项目人员",
        "desc": "请输入项目成员人数:",
        "init": "40",
        "button": "...",
        "min": 20,
        "max": 100,
        "step": 2,
    },
    {
        "type": "double",
        "title": "项目成本",
        "desc": "输入项目成本:",
        "init": "400.98",
        "button": "...",
        "min": 100.0,
        "max": 500.0,
        "step": 2,
    },
    {
        "type": "textarea",
        "title": "项目介绍",
        "desc": "输入项目介绍:",
        "init": "服务外包第三方公司",
        "button": "...",
    },
]


class TestInputDialog(MakeInputDialog):
    def __init__(self):
        super(TestInputDialog, self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("项目信息")
        self.setGeometry(400, 400, 300, 260)

        self.make_input_ui(input_list)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    myshow = TestInputDialog()
    myshow.show()
    sys.exit(app.exec_())
