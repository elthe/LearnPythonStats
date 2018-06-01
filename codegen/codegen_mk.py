#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
把EXCEL文件转成代码的模块信息字典
"""

import os
import sys

from common import logcm
from common import filecm
from common import loadcfgcm
from jinja2 import Template

# 配置
default_config = """
{
    "base_package": "com.xxxx.kkk",
    "base_package_path": "com/xxxx/kkk",
    "base_project": "xxxx-yyyy",
    "base_service_prefix": "Crm",
    "base_controller_prefix": "Crm",    
    "core_base_package": "com.xxxx.crmcore",
    "core_base_package_path": "com/xxxx/kkk",
    "core_base_project": "xxxx-kkk",
    "core_base_service_prefix": "App",    
    "package_sysname": "app",
    "controller_path": "app",
    "author": "somebody",
    "copyrightEN": "Copyright (c) 2017, www.xxxxx.com.cn All Rights Reserved.",
    "copyrightCN": "XXXXXXXXXX版权所有"
}
"""


class CodeGenModuleMaker:
    """
    代码生成-代码生成类
    """

    def __init__(self, tpl_path, out_path):
        """
        初始化
        :param tpl_path: 模版路径
        :param out_path: 生成文件路径
        """
        # 加载配置文件
        self.cfg_mk = loadcfgcm.load("codegen_maker_module.json", default_config)
        # 模版文件根路径
        self.tpl_path = tpl_path
        # 输出文件根路径
        self.out_path = out_path
        # 读取模版配置
        self.cfg_tpl = loadcfgcm.load_cfg_file(self.tpl_path, "tpl_config.json")
        if self.cfg_tpl is None:
            logcm.print_info("Template Config Load Failed!", fg='red')
            sys.exit()

    def make(self, mdl):
        """
        根据指定模块信息,和代码模版目录,生成代码
        :param mdl: 模块
        :return: 无
        """
        logcm.print_info("Making src with %s to %s ..." % (self.tpl_path, self.out_path))
        total_count = 0
        # 使用模块生成代码
        path = self.cfg_tpl["Module"]["tpl_path"]
        path_map = self.cfg_tpl["Module"]["path_map"]
        cfg_obj = {
            "config": self.cfg_mk,
            "module": mdl
        }
        total_count += self.make_by_path(path, path_map, cfg_obj)

        # 使用接口生成代码
        path = self.cfg_tpl["Service"]["tpl_path"]
        path_map = self.cfg_tpl["Service"]["path_map"]
        for svc in mdl.services:
            cfg_obj["service"] = svc
            total_count += self.make_by_path(path, path_map, cfg_obj)

        logcm.print_info("Output %d files successfully. " % total_count)

    def make_by_path(self, path, path_map, cfg_obj):
        """
        按照指定模版目录,和路径Map,进行代码生成
        :param path: 模版目录
        :param path_map: 路径Map
        :param cfg_obj: 配置数据
        :return: 文件生成数
        """
        make_count = 0
        path = os.path.join(self.tpl_path, path)
        tpl_list = filecm.search_files(path, ".tpl")
        for tpl_path in tpl_list:
            out_file_tpl = path_map[filecm.short_name(tpl_path)]
            self.make_by_tpl(tpl_path, out_file_tpl, cfg_obj)
            make_count += 1
        return make_count

    def make_by_tpl(self, tpl_path, out_file_tpl, cfg_obj):
        """
        按照指定模版文件,进行代码生成
        :param tpl_path: 模版文件路径
        :param out_file_tpl: 输出路径模版
        :param cfg_obj: 配置数据
        :return: 无
        """
        # 读入模版
        tpl_str = filecm.read_str(file_name=tpl_path)
        # 生成代码
        out_str = Template(tpl_str, trim_blocks=True).render(**cfg_obj)
        # 生成输出路径
        out_file = Template(out_file_tpl, trim_blocks=True).render(**cfg_obj)
        # 保存到文件
        out_file = os.path.join(self.out_path, out_file)
        filecm.save_str(out_str, file_name=out_file)
