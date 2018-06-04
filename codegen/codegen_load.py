#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
把EXCEL文件转成代码的模块信息字典
"""

import sys

from common import datecm
from common import logcm
from common import xlscm
from common import loadcfgcm
from codegen.codegen_mdl import Module, Service, Bean, Code

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
                    "模块ID" : "moduleName", 
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
        },
        "sub_items" : {
            "start_col" : "F",
            "end_col" : "L",
            "group_keys" : ["req", "resp"],
            "title_map" : {
                "参数ID" : "id",
                "参数名" : "name", 
                "类型" : "type",
                "开始版本" : "startVersion",
                "默认值" : "defaultVal",                
                "说明" : "desc"
            }
        }
    },
    "Beans" : {
        "start_key" : "BEANS",
        "end_type" : "SORT-NO",
        "title_group" : {
            "Bean" : {
                "start_col" : "A",
                "end_col" : "E",
                "title_map" : {
                    "编号" : "sortNo",
                    "Bean名称" : "name", 
                    "开始版本" : "startVersion",
                    "Bean说明" : "desc",
                    "Bean英文名" : "className"                
                }
            }
        },
        "sub_items" : {
            "start_col" : "F",
            "end_col" : "L",
            "group_keys" : ["prop"],
            "title_map" : {
                "属性ID" : "id",
                "属性名" : "name", 
                "类型" : "type",
                "开始版本" : "startVersion",
                "默认值" : "defaultVal",                
                "说明" : "desc"
            }
        }
    },
    "Codes" : {
        "start_key" : "CODES",
        "end_type" : "SORT-NO",
        "title_group" : {
            "Code" : {
                "start_col" : "A",
                "end_col" : "E",
                "title_map" : {
                    "编号" : "sortNo",
                    "Code名称" : "name", 
                    "开始版本" : "startVersion",
                    "Code说明" : "desc",
                    "Code英文名" : "key"                
                }
            }
        },
        "sub_items" : {
            "start_col" : "F",
            "end_col" : "L",
            "group_keys" : ["option"],
            "title_map" : {
                "选项KEY" : "key",
                "选项名称" : "name", 
                "选项CD" : "code",
                "开始版本" : "startVersion",                                
                "说明" : "desc"
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
        mdl = Module(**mdl_info)

        # 加载接口信息
        cfg_svc = self.cfg_xls['Services']
        svc_list = xlscm.load_excel_dict(xls_path, sheet_name, **cfg_svc)
        for svc in svc_list:
            mdl.services.append(Service(svc))

        # 加载Bean信息
        cfg_bean = self.cfg_xls['Beans']
        bean_list = xlscm.load_excel_dict(xls_path, sheet_name, **cfg_bean)
        for bean in bean_list:
            mdl.beans.append(Bean(bean))

        # 加载Code信息
        cfg_code = self.cfg_xls['Codes']
        code_list = xlscm.load_excel_dict(xls_path, sheet_name, **cfg_code)
        for code in code_list:
            mdl.codes.append(Code(code))

        logcm.print_obj(mdl, "mdl")

        return mdl


if __name__ == '__main__':
    loader = CodeGenXlsLoader()
    loader.xls_to_module("./input/xxxxx接口明细v1.0.xlsx", "某个模块")
