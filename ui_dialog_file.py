#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文件Dialog使用示例。
"""

from PyQt5.QtWidgets import QApplication
from common.widgetcm import MakeInputDialog
from common import logcm

input_item_list = [
    {
        "type": "dir",
        "key": "dir_name",
        "title": "打开目录",
        "desc": "选择目录:",
        "init": "./",
        "button": "Choose",
        "options": "",
    },
    {
        "type": "file",
        "key": "open_file",
        "title": "打开文件",
        "desc": "请选择文件:",
        "init": "./",
        "button": "Browse",
        "options": "Python Files (*.py)",
    },
    {
        "type": "files",
        "key": "open_files",
        "title": "一组文件",
        "desc": "请选择多个文件:",
        "init": "./",
        "button": "...",
        "options": "Text Files (*.txt)",
    },
    {
        "type": "save_file",
        "key": "save_file",
        "title": "保存文件",
        "desc": "选择保存文件:",
        "init": "./",
        "button": "...",
        "options": "Text Files (*.txt)",
    },
]


class TestFileInputDialog(MakeInputDialog):
    def __init__(self):
        super(TestFileInputDialog, self).__init__()
        self.create_ui()

    def create_ui(self):
        self.setWindowTitle("文件上传")
        self.setGeometry(500, 400, 300, 260)

        # 输入项目初始化
        self.make_input_ui(input_item_list)
        # 添加按钮
        self.add_button('ok', self.on_click_ok, 1)

    def on_click_ok(self):
        # 取得设定值
        val_map = self.get_val()
        logcm.print_obj(val_map, "val_map")
        return val_map


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    dialog = TestFileInputDialog()
    dialog.show()
    sys.exit(app.exec_())
