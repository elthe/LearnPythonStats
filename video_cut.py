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
    "start": 0,
    "end": 12    
}
'''

# 加载配置文件
cfg = loadcfgcm.load("video_cut.json", default_config)

# 视频剪切
videocm.cut_save(cfg['src_path'], cfg['start'], cfg['end'], cfg['target_path'])
