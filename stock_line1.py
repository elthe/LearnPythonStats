#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 根据Tushare取得股票数据，绘制曲线图。

import tushare as ts
import matplotlib.pyplot as plt
from pandas import DataFrame, Series
import logcm

# 多子图绘制
fig, axes = plt.subplots(2, 1, figsize=(15, 7), sharey=False, sharex=True)
# 设置图片尺寸
fig.set_size_inches(10, 6)
# 总标题
fig.suptitle(u'股票价格成交量变化示例图')
# 设置标题(中文字体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 股票代码
stcd = '000001'
# 股票数据，日期为索引，其他列为数据
df = ts.get_hist_data('000001', start='2015-01-01', end='2016-12-31').sort_index()
# 截取：开盘, 收盘, 最高, 最低
df1 = DataFrame(df, columns=['high', 'low', 'open', 'close'])
logcm.print_obj(df1, 'df1')

# 截取：成交量
df2 = DataFrame(df, columns=['volume'])
logcm.print_obj(df2, 'df2')

# 上图
df1.plot(ax=axes[0], grid=True, title='价格变化')
axes[0].set_ylabel('价格（元）')
# 下图
df2.plot(ax=axes[1], grid=True, title='成交量变化')
axes[1].set_ylabel('成交量')
# X轴：旋转50度
plt.xticks(rotation=30)
plt.xlabel('')

# 保存图片
plt.savefig('images/stock_line1_result.jpg')

# 显示绘制后的图片
plt.show()
