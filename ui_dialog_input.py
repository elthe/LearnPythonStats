#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dialog使用示例。
"""

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QInputDialog, QGridLayout, QLabel, QPushButton, QFrame

from common import widgetcm

input_list = [
    {
        "type": "text",
        "title": "项目名称",
        "desc": "输入项目名称:",
        "init": "PyQt5",
        "button": "...",
        "sel_list": [],
        "min": 0,
        "max": 100,
        "step": 2,
        "filter": "",
        "options": "",
    },
    {
        "type": "select",
        "title": "项目性质",
        "desc": "请选择项目性质:",
        "init": "外包",
        "button": "...",
        "list": ["外包", "自研"],
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


class InputDialog(QWidget):
    def __init__(self):
        super(InputDialog, self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("项目信息")
        self.setGeometry(400, 400, 300, 260)
        mainLayout = QGridLayout()

        widgetcm.make_input_ui(self, input_list, mainLayout)

        self.setLayout(mainLayout)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    myshow = InputDialog()
    myshow.show()
    sys.exit(app.exec_())
