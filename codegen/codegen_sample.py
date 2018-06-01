#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
把EXCEL文件转成代码的使用示例
"""

from codegen.codegen_load import CodeGenXlsLoader
from codegen.codegen_mk import CodeGenModuleMaker

if __name__ == '__main__':
    loader = CodeGenXlsLoader()
    mdl = loader.xls_to_module("./input/xxxxx接口明细v1.0.xlsx", "某个模块")
    tpl_path = "./template/xls_to_interface"
    out_path = "./output"
    maker = CodeGenModuleMaker(tpl_path, out_path)
    maker.make(mdl)
