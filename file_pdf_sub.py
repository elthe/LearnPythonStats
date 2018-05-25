#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PDF 文件读取示例
"""

from common import logcm
from common import loadcfgcm

import PyPDF2 as pdf

default_config = """
{    
    "input_path": "/path/to/your/pdf/file",
    "output_path": "/path/to/your/new/pdf/file",
    "sub_pages": [0, 2, 4]        
}
"""

# 加载配置文件
cfg = loadcfgcm.load("file_pdf_sub.json", default_config)

# PDF读取
reader = pdf.PdfFileReader(cfg["input_path"])
logcm.print_obj(reader.getNumPages(), "pages")

pdf_page_list = list()
for i in cfg["sub_pages"]:
    # page number starts with 0
    page = reader.getPage(i - 1)
    pdf_page_list.append(page)
logcm.print_obj(pdf_page_list, "pdf_page_list")

# PDF输出
writer = pdf.PdfFileWriter()
for page in pdf_page_list:
    writer.addPage(page)
with open(cfg["output_path"], 'wb+') as fh:
    writer.write(fh)
