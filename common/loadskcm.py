# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
SkLearn Data Load Common
SkLearn用数据加载共通
"""

import os
import pandas as pd

from pandas import DataFrame

from sklearn import datasets
from common import logcm


def load_diabetes():
    """
    Load the diabetes dataset
    @return: diabetes dataset by (data, target)
    """

    # 文件路径
    file_path_data = './cache/sk/sk_diabete_data.csv'
    file_path_target = './cache/sk/sk_diabete_target.csv'
    # 如果存在数据文件，则直接读取
    if os.path.exists(file_path_data):
        # 读取文件
        df_data = pd.read_csv(file_path_data)
        df_target = pd.read_csv(file_path_target)
        return df_data.as_matrix(), df_target.as_matrix()

    else:
        # 取得数据
        diabetes = datasets.load_diabetes()
        logcm.print_obj(diabetes.DESCR, 'diabetes.DESCR')
        logcm.print_obj(diabetes.data, '样本原始数据集')
        logcm.print_obj(diabetes.target, '样本目标数据集')

        # 保存到文件
        DataFrame(diabetes.data).to_csv(file_path_data, index=False)
        DataFrame(diabetes.target).to_csv(file_path_target, index=False)

        return diabetes.data, diabetes.target
