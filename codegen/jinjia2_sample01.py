#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Jinjia2 使用示例。
"""

from jinja2 import Template
from common import filecm
from codegen.codegen_mdl import Module

mdl = Module("aaa", "bbb", "ccc")

tpl_str = filecm.read_str(file_name="./template/sample_01.tpl")
out_str = Template(tpl_str, trim_blocks=True).render(config=[1, 2, 3], module=mdl)
filecm.save_str(out_str, file_name="./output/sample_01.txt")
#print(out_str)
