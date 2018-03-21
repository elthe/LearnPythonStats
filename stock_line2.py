# -*- coding:utf-8 -*-
import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import datetime
from matplotlib.pylab import date2num

wdyx = ts.get_k_data('000001','2015-01-01','2016-12-31')
print(wdyx)

# 对tushare获取到的数据转换成candlestick_ohlc()方法可读取的格式
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

# 接下来可以绘制K线图了
# 多子图绘制
fig, axes = plt.subplots(2, 1, figsize=(15,7), sharey=False, sharex=True)
# 设置图片尺寸
fig.set_size_inches(10, 6)
# 总标题
fig.suptitle(u'股票价格成交量K线图')
# 设置标题(中文字体)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

# 绘制K线的蜡烛图
mpf.candlestick_ochl(axes[0], mat_wdyx, width=0.6, colorup='g', colordown='r', alpha=1.0)
plt.grid(True)

# 设置日期刻度旋转的角度
plt.xticks(rotation=30)
# x轴的刻度为日期
axes[0].xaxis_date()
axes[0].set_ylabel('Price')
axes[0].grid(True)

# 绘制条形图
plt.bar(mat_wdyx[:,0]-0.25, mat_wdyx[:,5], width= 0.5)
axes[1].set_ylabel('Volume')
axes[1].grid(True)

# 保存图片
plt.savefig('images/stock_line2_result.jpg')

# 显示绘制后的图片
plt.show()