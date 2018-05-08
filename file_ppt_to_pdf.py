#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PPT文件转PDF文件 示例

"""

import comtypes.client
import os

def init_powerpoint():
    powerpoint=comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible=1
    return powerpoint

def ppt_to_pdf(powerpoint,inputFileName,outputFileName,formatType=32):
    if outputFileName[-3:] != 'pdf':
        outputFileName=outputFileName+'.pdf'
    deck=powerpoint.Presentations.Open(inputFileName)
    deck.SaveAs(outputFileName,formatType)
    deck.Close()
def convert_files_folder(powerpoint,folder):
    files=os.listdir(folder)
    pptfiles=[f for f in files if f.endswith((".ppt",".pptx"))]
    for pptfile in pptfiles:
        fullpath=os.path.join(folder,pptfile)
        ppt_to_pdf(powerpoint,fullpath,fullpath)

if __name__ == '__main__':
    powerpoint=init_powerpoint()
    cwd=os.getcwd()
    convert_files_folder(powerpoint,"./temp")
    powerpoint.Quit()
