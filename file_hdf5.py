#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
一个HDF5文件是一种存放两类对象的容器：dataset和group.
Dataset是类似于数组的数据集，而group是类似文件夹一样的容器，存放dataset和其他group。
在使用h5py的时候需要牢记一句话：groups类比词典，dataset类比Numpy中的数组。
"""

import h5py
import numpy as np
from common import filecm

# 输出文件
tmp_path = "./temp/file/mytestfile.hdf5"
filecm.makedir(tmp_path, by_file=True)

# HDF5的写入：
imgData = np.zeros((30, 3, 128, 256))
# 创建一个h5文件，文件指针是f
f = h5py.File(tmp_path, 'w')
# 将数据写入文件的主键data下面
f['data'] = imgData
# 将数据写入文件的主键labels下面
f['labels'] = range(100)
# 关闭文件
f.close()

# HDF5的读取：
# 打开h5文件
f = h5py.File(tmp_path, 'r')
# 可以查看所有的主键
print(f.keys())
# 取出主键为data的所有的键值
a = f['data'][:]
print(a)
f.close()
