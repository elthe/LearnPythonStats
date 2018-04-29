#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
matplotlib.animation使用示例。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# 每次产生一个新的坐标点
def data_gen():
    t = data_gen.t
    cnt = 0
    while cnt < 1000:
        cnt += 1
        t += 0.05
        yield t, np.sin(2 * np.pi * t) * np.exp(-t / 10.)


data_gen.t = 0

# 绘图
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_ylim(-1.1, 1.1)
ax.set_xlim(0, 5)
ax.grid()
xdata, ydata = [], []


# 因为run的参数是调用函数data_gen,所以第一个参数可以不是framenum:设置line的数据,返回line
def run(data):
    # update the data
    t, y = data
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()

    if t >= xmax:
        ax.set_xlim(xmin, 2 * xmax)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line,


# 每隔10秒调用函数run,run的参数为函数data_gen,
# 表示图形只更新需要绘制的元素
ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=10,
                              repeat=False)
plt.show()