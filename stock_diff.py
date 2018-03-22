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

import tushare as ts
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import logcm

from pandas import DataFrame, Series

# 取得K线数据
df = ts.get_k_data('000001','2015-01-01','2016-12-31')
logcm.print_obj(df, 'df')

# 截取：收盘
df1 = DataFrame(df, columns=['close'])
logcm.print_obj(df1, 'df1')

# 插入前1天差分列
df1.insert(1, 'diff_1', df.close.copy().diff(1).tolist())
# 插入前2天差分列
df1.insert(2, 'diff_2', df.close.copy().diff(2).tolist())
# 插入31天差分列
df1.insert(3, 'diff_31', df.close.copy().diff(31).tolist())

# 自然对数
df1.insert(4, 'close_log', np.log(df.close.copy()).tolist())
# 插入前一天差分列(自然对数)
df1.insert(5, 'diff_log_1', df1.close_log.copy().diff(1).tolist())
# 插入31天差分列(自然对数)
df1.insert(6, 'diff_log_31', df1.close_log.copy().diff(31).tolist())

# 排除31天前的数据
df1 = df1[31:]

# 显示最新的矩阵
logcm.print_obj(df1, 'df1')

# 多子图绘制
fig, axes = plt.subplots(2, 2, figsize=(15, 7), sharey=True, sharex=True)
# 设置图片尺寸
fig.set_size_inches(10, 6)
# 总标题
fig.suptitle(u'残差的ACF和PACF图')
# 设置标题(中文字体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 残差的ACF和PACF图
sm.graphics.tsa.plot_acf(df1.diff_31, ax=axes[0][0])
sm.graphics.tsa.plot_pacf(df1.diff_31, ax=axes[0][1])

# 残差的ACF和PACF图(自然对数)
sm.graphics.tsa.plot_acf(df1.diff_log_31, ax=axes[1][0])
sm.graphics.tsa.plot_pacf(df1.diff_log_31, ax=axes[1][1])

# 保存图片
plt.savefig('images/stock_diff_result.jpg')
# 显示绘制后的图片
plt.show()