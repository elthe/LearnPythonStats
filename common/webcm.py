# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
web common api
WEB连接相关共通函数
"""

import os
import pycurl
import random
import urllib

from common import filecm
from common import htmlcm
from common import logcm
from common import urlcm
from urllib import request


def random_agent():
    # agent列表
    agent_list = [
        # Firefox
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        # Safari
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
        # Chrome
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
        # IE
        "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)",
    ]
    # 随机返回一个
    index = random.randint(0, len(agent_list))
    return agent_list[index]


def read_url(page_url, encoding):
    """
    通过URL得到网页内容
    @param page_url: 请求的网页地址
    @param encoding: 网页编码
    @return: 网页文本
    """

    headers = {'User-Agent': random_agent()}
    req = urllib.request.Request(url=page_url, headers=headers)
    logcm.print_obj(req, 'req')

    response = urllib.request.urlopen(req)
    logcm.print_obj(response, 'response')

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

    logcm.print_info("Saved url as file. %s --> %s/%s" % (file_url, local_path, file_name))
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

    logcm.print_info("Saved url as html. %s --> %s/%s" % (page_url, local_path, file_name))
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
    logcm.print_info("Page.%d find %d images." % (page_no, len(src_list)))

    count = 0
    for img_src in src_list:
        # 从链接取得文件名
        file_path = urlcm.file_path(img_src)
        file_name = urlcm.file_name(img_src)
        logcm.print_info("Page.%d No.%d %s/%s" % (page_no, count + 1, file_path, file_name))

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


def curl(url, tmp_path, tmp_file='content.txt'):
    """
    访问指定URL，并生成临时文件
    @param url: 网页URL
    @param tmp_path: 临时路径
    @param tmp_file: 临时文件名
    @return:临时文件路径
    """
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)

    # 连接超时时间,5秒
    c.setopt(pycurl.CONNECTTIMEOUT, 5)

    # 下载超时时间,5秒
    c.setopt(pycurl.TIMEOUT, 5)
    c.setopt(pycurl.FORBID_REUSE, 1)
    c.setopt(pycurl.MAXREDIRS, 1)
    c.setopt(pycurl.NOPROGRESS, 1)
    c.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)
    # 临时文件
    file_path = os.path.join(tmp_path, tmp_file)
    file_save = open(file_path, "wb")
    c.setopt(pycurl.WRITEHEADER, file_save)
    c.setopt(pycurl.WRITEDATA, file_save)

    try:
        c.perform()
    except BaseException as err:
        logcm.print_info("Exception:%s" % str(err))
        file_save.close()
        c.close()
        return None

    result = {}
    result["NAMELOOKUP_TIME"] = c.getinfo(c.NAMELOOKUP_TIME)
    result["CONNECT_TIME"] = c.getinfo(c.CONNECT_TIME)
    result["PRETRANSFER_TIME"] = c.getinfo(c.PRETRANSFER_TIME)
    result["STARTTRANSFER_TIME"] = c.getinfo(c.STARTTRANSFER_TIME)
    result["TOTAL_TIME"] = c.getinfo(c.TOTAL_TIME)
    result["HTTP_CODE"] = c.getinfo(c.HTTP_CODE)
    result["SIZE_DOWNLOAD"] = c.getinfo(c.SIZE_DOWNLOAD)
    result["HEADER_SIZE"] = c.getinfo(c.HEADER_SIZE)
    result["SPEED_DOWNLOAD"] = c.getinfo(c.SPEED_DOWNLOAD)

    print()
    print("-" * 100)
    print("curl %s --> %s" % (url, file_path))
    print("HTTP状态码：%s" % (result["HTTP_CODE"]))
    print("DNS解析时间：%.2f ms" % (result["NAMELOOKUP_TIME"] * 1000))
    print("建立连接时间：%.2f ms" % (result["CONNECT_TIME"] * 1000))
    print("准备传输时间：%.2f ms" % (result["PRETRANSFER_TIME"] * 1000))
    print("传输开始时间：%.2f ms" % (result["STARTTRANSFER_TIME"] * 1000))
    print("传输结束总时间：%.2f ms" % (result["TOTAL_TIME"] * 1000))
    print("下载数据包大小：%d KB/s" % (result["SIZE_DOWNLOAD"] // 1024))
    print("HTTP头部大小：%d byte" % (result["HEADER_SIZE"]))
    print("平均下载速度：%d KB/s" % (result["SPEED_DOWNLOAD"] // 1024))

    print("-" * 100)

    file_save.close()
    c.close()
    return result
