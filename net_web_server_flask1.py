#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Flask WebServer使用示例。
"""

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0')
