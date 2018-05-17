# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
XML common api
XML相关共通函数
"""

import xml.dom.minidom as minidom

from lxml import etree
from common import logcm
from common import filecm

# 常量
KEY_TAG = "tag"
KEY_VAL = "value"
KEY_ATTR = "attr"
KEY_PREFIX = "prefix"
KEY_XMLNS = "xmlns"


class XmlTag:
    """
    XML的标签类
    """
    # 标签
    tag = None
    # 前缀
    prefix = None
    # 属性字典
    attr = None
    # 标签内容(文本或标签列表)
    value = None
    # 命名空间字典
    xmlns = None

    def __init__(self, tag, prefix=None, attr=None, value=None, xmlns=None):
        """
        XML标签初始化
        :param tag: 标签名
        :param prefix: 前缀
        :param attr: 属性字典
        :param value: 值
        :param xmlns: 命名空间字典
        """
        self.tag = tag
        self.prefix = prefix
        self.attr = attr
        self.value = value
        self.xmlns = xmlns

    def add_sub_tag(self, sub_tag):
        """
        给当前标签添加子标签
        :param sub_tag: 子标签对象
        :return: 无
        """
        # 子标签列表初始化
        if self.value is None:
            self.value = []
        # 添加子标签
        if sub_tag is not None:
            self.value.append(sub_tag)

    def to_dict(self):
        """
        转换成数据字典
        :return:
        """
        data = {KEY_TAG: self.tag}
        if self.attr:
            data[KEY_ATTR] = self.attr
        if self.prefix:
            data[KEY_PREFIX] = self.prefix
        if self.value:
            if type(self.value) == list:
                # 如果值是列表类型,则把标签列表转成字典列表
                sub_list = []
                for item in self.value:
                    sub_list.append(item.to_dict())
                data[KEY_VAL] = sub_list
            else:
                data[KEY_VAL] = self.value
        if self.xmlns:
            data[KEY_XMLNS] = self.xmlns
        return data


def xml_to_dict(xml_bytes=None, xml_path=None):
    """
    把XML文本或文件转换成字典
    :param xml_bytes: XML文本字节数组
    :param xml_path: XML文件路径
    """
    if xml_path is not None:
        logcm.print_info("Reading xml file : %s" % xml_path)
        xml_bytes = filecm.read_bytes(file_name=xml_path)

    if xml_bytes is None:
        logcm.print_info("xml_bytes is None!", fg='red')
        return None
    root_node = etree.XML(xml_bytes)

    # 取得根节点下字典一览
    root_list = []
    node_to_list(root_node, root_list)
    # 根节点字典做成
    tag_root = get_tag_name(root_node)
    # 节点转字典
    data_root = node_to_dict(root_node, tag_root, root_list)
    # 命名空间
    if root_node.nsmap:
        data_root[KEY_XMLNS] = dict(root_node.nsmap)

    return data_root


def get_tag_name(node):
    """
    取得指定节点的标签名
    :param node: 节点对象(lxml.etree._Element)
    :return: 标签名
    """
    tag = node.tag
    if tag[0] == "{" and tag.index("}") > 0:
        tag = tag[tag.index("}") + 1:]
    return tag


def node_to_dict(node, tag, value):
    """
    把指定节点,以及对应值转换成字典.
    :param node: 节点对象(lxml.etree._Element)
    :param tag: 标签名
    :param value: 当前对应值
    :return:
    """

    # 名称和值
    data = {KEY_VAL: value, KEY_TAG: tag}
    # 属性
    if node.attrib:
        data[KEY_ATTR] = dict(node.attrib)
    # 前缀
    if node.prefix:
        data[KEY_PREFIX] = node.prefix
    return data


def node_to_list(parent_node, parent_list):
    """
    把指定节点下的XML结构,转换成字典放入列表
    :param parent_node: 指定父节点(lxml.etree._Element)
    :param parent_list: 指定列表
    :return: 无
    """
    tag_parent = get_tag_name(parent_node)
    if len(parent_node):
        for sub_Node in list(parent_node):
            tag_sub = get_tag_name(sub_Node)
            sub_list = []
            # 递归处理子节点
            node_to_list(sub_Node, sub_list)

            if len(sub_Node):
                # 子节点字典
                data_sub = node_to_dict(sub_Node, tag_sub, sub_list)
                parent_list.append(data_sub)
            else:
                # 如果子节点为文本
                parent_list.append(sub_list[0])
    else:
        # 父节点字典
        data_parent = node_to_dict(parent_node, tag_parent, parent_node.text.strip())
        parent_list.append(data_parent)
    return


def data_to_xml(data):
    """
    字典转XML(可递归)
    :param data: 字典数据
    :return: XML文本
    """
    # 设置标签
    tag = data[KEY_TAG]
    if KEY_PREFIX in data:
        prefix = data[KEY_PREFIX]
        if prefix:
            tag = "%s:%s" % (prefix, tag)

    # 设置属性字符串
    attr_str = ""
    if KEY_ATTR in data:
        attr = data[KEY_ATTR]
        if attr:
            for (k, v) in attr.items():
                attr_str += ' %s="%s"' % (k, v)

    # 设置命名空间
    if KEY_XMLNS in data:
        xmlns = data[KEY_XMLNS]
        if xmlns:
            for (k, v) in xmlns.items():
                attr_str += ' xmlns:%s="%s"' % (k, v)

    # 设置内容值
    value_str = ""
    if KEY_VAL in data:
        value = data[KEY_VAL]
        if type(value) == list:
            sub_list = []
            for item in value:
                sub_xml = data_to_xml(item)
                sub_list.append(sub_xml)
            value_str = "".join(sub_list)
        else:
            value_str = value

    # 生成XML字符串
    xml = "<%s%s>%s</%s>" % (tag, attr_str, value_str, tag)
    return xml


def dict_to_xml(root_data, save_path=None):
    """
    把dict转换成XML
    @param root_data: 输入根节点字典对象
    @param save_path: 保存路径
    @return: XML的Root对象
    """
    xml_str = '<?xml version="1.0" encoding="utf-8"?>'
    xml_str += data_to_xml(root_data)

    if save_path:
        save_xml(xml_str, save_path)

    return xml_str


def save_xml(xml_str, save_path, encoding="utf-8"):
    """
    格式化root转换为xml文件
    @param xml_str: 根节点
    @param save_path: xml文件
    @param encoding: 文本编码
    @return: 无
    """

    try:
        logcm.print_info("Saving xml file --> %s" % save_path)

        # 解析XML文档
        xml_doc = minidom.parseString(xml_str.encode(encoding))

        # 写入XML文件
        with open(save_path, "w+") as file:
            xml_doc.writexml(file, addindent="\t", newl="\n", encoding=encoding)

    except Exception as e:
        logcm.print_info("Saving xml error! %s" % e, fg='red')
