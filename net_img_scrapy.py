#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
网络图片下载
"""

from common import crawlcm

# 开始地址
page_url = 'http://findicons.com/search/schedule/2'
encoding = 'utf-8'
next_page_select = 'ul.pull-right li [aria-label="Next"]'
img_select = 'div.icon_list li.items a.iconenter img'
tag_select = 'div.main-tags a[rel="tag"]'
local_path = './temp'

crawlcm.crawl_from_url(page_url, next_page_select, img_select, tag_select, local_path)
