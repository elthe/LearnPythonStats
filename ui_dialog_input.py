#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
输入Dialog使用示例。
"""

from PyQt5.QtWidgets import QApplication
from common.widgetcm import MakeInputDialog
from common import logcm

input_item_list = [
    {
        "type": "text",
        "key": "project_name",
        "title": "项目名称",
        "desc": "输入项目名称:",
        "init": "PyQt5",
        "button": "设置..."
    },
    {
        "type": "select",
        "key": "project_type",
        "title": "项目性质",
        "desc": "请选择项目性质:",
        "init": "外包",
        "button": "选择...",
        "sel_list": ["外包", "自研"],
    },
    {
        "type": "int",
        "key": "project_member",
        "title": "项目人员",
        "desc": "请输入项目成员人数:",
        "init": "40",
        "button": "Set...",
        "min": 20,
        "max": 100,
        "step": 2,
    },
    {
        "type": "double",
        "key": "project_cost",
        "title": "项目成本",
        "desc": "输入项目成本:",
        "init": "400.98",
        "button": "设定",
        "min": 100.0,
        "max": 500.0,
        "step": 2,
    },
    {
        "type": "multiLineText",
        "key": "project_desc",
        "title": "项目介绍",
        "desc": "输入项目介绍:",
        "init": "服务外包第三方公司\nABCDEF",
        "button": "设定",
    },
]


class TestInputDialog(MakeInputDialog):
    def __init__(self):
        super(TestInputDialog, self).__init__()
        self.create_ui()

    def create_ui(self):
        self.setWindowTitle("项目信息")
        self.setGeometry(400, 400, 300, 260)

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
    dialog = TestInputDialog()
    dialog.show()
    sys.exit(app.exec_())
