# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
web common api
WEB连接相关共通函数
"""

from common import filecm
from common import urlcm
from common import htmlcm
import urllib
from urllib import request


def read_url(page_url, encoding):
    """
    通过URL得到网页内容
    @param page_url: 请求的网页地址
    @param encoding: 网页编码
    @return: 网页文本
    """

    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    req = urllib.request.Request(url=page_url, headers=headers)
    response = urllib.request.urlopen(req)
    html = response.read().decode(encoding, 'ignore')
    return html


def read_file(path, file_name, encoding):
    """
    通过本地文件得到网页内容
    @param path: 文件路径
    @param file_name: 文件名
    @param encoding: 网页编码
    @return: 网页文本
    """

    # 从本地HTML文件读取文本
    html = filecm.read_str(path, file_name, encoding)
    return html


def response_file(file_url, ref_url):
    """
    根据文件URL取得Response对象
    @param file_url: 文件URL
    @param ref_url: 来源网页URL
    @return:Response对象
    """

    # 防盗链，修改访问来源
    headers = ('Referer', ref_url)
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    # 模拟网页打开文件
    response = opener.open(file_url)
    return response


def save_file_url(file_url, ref_url, local_path, file_name):
    """
    把文件URL保存到本地文件
    @param file_url: 文件URL
    @param ref_url: 来源网页URL
    @param local_path: 文件路径
    @param file_name: 文件名
    @return:无
    """

    # 取得文件Response对象
    response = response_file(file_url, ref_url)
    # 把数据保存到本地文件
    filecm.save_data(response.read(), local_path, file_name)


def save_html_url(page_url, encoding, local_path, file_name):
    """
    把网页URL保存到本地HTML文件
    @param page_url: 网页URL
    @param encoding: 网页编码
    @param local_path: 文件路径
    @param file_name: 文件名
    @return:无
    """

    # 读取HTML内容到文本
    html = read_url(page_url, encoding)
    # 保存HTML内容到本地文件
    filecm.save_str(html, encoding, local_path, file_name)


def down_img(soup, page_url, img_select, tag_select, local_path, page_no=1):
    """
    从指定的网页URL，下载所有满足要求的图片到本地
    @param soup: 网页Soup对象
    @param page_url: 网页URL
    @param img_select: 图片select语句
    @param tag_select: 标签select语句
    @param local_path: 本地文件保存路径
    @param page_no: 网页页码号
    @return:下载到的图片数量
    """

    src_list = htmlcm.img_src_list(soup, page_url, img_select)
    print("Page." + str(page_no) + " find " + str(len(src_list)) + " images.")
    count = 0
    for img_src in src_list:
        # 从链接取得文件名
        file_path = urlcm.file_path(img_src)
        file_name = urlcm.file_name(img_src)
        print("Page." + str(page_no) + " No." + str(count + 1) + " " + file_path + "/" + file_name)
        names = htmlcm.tag_name_list(soup, tag_select)
        if len(names) > 0:
            local_save_path = local_path + "/" + "_".join(names)
        else:
            local_save_path = local_path + "/" + file_path

        if not filecm.exists(local_save_path, file_name):
            # 如果本地不存在，保存文件到本地        
            save_file_url(img_src, page_url, local_save_path, file_name)
            count = count + 1
    return count
