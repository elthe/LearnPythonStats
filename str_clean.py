#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
字符串对比示例
"""
import re

from common import diffcm
from common import filecm
from common import strcm


#
REPLACE_KEYS = [
    r'[a-zA-Z\.-]*mianhuatang[a-zA-Z\.-]*',
    r'[a-zA-Z\.-]*qiushu[a-zA-Z\.-]*',
    r'[a-zA-Z\.-]*80txt[a-zA-Z\.-]*',
    r'[a-zA-Z\.-]*[^\n]{0,2}wxs520[a-zA-Z\.-]*',

    r'<strong>[^<>]+</strong>',
    r'<a [^<>]+>[^<>]+</a>',
    r'<!--[^<>]+-->',

    r'\[[^\[\n]*小说网[^\]\n]*\]',
    r'\[[^\[\n]*电子书[^\]\n]*\]',
    r'\[[^\[\n]*更新快[^\]\n]*\]',
    r'\[[^\[\n]*好看小说[^\]\n]*\]',
    r'\[[^\[\n]*全集下载[^\]\n]*\]',
    r'\[[^\[\n]*天火大道[^\]\n]*\]',

    r'（[^\n]*无弹窗广告[^\n]*）',
    r'\([^\(\n]*棉花糖[^\n\)]*\)',
    r'\([^\(\n]*小说网[^\n\)]*\)',
    r'\([^\(\n]*电子书[^\n\)]*\)',
    r'\([^\(\n]*未完待续[^\n\)]*\)',

    r'\([^\(\n]*求[^\(\n]{0,2}书[^\(\n]{0,2}网[^\n\)]*\)',

    r'&#[0-9]+;',
    r'txt[^\n]{0,5}下载',
    r'为[^\n]{0,10}加更',
    r'～[^\n]{0,15}加更',
    r'手机用户请到[^\n]{0,15}阅读。',
    r'[^\n]{0,15}欢迎广大书友光临阅读[^\n]{0,50}',
    r'求月票',
    r'\nps[^\n]+\n',
    r'\n天才一秒记住本站地址[^\n]+\n',
    r'\n手机版阅读网址：[^\n]+\n',
]

str_org = filecm.read_str("./temp", "test.txt", "utf-8")

str_new = str_org
find_cnt = 0
for key in REPLACE_KEYS:
    # 匹配正则，匹配小写字母和大写字母的分界位置
    p = re.compile(key, re.IGNORECASE)

    findList = p.findall(str_new)
    find_cnt += len(findList)
    print("Found %d by key : %s" % (len(findList), key))
    print(findList)

    # 这里第二个参数使用了正则分组的后向引用
    str_new = re.sub(p, r'', str_new)

    filecm.save_str(str_new, path="./temp", file_name="test2.txt")

print("Replace %d String in total!" % find_cnt)