#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
XML 文件读取示例
"""

from common import logcm
from common import xmlcm

# XML文件读取
in_files = "./data/xmlcncrstest.xml"
tree = xmlcm.xml_to_dict(xml_path=in_files)
logcm.print_obj(tree, "tree", show_json=True)

# XML文件输出
out_file = "./temp/xmlout.xml"
xmlcm.dict_to_xml(tree, save_path=out_file)
