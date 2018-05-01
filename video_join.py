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
    "remark" : "视频组合",
    "src_clips": [
        {
            "path": "myopener.mp4",
            "start": 10,
            "end": 12
        },
        {
            "path": "video.mp4",
            "start": 10,
            "end": -18
        }
    ],
    "target_path": "video_con.mp4"
}
'''

# 加载配置文件
config_map = loadcfgcm.load("video_join.json", default_config)

# 视频组合
clip_list = []
for cfg in config_map["src_clips"]:
    clip = videocm.cut_save(cfg['src_path'], cfg['start'], cfg['end'])
    clip_list.append(clip)
videocm.concat_save(clip_list, config_map["target_path"])
