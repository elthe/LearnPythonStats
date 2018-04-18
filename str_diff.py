#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
字符串对比示例
"""

from common import loadcfgcm
from common import logcm

import difflib

text1 = """
text1:
This module provides classes and functions for comparing sequences.
including HTML and context and unified diffs.
difflib document v7.4
add string
"""

text1_lines = text1.splitlines()

text2 = """
text2:
This module provides classes and functions for Comparing sequences.
including HTML and context and unified diffs.
difflib document v7.5

add2
"""

text2_lines = text2.splitlines()

d = difflib.Differ()
diff = d.compare(text1_lines, text2_lines)
diff_list = list(diff)

for i in range(len(diff_list)):
    msg = diff_list[i]
    msg_next = diff_list[i + 1] if i < len(diff_list) - 1 else ""

    if msg.startswith("+"):
        if msg_next.startswith("?"):
            msg += "\n" + msg_next
        logcm.print_obj(msg, "diff-%d" % i, fg='red', show_header=False)

    elif msg.startswith("-"):
        if msg_next.startswith("?"):
            msg += "\n" + msg_next
        logcm.print_obj(msg, "diff-%d" % i, fg='green')

    elif msg.startswith("?"):
        continue
