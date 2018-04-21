#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dialog使用示例。
"""

from PyQt5.QtWidgets import QApplication

from common.widgetcm import MakeInputDialog

input_list = [
    {
        "type": "dir",
        "title": "打开目录",
        "desc": "选择目录:",
        "init": "./",
        "button": "select"
    },
    {
        "type": "file",
        "title": "打开文件",
        "desc": "请选择文件:",
        "init": "",
        "button": "...",
    },
    {
        "type": "files",
        "title": "一组文件",
        "desc": "请选择多个文件:",
        "init": "",
    },
    {
        "type": "save_file",
        "title": "保存文件",
        "desc": "选择保存文件:",
        "init": "",
    },
]


class TestFileInputDialog(MakeInputDialog):
    def __init__(self):
        super(TestFileInputDialog, self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("文件上传")
        self.setGeometry(500, 400, 300, 260)

        self.make_input_ui(input_list)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    myshow = TestFileInputDialog()
    myshow.show()
    sys.exit(app.exec_())
