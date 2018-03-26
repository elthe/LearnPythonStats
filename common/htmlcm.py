# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
HTML common api
HTML相关共通函数
"""

from common import urlcm
from bs4 import BeautifulSoup


def clean_html(html):
    """
    通过URL得到网页内容
    @param html: 请求的网页地址
    @return: 网页文本
    """
    return to_soup(html).text


def to_soup(html):
    """
    把网页内容封装到BeautifulSoup中并返回BeautifulSoup
    @param html: 网页内容
    @return:BeautifulSoup
    """

    if html is None:
        return None
    # 固定编码
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def img_src_list(soup, page_url, img_select):
    """
    从指定的网页URL，取得满足要求的图片URL列表
    @param soup: 网页Soup对象
    @param page_url: 网页URL
    @param img_select: 图片select语句
    @return:
    """

    # 图片路径列表
    src_list = []
    for tag in soup.select(img_select):
        src = tag.attrs['src']
        # 根据相对路径，取得连接URL
        link_url = urlcm.link_url(page_url, src)
        # 加入数组    
        src_list.append(link_url)
    # 返回图片数组
    return src_list


def link_list(soup, page_url, link_select):
    """
    从指定的网页URL，取得满足要求的链接列表
    @param soup: 网页Soup对象
    @param page_url: 网页URL
    @param link_select: 链接select语句
    @return:链接列表
    """

    # 链接列表
    links = []
    for tag in soup.select(link_select):
        href = tag.attrs['href']
        # 根据相对路径，取得连接URL
        link = urlcm.link_url(page_url, href)
        # 加入列表 
        links.append(link)
    # 返回链接列表
    return links


def next_page(soup, page_url, next_page_select):
    """
    从指定的网页URL，取得下一页的网页URL
    @param soup: 网页Soup对象
    @param page_url: 网页URL
    @param next_page_select: 下一页连接select语句
    @return: 下一页网页URL
    """

    # 取得下一个页面的URL地址(如果有多个返回包含关键词的那个)
    tags = soup.select(next_page_select)
    for tag in tags:
        href = tag.attrs['href']
        link_url = urlcm.link_url(page_url, href)
        return link_url
    # 没有找到返回空
    return None


def tag_name_list(soup, tag_select):
    """
    从指定的网页soup，取得满足条件的标签一览
    @param soup: 网页Soup对象
    @param tag_select: 下一页连接select语句
    @return: 标签一览
    """

    # 选择器
    tags = soup.select(tag_select)
    names = []
    for tag in tags:
        name = tag.string
        names.append(name)
    # 没有找到返回空
    return names
