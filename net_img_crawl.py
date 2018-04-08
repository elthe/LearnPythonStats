#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
网络图片下载
"""

from common import crawlcm
from common import loadcfgcm

# 缺省配置及说明
default_config = {
    # 链接模式：SELECT 从选定页面开始，根据下一页按钮，循环抓取
    # 链接模式：FORMAT 按照格式，根据格式生成下一页链接，循环抓取
    'link_mode': 'SELECT',
    # 下载的首页
    'page_url': 'http://www.somesite.to.crawl/xxxx',
    # 网页HTML编码
    'encoding': 'utf-8',
    # 下一页链接的Soup路径
    'next_page_select': 'div.page a.next',
    # 格式化翻页时，由开始页面和页号组合成的模版，链接模式为FORMAT时必须
    'next_page_format': '[linkUrl]/[pageNo]',
    # 网页中要下载的图片的Soup路径
    'img_select': 'div.article div.content a img',
    # 网页中要获取的标签的Soup路径（标签会作为保存目录名使用）
    'tag_select': 'div.other div.tags a',
    # 抓取图片的保存路径
    'local_path': './temp',
}

# 加载配置文件
cfg = loadcfgcm.load("net_img_crawl.json", default_config)

if cfg['link_mode'] == 'SELECT':
    crawlcm.crawl_from_url(cfg['page_url'], cfg['next_page_select'],
                           cfg['img_select'], cfg['tag_select'], cfg['local_path'])

elif cfg['link_mode'] == 'FORMAT':
    crawlcm.crawl_with_format(cfg['page_url'], cfg['next_page_format'],
                              cfg['img_select'], cfg['tag_select'], cfg['local_path'])
