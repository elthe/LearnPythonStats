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

    def make_input_ui(self, _input_list):
        """
        做成输入画面
        @param _input_list: 输入列表
        @return: 无
        """

        self.inputList = _input_list
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        self.row_num = 0
        self.valueLabels = []
        for item in self.inputList:
            title_label = QLabel(item["title"])
            value_label = QLabel(item["init"])
            value_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            self.valueLabels.append(value_label)

            set_button = QPushButton(item['button'])
            set_button.clicked.connect(partial(self.do_input, self.row_num))

            self.mainLayout.addWidget(title_label, self.row_num, 0)
            self.mainLayout.addWidget(value_label, self.row_num, 1)
            self.mainLayout.addWidget(set_button, self.row_num, 2)
            self.row_num += 1

    def do_input(self, row):
        """
        执行输入设定
        @param row: 行号
        @return: 无
        """

        item = self.inputList[row]
        value_label = self.valueLabels[row]
        val = value_label.text()

        title = item['title'] if 'title' in item else ''
        desc = item['desc'] if 'desc' in item else ''
        options = item['options'] if 'options' in item else ''
        item_type = item['type']
        logcm.print_info("Do input row %d type %s for %s" % (row, item_type, title))

        # 文本类型
        if item_type == "text":
            text, ok = QInputDialog.getText(self, title, desc, QLineEdit.Normal, val)
            logcm.print_info("Text Input end( ok : %s, text : %s )" % (str(ok), text))
            if ok and (len(text) != 0):
                value_label.setText(text)

        # 多行文本
        if item_type == "multiLineText":
            text, ok = QInputDialog.getMultiLineText(self, title, desc, val)
            logcm.print_info("MultiLineText Input end( ok : %s, text : %s )" % (str(ok), text))
            if ok and (len(text) != 0):
                value_label.setText(text)
                value_label.adjustSize()

        # 选择
        elif item_type == "select":
            text, ok = QInputDialog.getItem(self, title, desc, item['sel_list'])
            logcm.print_info("Select Item Input end( ok : %s, text : %s )" % (str(ok), text))
            if ok:
                value_label.setText(text)

        # 整数
        elif item_type == "int":
            number, ok = QInputDialog.getInt(self, title, desc, int(val), item['min'], item['max'],
                                             item['step'])
            logcm.print_info("Int Input end( ok : %s, number : %d )" % (str(ok), number))
            if ok:
                value_label.setText(str(number))

        # 浮点数
        elif item_type == "double":
            number, ok = QInputDialog.getDouble(self, title, desc, float(val), item['min'], item['max'],
                                                item['step'])
            logcm.print_info("Double Input end( ok : %s, number : %f )" % (str(ok), number))
            if ok:
                value_label.setText(str(number))

        # 打开目录
        elif item_type == "dir":
            dir_name = QFileDialog.getExistingDirectory(self, desc, val)
            logcm.print_info("ExistingDirectory Input end( dir_name : %s )" % dir_name)
            if dir_name:
                value_label.setText(dir_name)

        # 打开文件
        elif item_type == "file":
            file_name, file_type = QFileDialog.getOpenFileName(self, desc, val, options)
            logcm.print_info("OpenFileName Input end( file_name : %s, file_type : %s )" % (file_name, file_type))
            if file_name:
                value_label.setText(file_name)

        # 打开多个文件
        elif item_type == "files":
            file_list, file_type = QFileDialog.getOpenFileNames(self, desc, val, options)
            logcm.print_info("OpenFileNames Input end( file_type : %s, file_list : %s )" % (file_type, file_list))
            if file_list:
                value_label.setText("\n".join(file_list))
                value_label.adjustSize()

        # 保存文件
        elif item_type == "save_file":
            file_name, file_type = QFileDialog.getSaveFileName(self, desc, val, options)
            logcm.print_info("SaveFileName Input end( file_type : %s, file_name : %s )" % (file_type, file_name))
            if file_name:
                value_label.setText(file_name)

    def add_button(self, btn_txt, call_func, pos_index):
        """
        在末尾添加按钮
        @param btn_txt: 按钮文本
        @param call_func: 回调方法
        @param pos_index: 位置索引
        @return:无
        """

        set_button = QPushButton(btn_txt)
        set_button.clicked.connect(call_func)
        self.mainLayout.addWidget(set_button, self.row_num, pos_index)

    def get_val(self):
        """
        取值
        @return: 表单内容字典
        """

        val_map = {}
        for i in range(len(self.inputList)):
            item = self.inputList[i]
            key = item["key"]
            value_label = self.valueLabels[i]
            val = value_label.text()
            val_map[key] = val

        return val_map
