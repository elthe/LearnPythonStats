# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Crawl common api
网络爬虫相关共通函数
"""

from common import htmlcm
from common import logcm
from common import webcm


def crawl_from_url(page_url, next_page_select,
                   img_select, tag_select, local_path, encoding='utf-8', page_no=1):
    """
    从指定的网页URL，取得满足要求的图片URL列表
    @param page_url: 网页URL
    @param next_page_select: 下一页select语句
    @param img_select: 图片select语句
    @param tag_select: 标签select语句
    @param local_path: 本地文件保存路径
    @param encoding: 网页编码
    @param page_no: 网页页码号
    @return: 无
    """
    logcm.print_info("crawl_from_url Page.%d start..." % page_no)
    html = webcm.read_url(page_url, encoding)
    # print(html)
    soup = htmlcm.to_soup(html)
    # 下载当前网页中的所有图片
    webcm.down_img(soup, page_url, img_select, tag_select, local_path, page_no)
    # 取得下一个页面的URL地址
    next_page_url = htmlcm.next_page(soup, page_url, next_page_select)
    # 只要下一个页面存在，继续递归下载
    if next_page_url is not None:
        logcm.print_info("NextPageUrl is " + next_page_url)
        crawl_from_url(next_page_url, next_page_select,
                       img_select, tag_select, local_path, encoding, page_no + 1)
    else:
        logcm.print_info("End\n")


def crawl_with_format(page_url, next_page_format,
                      img_select, tag_select, local_path, encoding='utf-8', page_no=1):
    """
    从指定的网页URL，取得满足要求的图片URL列表
    @param page_url: 网页URL
    @param next_page_format: 下一页连接的模板
    @param img_select: 图片select语句
    @param tag_select: 标签select语句
    @param local_path: 本地文件保存路径
    @param encoding: 网页编码
    @param page_no: 网页页码号
    @return: 无
    """
    logcm.print_info("......crawl_with_format Page." + str(page_no) + "......")
    html = webcm.read_url(page_url, encoding)
    # print(html)
    soup = htmlcm.to_soup(html)
    # 下载当前网页中的所有图片
    count = webcm.down_img(soup, page_url, img_select,
                           tag_select, local_path, page_no)
    if count == 0:
        # 如果下载不到文件，或者是已存在的文件，则结束下载。
        logcm.print_info("Not found image End\n")
        return

    # 取得下一个页面的URL地址
    next_page_url = next_page_format.replace('[page_no]', str(page_no + 1))
    logcm.print_info("NextPageUrl is " + next_page_url)
    crawl_with_format(next_page_url, next_page_format,
                      img_select, tag_select, local_path, encoding, page_no + 1, )
