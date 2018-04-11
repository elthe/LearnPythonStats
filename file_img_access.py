#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图片文件访问
"""

from common import filecm
from common import imagecm
from common import logcm

# 读取图片尺寸
img_path = './images/draw_box_result.jpg'
size = imagecm.get_size(img_path)
logcm.print_obj(size, 'size')

# 调整图片尺寸并保存
save_path = './temp/draw_box_result_thumb.jpg'
imagecm.resize(img_path, 500, 500, save_path, keep_ratio=True)

# 检索图片列表
search_path = '/Volumes/Transcend/data/down/aaa/photo/makeH'
path_list = filecm.search_files(search_path, '.jpg', r'^[^\.]+')
logcm.print_obj(path_list, 'path_list')

# 横版图片路径列表
copy_list = []
for path in path_list:
    if imagecm.is_landscape(path):
        copy_list.append(path)
logcm.print_obj(copy_list, 'copy_list')

# 复制图片
copy_path = '/Volumes/Transcend/data/down/aaa/photo/makeW'
filecm.move_files(copy_list, copy_path)
