#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
视频剪辑示例。
"""

from common import loadcfgcm
from common import videocm


# 缺省配置及说明
default_config = '''
{
    "remark" : "视频剪切保存",
    "src_path": "myopener.mp4",
    "target_path": "myopener_sub.mp4",
    "start_time": "01:02:00"
}
'''

# 加载配置文件
cfg = loadcfgcm.load("video_cut_os.json", default_config)

videocm.trim_save_os(cfg["src_path"], cfg["target_path"], cfg["start_time"])

