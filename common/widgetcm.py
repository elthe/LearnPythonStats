# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
widget common class
widget 相关共通类
"""

from common import logcm
from functools import partial
from PyQt5.QtWidgets import QWidget, QLineEdit, QInputDialog, QGridLayout, QLabel, QPushButton, QFrame
from PyQt5.QtWidgets import QFileDialog


class MakeInputDialog(QWidget):
    def __init__(self):
        super(MakeInputDialog, self).__init__()

    def make_input_ui(self, input_list):
        """
        做成输入画面
        @param input_list: 输入列表
        @return: 无
        """

        self.input_list = input_list
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        row_num = 0
        self.value_labels = []
        for item in self.input_list:
            title_label = QLabel(item["title"])
            value_label = QLabel(item["init"])
            value_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            self.value_labels.append(value_label)

            set_button = QPushButton(item['button'])
            set_button.clicked.connect(partial(self.do_input, row_num))

            self.mainLayout.addWidget(title_label, row_num, 0)
            self.mainLayout.addWidget(value_label, row_num, 1)
            self.mainLayout.addWidget(set_button, row_num, 2)
            row_num += 1

    def do_input(self, row_num):
        """
        执行输入设定
        @param row_num: 行号
        @return: 无
        """

        item = self.input_list[row_num]
        value_label = self.value_labels[row_num]

        title = item['title'] if 'title' in item else ''
        desc = item['desc'] if 'desc' in item else ''
        options = item['options'] if 'options' in item else ''
        item_type = item['type']
        logcm.print_info("Do input row %d type %s for %s"%(row_num, item_type, title))

        # 文本类型
        if item_type == "text":
            text, ok = QInputDialog.getText(self, title, desc,
                                            QLineEdit.Normal, value_label.text())
            if ok and (len(text) != 0):
                value_label.setText(text)
        # 多行文本
        if item_type == "textarea":
            text, ok = QInputDialog.getMultiLineText(self, title, desc,
                                                     value_label.text())
            if ok and (len(text) != 0):
                value_label.setText(text)

        # 选择
        elif item_type == "select":
            text, ok = QInputDialog.getItem(self, title, desc, item['sel_list'])
            if ok:
                value_label.setText(text)

        # 整数
        elif item_type == "int":
            number, ok = QInputDialog.getInt(self, title, desc, int(value_label.text()), item['min'], item['max'],
                                             item['step'])
            if ok:
                value_label.setText(str(number))

        # 浮点数
        elif item_type == "double":
            number, ok = QInputDialog.getDouble(self, title, desc, float(value_label.text()), item['min'], item['max'],
                                                item['step'])
            if ok:
                value_label.setText(str(number))

        # 打开目录
        elif item_type == "dir":
            dir_name = QFileDialog.getExistingDirectory(self, title, filter)
            if dir_name:
                value_label.setText(dir_name)

        # 打开文件
        elif item_type == "file":
            file_name = QFileDialog.getOpenFileName(self, title, filter, options)
            if file_name:
                value_label.setText(file_name)

        # 打开多个文件
        elif item_type == "files":
            file_list = QFileDialog.getOpenFileNames(self, title, filter, options)
            if file_list:
                value_label.setText(file_list)

        # 保存文件
        elif item_type == "save_file":
            file_name = QFileDialog.getSaveFileName(self, title, filter, options)
            if file_name:
                value_label.setText(file_name)
