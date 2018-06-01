#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
把EXCEL报送文件转成XML转化器类及配置
"""

import sys

from common import logcm
from common import datecm
from common import xmlcm
from common import filecm
from common import xlscm
from common import loadcfgcm
from common import checkcm
from common.checkcm import CheckRule

from cncrs.cncrs_mk import CNCRSReportMaker
from cncrs.cncrs_tag import *

# 配置
default_config = """
{
    "Module" : {
        "start_key" : "MODULE",
        "title_group" : {
            "Module" : {
                "start_col" : "A",
                "end_col" : "F",
                "title_map" : {
                    "包路径" : "packageName",
                    "模块ID" : "moduleId", 
                    "模块描述" : "moduleDesc"
                }
            }
        }
    },
    "Services" : {
        "start_key" : "SERVICES",
        "end_type" : "SORT-NO",
        "title_group" : {
            "Service" : {
                "start_col" : "A",
                "end_col" : "E",
                "title_map" : {
                    "编号" : "sortNo",
                    "允许身份" : "role", 
                    "开始版本" : "startVersion",
                    "接口说明" : "desc",
                    "接口英文名" : "interfaceName"                
                }
            }
        }
    }
}
"""


class CodeGenXlsLoader:
    """
    代码生成-Excel设计文档加载类
    """

    def __init__(self):
        # 加载配置文件
        self.cfg_xls = loadcfgcm.load("codegen_loader_xls.json", default_config)

    def xls_to_module(self, xls_path, sheet_name):
        """
        按照配置读取指定Exel,指定Sheet名,载入模块数据
        :param xls_path: Excel文件路径
        :param sheet_name: Sheet名
        :return:模块数据字典对象
        """
        logcm.print_info("Loading xls : %s ..." % xls_path)
        # 加载Excel模块信息
        cfg_mdl = self.cfg_xls['Module']
        mdl_list = xlscm.load_excel_dict(xls_path, sheet_name, **cfg_mdl)
        # 模块信息为空判断
        if mdl_list is None or len(mdl_list) == 0:
            logcm.print_info("Module Info is not set!", fg='red')
            sys.exit()
        if len(mdl_list) != 1:
            logcm.print_info("Module Info need only one!", fg='red')
            sys.exit()
        mdl_info = mdl_list[0]["Module"]
        logcm.print_obj(mdl_info, "mdl_info", show_json=True, show_table=True)

        # 加载Excel接口信息
        cfg_mdl = self.cfg_xls['Services']
        svc_list = xlscm.load_excel_dict(xls_path, sheet_name, **cfg_mdl)
        logcm.print_obj(svc_list, "svc_list", show_json=True, show_table=True)

        return mdl_info


loader = CodeGenXlsLoader()
loader.xls_to_module("./input/xxxxx接口明细v1.0.xlsx", "某个模块")
