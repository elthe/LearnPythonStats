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
    "cut_save": {
        "remark" : "视频剪切保存",
        "src_path": "myopener.mp4",
        "target_path": "myopener_sub.mp4",
        "start": 0,
        "end": 12
    },
    "concate_clips": {
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
}
'''

# 加载配置文件
config_map = loadcfgcm.load("movie_cut1.json", default_config)

# 视频剪切
cfg = config_map["cut_save"]
videocm.cut_save(cfg['src_path'], cfg['start'], cfg['end'], cfg['target_path'])

# 视频组合
cfg2 = config_map["concate_clips"]
clip_list = []
for cfg in cfg2["src_clips"]:
    clip = videocm.cut_save(cfg['src_path'], cfg['start'], cfg['end'])
    clip_list.append(clip)
videocm.concat_save(clip_list, cfg2["target_path"])
