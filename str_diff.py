#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
字符串对比示例
"""

from common import loadcfgcm
from common import logcm
from common import diffcm

import difflib

text1 = """
text1:
This module provides classes and functions for comparing sequences.
including HTML and context and unified diffs.
difflib Document v7.411
add string
kk
pp
"""

text1_lines = text1.splitlines()

text2 = """
text2:
This module provides classes and functions for Comparing sequences.
including HTML and context and unified diffs.
difflib document v7.522
kk
add2
pp
"""

text2_lines = text2.splitlines()

diffcm.diff_by_lines(text1_lines, text2_lines)
