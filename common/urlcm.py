# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
URL common api
URL相关共通函数
"""


def base_url(url):
    """
    通过URL得到基础URL（到URL最后一级目录）
    @param url: 请求URL
    @return: 基础URL
    """

    end_pos = url.rfind('/')
    base = url[0:end_pos]
    return base


def root_url(url):
    """
    通过URL得到服务器URL
    @param url: 请求URL
    @return: 服务器URL
    """

    end_pos = url.find('/', 8)
    root = url[0:end_pos]
    return root


def file_name(url):
    """
    通过URL得到文件名
    @param url: 请求URL
    @return: 文件名
    """

    end_pos = url.rfind('/')
    name = url[end_pos + 1:len(url)]
    return name


def file_path(url):
    """
    通过URL得到文件路径
    @param url: 请求URL
    @return: 文件路径
    """

    end_pos = url.rfind('/')
    start_pos = url.find('/', 8)
    path = url[start_pos:end_pos]
    return path


def link_url(page_url, link_path):
    """
    通过URL和文件路径得到链接URL
    @param page_url: 请求URL
    @param link_path: 连接路径
    @return: 链接URL
    """

    if link_path.startswith('http'):
        return link_path
    if link_path.startswith('/'):
        root = root_url(page_url)
        link = root + "/" + link_path
    else:
        base = base_url(page_url)
        link = base + "/" + link_path
    return link
