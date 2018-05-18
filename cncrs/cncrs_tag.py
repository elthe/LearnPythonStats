#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CNCRS XML标签定义
"""

from common import logcm
from common import xmlcm
from common.xmlcm import XmlTag


class CNCRSReport(XmlTag):
    """
    CNCRS标签
    """

    def __init__(self):
        """
        标签初始化
        @return: 无
        """
        init_param = {
            'prefix': "cncrs",
            'attr': {'version': "1.0"},
            'xmlns': {
                'stc': "http://aeoi.chinatax.gov.cn/crs/stctypes/v1",
                'cncrs': "http://aeoi.chinatax.gov.cn/crs/cncrs/v1"
            }
        }
        super(CNCRSReport, self).__init__("CNCRS", **init_param)



report = CNCRSReport()
logcm.print_obj(report.to_dict(), "report")