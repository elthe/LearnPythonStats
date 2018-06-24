#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图片文件访问
"""
import os
from common import filecm
from common import imagecm
from common import logcm
from common import loadcfgcm

default_config = """
{
    "remark" : "图片批量转换格式，大小，并移动",
     "action" : "copy|move",
    "src_path": "",
    "target_path": "",
    "target_w": 1280,
    "target_h": 800,
    "src_ext": "png",
    "target_ext": "jpg"
}
"""

# 加载配置文件
cfg = loadcfgcm.load("file_img_convert.json", default_config)

# 检索图片列表
search_path = ''
path_list = filecm.search_files(cfg["src_path"], '.' + cfg["src_ext"], r'^[^\.]+')
logcm.print_obj(path_list, 'path_list')

# 横版图片路径列表
w_list = []
h_list = []
count = 1
for path in path_list:
    # 调整图片尺寸并保存
    (file_path, file_name) = os.path.split(path)
    (short_name, extension) = os.path.splitext(file_name)
    # 修改大小
    im_new = imagecm.resize(path, cfg["target_w"], cfg["target_h"], keep_ratio=True)
    # PNG转JPG
    im_new = im_new.convert("RGB")
    # 保存
    save_path = os.path.join(cfg["target_path"], short_name + "." + cfg["target_ext"])
    im_new.save(save_path, quality=100)
    logcm.print_info("No.%d converted %s." % (count, short_name))
    # 删除源文件
    os.remove(path)
    count += 1
