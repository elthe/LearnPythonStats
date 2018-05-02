#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
网络图片下载
"""

from common import crawlcm
from common import loadcfgcm

# 缺省配置及说明
# 链接模式：SELECT 从选定页面开始，根据下一页按钮，循环抓取
# 链接模式：FORMAT 按照格式，根据格式生成下一页链接，循环抓取
default_config = """
{
    "link_mode": "SELECT",
    "page_url": "http://www.somesite.to.crawl/xxxx",
    "encoding": "utf-8",
    "next_page_select": "div.page a.next",
    "next_page_format": "[linkUrl]/[pageNo]",
    "img_select": "div.article div.content a img",
    "tag_select": "div.other div.tags a",
    "local_path": "./temp",
}
"""

# 加载配置文件
cfg = loadcfgcm.load("net_img_crawl.json", default_config)

if cfg['link_mode'] == 'SELECT':
    crawlcm.crawl_from_url(cfg['page_url'], cfg['next_page_select'],
                           cfg['img_select'], cfg['tag_select'], cfg['local_path'])

elif cfg['link_mode'] == 'FORMAT':
    crawlcm.crawl_with_format(cfg['page_url'], cfg['next_page_format'],
                              cfg['img_select'], cfg['tag_select'], cfg['local_path'])
