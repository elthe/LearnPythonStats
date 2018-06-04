#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
把EXCEL文件转成代码的使用示例
"""

from common import loadcfgcm
from codegen.codegen_load import CodeGenXlsLoader
from codegen.codegen_mk import CodeGenModuleMaker

# 配置
default_config = """
{
    "xls_path": "./input/xxxxx接口明细v1.0.xlsx",
    "sheet_name": "某个模块",
    "tpl_path": "./template/xls_to_interface",
    "out_path": "./output"
}
"""

if __name__ == '__main__':
    # 加载配置文件
    cfg = loadcfgcm.load("codegen_maker_run.json", default_config)

    loader = CodeGenXlsLoader()
    mdl = loader.xls_to_module(cfg["xls_path"], cfg["sheet_name"])
    maker = CodeGenModuleMaker(cfg["tpl_path"], cfg["out_path"])
    maker.make(mdl)
