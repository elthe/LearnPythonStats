#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
多线程，线程锁，任务队列的简单例子
"""

import queue
import time
import threading
import numpy as np

from common import logcm
from common import datecm


def run_task(sleep_seconds):
    # 声明使用全局锁
    global lock, queue_list

    # 取得当前线程
    thd_now = threading.current_thread()
    thd_name = thd_now.getName()

    # 循环直到任务队列为空
    while not queue_list.empty():
        # 取得任务编号
        task = queue_list.get()
        # 锁请求
        if lock.acquire():
            # 当前时间
            now_time = datecm.now_time_str('%Y-%m-%d %H:%M:%S')
            # 输出日志（同时只有一个线程可以写日志）
            logcm.print_info("%s is doing %s sleep %d seconds. %s " % (thd_name, task, sleep_seconds, now_time))
            # 释放锁
            lock.release()

        # 等待N秒后继续
        time.sleep(sleep_seconds)


# 初始化任务队列
queue_list = queue.Queue()
for i in range(10):
    # 在队列中加入新的任务号
    queue_list.put('Task-%d' % (i + 1))

# 线程锁
lock = threading.Lock()

# 启动多个线程
thd_list = []
for i in range(5):
    # 新建线程，指定执行方法及参数
    rands = np.random.randint(1, 4)
    thd = threading.Thread(target=run_task, args=(rands,))
    thd_list.append(thd)
    # 设定线程的名称
    thd.setName("Thread-%d" % (i + 1))
    # 启动线程
    thd.start()

# 调用Thread.join将会使主调线程堵塞，直到被调用线程运行结束或超时。
# 参数timeout是一个数值类型，表示超时时间，
# 如果未提供该参数，那么主调线程将一直堵塞到被调线程结束。
# for thd in thd_list:
#     thd.join()
# 所有线程结束后，自动退出程序
# sys.exit()
