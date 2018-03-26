#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Words common api
Words相关共通函数
"""

import jieba
import jieba.analyse

from common import filecm


def load_stopwords(path, file_name, encoding):
    """
    从指定路径加载停用词列表。
    @param path: 指定的文件路径
    @param file_name: 指定的文件名
    @param encoding: 编码
    @:return 停用词列表
    """
    stopwords = filecm.read_lines(path, file_name, encoding)
    return stopwords


def seg_sentence(sentence, stopwords):
    """
    对指定句子，按照指定停用词进行分词
    @param sentence: 指定句子
    @param stopwords: 停用词列表
    @:return 处理后的DF数据集
    """
    sentence_cut = jieba.cut(sentence.strip())
    seg_list = []
    for word in sentence_cut:
        # 排除停用词
        if word not in stopwords:
            if word != '\t':
                seg_list.append(word)
    # 返回停用词以外的分词
    return ' '.join(seg_list)
