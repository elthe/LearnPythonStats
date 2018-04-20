# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
check common api
check 相关共通函数
"""

from common import logcm
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QInputDialog, QGridLayout, QLabel, QPushButton, QFrame
from PyQt5.QtWidgets import QFileDialog


def make_input_ui(parent, input_list, layout):
    """
    做成输入画面
    @param parent: 父对象
    @param input_list: 输入列表
    @param layout: Layout
    @return: 无
    """

    row_num = 0
    for item in input_list:
        title_label = QLabel(item["title"])
        value_label = QLabel(item["init"])
        value_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        set_button = QPushButton(item['button'])
        set_button.clicked.connect(
            lambda: do_input(parent, item=item, value_label=value_label))
        layout.addWidget(title_label, row_num, 0)
        layout.addWidget(value_label, row_num, 1)
        layout.addWidget(set_button, row_num, 2)
        row_num += 1


def do_input(parent, item, value_label=None):
    """
    执行输入设定
    @param parent: 父对象
    @param type: 类型
    @return: 无
    """

    title = item['title'] if 'title' in item else ''
    desc = item['desc'] if 'desc' in item else ''
    options = item['options'] if 'options' in item else ''

    if type == "text":
        text, ok = QInputDialog.getText(parent, title, desc,
                                        QLineEdit.Normal, value_label.text())
        if ok and (len(text) != 0):
            value_label.setText(text)

    if type == "textarea":
        text, ok = QInputDialog.getMultiLineText(parent, title, desc,
                                                 value_label.text())
        if ok and (len(text) != 0):
            value_label.setText(text)

    elif type == "select":
        text, ok = QInputDialog.getItem(parent, title, desc, item['sel_list'])
        if ok:
            value_label.setText(text)

    elif type == "int":
        number, ok = QInputDialog.getInt(parent, title, desc, int(value_label.text()), item['min'], item['max'], item['step'])
        if ok:
            value_label.setText(str(number))

    elif type == "double":
        number, ok = QInputDialog.getDouble(parent, title, desc, float(value_label.text()), item['min'], item['max'], item['step'])
        if ok:
            value_label.setText(str(number))

    elif type == "dir":
        dir_name = QFileDialog.getExistingDirectory(parent, title, filter)
        if dir_name:
            value_label.setText(dir_name)

    elif type == "file":
        file_name = QFileDialog.getOpenFileName(parent, title, filter, options)
        if file_name:
            value_label.setText(file_name)

    elif type == "files":
        file_list = QFileDialog.getOpenFileNames(parent, title, filter, options)
        if file_list:
            value_label.setText(file_list)

    elif type == "save_file":
        file_name = QFileDialog.getSaveFileName(parent, title, filter, options)
        if file_name:
            value_label.setText(file_name)
