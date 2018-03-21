# matplotlib提供了一些金融图表主要用于可视化历史股票价格,或者类似的金融时间序列数据
# 在matplotlib.finance的子库中也提供了获取历史数据的函数
# 版本matplotlib 2.2中，finance会被替换成mpl_finance,但是在2.0版本中
# import matplotlib.finance as mpf仍可以使用
# data = mpf.quotes_historical_yahoo('code',start, end)
# 但是web数据来源的数据不足以作为任何重要投资的决策基础,本文中的数据通过tushare获取

# -*- coding:utf-8 -*-
import matplotlib as mpl
import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.finance as mpf

wdyx = ts.get_k_data('002739','2017-01-01')
print(wdyx.shape)
print(wdyx[:15])

# 由于数据不是通过,mpf.candlestick_ohlc()获取的,所以日期的格式与,绘图函数的不一致
# tushare回去的数据对象为DataFrame类型
# 所以要将格式转换为mpf.candlestick_ohlc()能够处理的浮点数格式

# 导入两个涉及的库
from matplotlib.pylab import date2num
import datetime

# 对tushare获取到的数据转换成candlestick_ohlc()方法可读取的格式
'''
data_list = []
for dates,row in hist_data.iterrows():
    # 将时间转换为数字
    date_time = datetime.datetime.strptime(dates,'%Y-%m-%d')
    t = date2num(date_time)
    open,high,low,close = row[:4]
    datas = (t,open,high,low,close)
    data_list.append(datas)
'''
def date_to_num(dates):
    num_time = []
    for date in dates:
        date_time = datetime.datetime.strptime(date,'%Y-%m-%d')
        num_date = date2num(date_time)
        num_time.append(num_date)
    return num_time

# dataframe转换为二维数组
mat_wdyx = wdyx.as_matrix()
num_time = date_to_num(mat_wdyx[:,0])
mat_wdyx[:,0] = num_time


# 日期,   开盘,     收盘,    最高,      最低,   成交量,    代码
print(mat_wdyx[:3])

# 数据列的顺序,从左至右是,开盘,收盘,最高,最低,成交量
# matplotlib.finance中有两个函数,一个是candlestick_ochl(),刚好对应上边的顺序
# 另一个是candlestick_ohlc(),对应的是开盘,最高,最低,收盘的数据格式

# 接下来可以绘制K线图了

fig, ax = plt.subplots(figsize=(15,5))
fig.subplots_adjust(bottom=0.5)
mpf.candlestick_ochl(ax, mat_wdyx, width=0.6, colorup='g', colordown='r', alpha=1.0)
plt.grid(True)

# 设置日期刻度旋转的角度
# plt.xticks(rotation=30)
# plt.title('wanda yuanxian 17')
# plt.xlabel('Date')
# plt.ylabel('Price')
# x轴的刻度为日期
# ax.xaxis_date ()
###candlestick_ochl()函数的参数
# ax 绘图Axes的实例
# mat_wdyx 价格历史数据
# width    图像中红绿矩形的宽度,代表天数
# colorup  收盘价格大于开盘价格时的颜色
# colordown   低于开盘价格时矩形的颜色
# alpha      矩形的颜色的透明度

# 金融数据每日摘要图表
# 开盘价格和收盘价格由两条水平线表示

# fig, ax = plt.subplots(figsize=(15,5))
# mpf.plot_day_summary_oclh(ax, mat_wdyx,colorup='g', colordown='r')
# plt.grid(True)
# ax.xaxis_date()
# plt.title('wandayuanxian 17')
# plt.ylabel('Price')

# k线图和成交量(柱状图)的组合图表

# fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(15,8))
# mpf.candlestick_ochl(ax1, mat_wdyx, width=1.0, colorup = 'g', colordown = 'r')
# ax1.set_title('wandayuanxian')
# ax1.set_ylabel('Price')
# ax1.grid(True)
# ax1.xaxis_date()
# plt.bar(mat_wdyx[:,0]-0.25, mat_wdyx[:,5], width= 0.5)
# ax2.set_ylabel('Volume')
# ax2.grid(True)

plt.show()
