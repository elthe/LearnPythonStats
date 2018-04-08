#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
平稳性检验判断
ACF  ：自相关函数
PACF ：偏自相关系数
判断方法
--- 平稳的时间序列表现出一种围绕其均值不断波动的过程。
--- 非平稳的时间序列表现出在不同时间段有不同的均值（持续上升或下降）
"""


import matplotlib.pyplot as plt

from common import loadtscm
from common import logcm
from common import statcm

# 取得K线数据
df = loadtscm.get_k_data('000001', '2015-01-01', '2016-12-31')
logcm.print_obj(df, 'df')

# 设置差分天数列表
days_list = [1, 2, 3, 4, 5, 6, 7, 10, 15, 21, 25, 30, 31, 40, 50, 60, 100, 150, 200, 250, 300]

# 多子图绘制
fig, axes = plt.subplots(len(days_list), 4, sharey=False, sharex=False)
# 设置图片尺寸
fig.set_size_inches(12, 3 * len(days_list))
# 总标题
fig.suptitle('')
# 设置标题(中文字体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

for row in range(len(days_list)):
    diff_days = days_list[row]
    # 差值ACF图-显示P值
    statcm.plot_acf(axes[row][0], df.close.copy(), diff_days, show_p=True)
    # 差值PACF图
    statcm.plot_acf(axes[row][1], df.close.copy(), diff_days, plt_pacf=True)
    # 对数差值ACF图-显示P值
    statcm.plot_acf(axes[row][2], df.close.copy(), diff_days, use_log=True, show_p=True)
    # 对数差值PACF图
    statcm.plot_acf(axes[row][3], df.close.copy(), diff_days, use_log=True, plt_pacf=True)

# 调整每隔子图之间的距离
plt.tight_layout()
# 保存图片
plt.savefig('images/stock_diff1_result.jpg')
# 显示绘制后的图片
plt.show()
