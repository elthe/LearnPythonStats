# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
OpenGL common api
OpenGL相关共通函数
"""

import sys
from OpenGL.GLUT import *


def on_key_down(key, win_id):
    """
    按键处理
    :param key 按键值（字节）
    :param win_id 窗口ID
    :return: 按键值字符串
    """
    # 字节转字符串
    key = bytes.decode(key)
    # q or Escape
    if key == 'q' or ord(key) == 27:
        if win_id is not None:
            # 关闭窗体和它包含的子窗体
            glutDestroyWindow(win_id)
        # 退出软件
        sys.exit(0)
    return key
