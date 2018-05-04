# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
XML common api
XML相关共通函数
"""

import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET

from common import logcm


def read_xml(xml_path):
    """
    通过XML文件得到Tree对象
    @param xml_path: XML文件路径
    @return: Tree对象
    """

    try:
        logcm.print_info("Reading xml file : %s" % xml_path)
        tree = ET.parse(xml_path)
        return tree
    except Exception as e:
        logcm.print_info("Reading xml error! %s" % e, fg='red')
        return None


def xml_to_dict(root):
    """
    把xml转换成dict
    @param root: XML的Root对象
    @return: dict对象
    """

    dict_new = {}
    for key, value in enumerate(root):
        dict_init = {}
        list_init = []
        for item in value:
            list_init.append([item.tag, item.text])
            for lists in list_init:
                dict_init[lists[0]] = lists[1]
        dict_new[key] = dict_init
    return dict_new


def dict_to_xml(input_dict, root_tag, node_tag):
    """
    把dict转换成XML
    @param input_dict: 输入dict对象
    @param root_tag: 根节点标签名
    @param node_tag: 子节点标签名
    @return: XML的Root对象
    """

    # 新建根节点
    root = ET.Element(root_tag)
    # 遍历字典
    for (k, v) in input_dict.items():
        # 新建子节点
        sub_node = ET.SubElement(root, node_tag)
        # 遍历二级字典
        for (key, val) in sorted(v.items(), key=lambda e: e[0], reverse=True):
            # 新建二级子节点
            ext_node = ET.SubElement(sub_node, key)
            ext_node.text = val
    return root


def save_xml(root, out_file, encoding="utf-8"):
    """
    格式化root转换为xml文件
    @param root: 根节点
    @param out_file: xml文件
    @param encoding: 文本编码
    @return: 无
    """

    try:
        logcm.print_info("Saving xml file --> %s" % out_file)

        # 取得XML字节流
        xml_bytes = ET.tostring(root, encoding)

        # 解析XML文档
        xml_doc = minidom.parseString(xml_bytes)

        # 写入XML文件
        with open(out_file, "w+") as file:
            xml_doc.writexml(file, addindent=" ", newl="\n", encoding=encoding)

    except Exception as e:
        logcm.print_info("Saving xml error! %s" % e, fg='red')
