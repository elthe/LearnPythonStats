#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Jinjia2 使用示例。
"""

from jinja2 import Template

tpl_str = """
{% for i in config %}
{{i}}
{% endfor %}
"""

out_str = Template(tpl_str, trim_blocks=True).render(config=[1, 2, 3])
print(out_str)
