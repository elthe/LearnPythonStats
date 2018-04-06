#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
网络图片下载
"""

from common import crawlcm

# 配置列表
cfg_list = [
    {
        'link_mode': 'SELECT',
        'page_url': 'http://www.mmjpg.com/mm/xxxx',
        'encoding': 'utf-8',
        'next_page_select': 'div.page a.next',
        'img_select': 'div.article div.content a img',
        'tag_select': 'div.other div.tags a',
        'local_path': './temp',
    },
    # {
    #     'link_mode': 'SELECT',
    #     'page_url': 'http://findicons.com/search/schedule/2',
    #     'encoding': 'utf-8',
    #     'next_page_select': 'ul.pull-right li [aria-label="Next"]',
    #     'img_select': 'div.icon_list li.items a.iconenter img',
    #     'tag_select': 'div.main-tags a[rel="tag"]',
    #     'local_path': './temp',
    # },
]

# 配置循环
for cfg in cfg_list:
    if cfg['link_mode'] == 'SELECT':
        crawlcm.crawl_from_url(cfg['page_url'], cfg['next_page_select'],
                               cfg['img_select'], cfg['tag_select'], cfg['local_path'])
    elif cfg['link_mode'] == 'FORMAT':
        crawlcm.crawl_with_format(cfg['page_url'], cfg['next_page_format'],
                                  cfg['img_select'], cfg['tag_select'], cfg['local_path'])
