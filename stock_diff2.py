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
import numpy as np
import tushare as ts

from common import statcm
from common import logcm

# 取得K线数据
df = ts.get_k_data('000001', '2015-01-01', '2016-12-31')
logcm.print_obj(df, 'df')

# 设置差分天数列表
days_list = np.arange(1, 120, 1).tolist()
logcm.print_obj(days_list, 'days_list')

# 多子图绘制
fig, axes = plt.subplots(2, 1, figsize=(15, 7), sharex=True, sharey=True)
# 设置图片尺寸
fig.set_size_inches(10, 6)
# 总标题
fig.suptitle('股票差分天数和P值的关系')
# 设置标题(中文字体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 计算差分及对数差分的P值
pv_list = []
pv_log_list = []
for row in range(len(days_list)):
    diff_days = days_list[row]
    pv_list.append(statcm.adf_test(df.close.copy(), diff_days))
    pv_log_list.append(statcm.adf_test(df.close.copy(), diff_days, use_log=True))
logcm.print_obj(pv_list, 'pv_list')
logcm.print_obj(pv_log_list, 'pv_log_list')

# 标准线
MAX_P_OK = 0.05
line_list = np.repeat(MAX_P_OK, len(days_list))
# 上图
axes[0].plot(days_list, pv_list)
axes[0].plot(days_list, line_list, '--')
axes[0].fill_between(days_list, pv_list, MAX_P_OK, where=pv_list <= line_list, facecolors='g')
axes[0].set_ylabel('差分P值')

axes[1].plot(days_list, pv_log_list)
axes[1].plot(days_list, line_list, '--')
axes[1].fill_between(days_list, pv_log_list, MAX_P_OK, where=pv_log_list <= line_list, facecolors='g')
axes[1].set_ylabel('对数差分P值')

# 设置XY轴标题
plt.xlabel('差分天数')
# 保存图片
plt.savefig('images/stock_diff2_result.jpg')
# 显示绘制后的图片
plt.show()
