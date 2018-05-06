#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图片文件访问
"""

from common import filecm
from common import imagecm
from common import logcm
from common import loadcfgcm

# 读取图片尺寸
img_path = './images/draw_box_result.jpg'
size = imagecm.get_size(img_path)
logcm.print_obj(size, 'size')

# 调整图片尺寸并保存
save_path = './temp/draw_box_result_thumb.jpg'
imagecm.resize(img_path, 500, 500, save_path, keep_ratio=True)

default_config = """
{
    "remark" : "图片按照横竖分类复制或移动",
     "action" : "copy|move",
    "src_path": "",
    "target_path_w": "",
    "target_path_h": "",
    "skeep_exist": true
}
"""

# 加载配置文件
cfg = loadcfgcm.load("file_img_movecopy.json", default_config)

# 检索图片列表
search_path = ''
path_list = filecm.search_files(cfg["src_path"], '.jpg', r'^[^\.]+')
logcm.print_obj(path_list, 'path_list')

# 横版图片路径列表
w_list = []
h_list = []
for path in path_list:
    if imagecm.is_landscape(path):
        w_list.append(path)
    else:
        h_list.append(path)
logcm.print_obj(w_list, 'w_list')
logcm.print_obj(h_list, 'h_list')

# 复制图片
if cfg['action'] == "copy":
    filecm.copy_files(w_list, cfg['target_path_w'], skeep_exist=cfg['skeep_exist'])
    filecm.copy_files(h_list, cfg['target_path_h'], skeep_exist=cfg['skeep_exist'])

# 移动图片
elif cfg['action'] == "move":
    filecm.move_files(w_list, cfg['target_path_w'])
    filecm.move_files(h_list, cfg['target_path_h'])

