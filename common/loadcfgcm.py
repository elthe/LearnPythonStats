# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Config Load Common
Config用数据加载共通
"""

import json

from common import logcm
from common import filecm


def load(config_name, default_config, config_path='./config', encoding='utf-8'):
    """
    从指定路径读取配置，如果配置文件不存在，则使用缺省配置
    并保存缺省配置到指定路径。
    @param config_name: 配置文件名
    @param default_config: 缺省配置
    @param config_path: 配置路径
    @param encoding: 文字编码
    @return: 配置信息
    """

    if filecm.exists(config_path, config_name):
        # 文件存在，读取文件
        return load_cfg_file(config_path, config_name, encoding)

    # 文件不存在，返回默认值并初始化配置文件。
    logcm.print_info('配置文件不存在：%s/%s' % (config_path, config_name))

    # 保存默认配置
    save_cfg_file(default_config, config_name, config_path, encoding=encoding)

    # 重新读取文件
    return load_cfg_file(config_path, config_name, encoding)


def load_cfg_file(config_path, config_name, encoding='utf-8'):
    """
    加载配置文件
    :param config_path: 配置路径
    :param config_name: 配置文件名
    :param encoding: 文字编码
    :return:
    """
    # 文件存在，读取文件
    logcm.print_info('配置文件存在：%s/%s' % (config_path, config_name))
    cfg_content = filecm.read_str(config_path, config_name, encoding)
    cfg_info = json.loads(cfg_content)
    return cfg_info


def save_cfg_file(config_info, config_name, config_path='./config', encoding='utf-8'):
    """
    保存配置信息
    :param config_info:配置数据字典或JSON文本
    :param config_name: 配置文件名
    :param config_path: 配置路径
    :param encoding: 文字编码
    :return:
    """
    # 把对象转成JSON字符串，并格式化
    if type(config_info) == type(""):
        # 如果本身就是字符串直接使用
        cfg_content = config_info.strip()
    else:
        cfg_content = json.dumps(config_info, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    # 保存到json文件
    filecm.save_str(cfg_content, encoding, config_path, config_name)
