#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
XML 文件读取示例
"""

from common import logcm
from common import xmlcm

# XML文件读取
in_files = "./data/xmltest.xml"
tree = xmlcm.read_xml(in_files)
logcm.print_obj(tree, "tree")

if tree is not None:
    # 将xml转换为dict
    node_dict = xmlcm.xml_to_dict(tree.getroot())
    logcm.print_obj(node_dict, "node_dict", show_json=True)

    # dict增加属性
    node_dict[3] = {'rank': '3', 'year': '2008', 'gdppc': '141103', 'neighbor': None}
    node_dict[4] = {'rank': '4', 'year': '2007', 'gdppc': '141104', 'neighbor': None}
    logcm.print_obj(node_dict, "node_dict", show_json=True)

    # 将dict转换为xml
    root = xmlcm.dict_to_xml(node_dict, "dataRoot", "node")
    # 输出xml到out_files
    out_file = "./temp/xmlout.xml"
    xmlcm.save_xml(root, out_file)
