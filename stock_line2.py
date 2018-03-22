#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
获取指定股票代码，指定期间的K线数据
"""

import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import datetime
from matplotlib.pylab import date2num
import logcm

df = ts.get_k_data('000001', '2015-01-01', '2015-03-31')
logcm.print_obj(df, 'df')

# 对tushare获取到的数据转换成candlestick_ohlc()方法可读取的格式
def date_to_num(dates):
    num_time = []
    for date in dates:
        # 日期字符串转日期对象
        date_time = datetime.datetime.strptime(date, '%Y-%m-%d')
        # 日期对象转数字
        num_date = date2num(date_time)
        num_time.append(num_date)
    return num_time


# dataframe转换为二维数组
mat = df.as_matrix()
num_time = date_to_num(mat[:, 0])
mat[:, 0] = num_time
logcm.print_obj(mat, 'mat')

# 接下来可以绘制K线图了
# 多子图绘制
fig, axes = plt.subplots(2, 1, figsize=(15, 7), sharey=False, sharex=True)
# 设置图片尺寸
fig.set_size_inches(10, 6)
# 总标题
fig.suptitle(u'股票价格成交量K线图')
# 设置标题(中文字体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# 设置日期刻度旋转的角度
plt.xticks(rotation=30)

# 绘制K线的蜡烛图
mpf.candlestick_ochl(axes[0], mat, width=0.8, colorup='r', colordown='g', alpha=1.0)
# x轴的刻度为日期（把数字显示为日期）
axes[0].xaxis_date()
# Y轴标签
axes[0].set_ylabel('Price')
# 显示网格
axes[0].grid(True)

# 绘制条形图
logcm.print_obj(mat[:, 0], 'mat[:, 0]')
logcm.print_obj(mat[:, 5], 'mat[:, 5]')
axes[1].bar(mat[:, 0], mat[:, 5], width=0.8)
# Y轴标签
axes[1].set_ylabel('Volume')
# 显示网格
axes[1].grid(True)

# 保存图片
plt.savefig('images/stock_line2_result.jpg')
# 显示绘制后的图片
plt.show()
