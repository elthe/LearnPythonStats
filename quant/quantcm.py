#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
量化计算共通类
"""

import pandas as pd
import numpy as np
import math
from scipy.stats import norm
from scipy import stats
from collections import Iterable
from pandas import Series
from math import sqrt
from quant import quant_formula as formula

q = 250
Rh = 0.035
Rf = 0.03


class QuantResult:
    ## #综合类量化指标
    # 年化总收益率
    Annual_total_return = None
    # 基准年化总收益率
    Annual_total_index_return = None
    # 年化总风险
    Annual_total_risk = None
    # 年化主动收益率
    Annual_active_return = None
    # 年化主动风险
    Annual_active_risk = None
    # 累计收益率
    cumulative_return = None
    # alpha
    alpha = None
    # beta
    beta = None
    # 残差余项风险
    residual_term = None
    # 信息比率
    IR = None
    # 收益率序列的偏度
    Skew = None
    # 收益率序列的峰度
    Kurt = None

    ## 风险类量化指标
    # 回测期间的收益波动率
    volatility = None
    # 最大回撤
    Max_Drawdown = None
    # 修复期数
    Max_Drawdown_recover_period = None
    # 夏普比例
    SharpRatio = None
    # 日收益率的索提诺序列
    SortinoRatio = None
    # 下行风险概率
    DownsideRisk_LMPN = None
    # VAR最大在险价值
    varHistory = None
    # 最大连续上涨天数
    Max_consecutive_up_days = None
    # 最大连续下跌天数
    Max_consecutive_down_days = None
    # 最大连续涨幅
    Max_consecutive_down_peak = None
    # 盈利期占比
    profit_period_ratio = None
    # 亏损期占比
    loss_period_ratio = None
    # 盈利天数
    profit_period_days = None
    # 亏损期天数
    loss_period_days = None


class QuantCalculator:
    def __init__(self, date_line, capital_line, return_line, index_line, index_return_line):
        """
        初始化方法.
        :param date_line: 日期序列
        :param capital_line: 账户日净值序列
        :param return_line: 账户日收益率序列
        :param index_line: 指数资产序列
        :param index_return_line: 基准日收益序列
        :return: 无
        """

        self.date_line = date_line
        self.capital_line = capital_line
        self.return_line = return_line
        self.index_line = index_line
        self.index_return_line = index_return_line

    def calculate_quant(self):
        """
        计算量化指标
        :return: 计算结果
        """
        # 计算结果
        self.result = QuantResult()
        ## 综合类量化指标
        # 年化总收益率
        result.Annual_total_return = formula.Annual_total_return(self.date_line, self.return_line)
        # 基准年化收益
        result.Annual_total_index_return = formula.Annual_total_return(self.date_line, self.index_return_line)
        # 年化总风险
        result.Annual_total_risk = formula.Annual_total_risk(self.date_line, self.return_line)
        # 主动年化收益率（Aar） = 年化总收益率 – 基准年化总收益率
        result.Annual_active_return = result.Annual_total_return - result.Annual_total_index_return
        # 年化主动风险
        result.Annual_active_risk = formula.Annual_active_risk(self.date_line, self.return_line, self.index_return_line)
        # 累计收益率
        result.cumulative_return = formula.cumulative_return(self.date_line, self.return_line)
        # alpha, beta
        result.alpha, result.beta = formula.alphabetalinearRegression(self.return_line, self.index_return_line)
        # 残差余项风险
        result.residual_term = formula.residual_term(self.return_line, self.index_return_line)
        # 信息比率 = 主动收益 / 主动风险
        result.IR = self.Annual_active_return / self.Annual_active_risk
        # 收益率序列的偏度
        result.Skew = formula.Skew(self.return_line)
        # 收益率序列的峰度
        result.Kurt = formula.Kurt(self.return_line)

        ## 风险类量化指标
        # 回测期间的收益波动率
        result.volatility = formula.volatility(self.date_line, self.return_line)
        # 最大回撤
        result.Max_Drawdown = None
        # 修复期数
        result.Max_Drawdown_recover_period = None
        # 夏普比例
        result.SharpRatio = None
        # 日收益率的索提诺序列
        result.SortinoRatio = None
        # 下行风险概率
        result.DownsideRisk_LMPN = None
        # VAR最大在险价值
        result.varHistory = None
        # 最大连续上涨天数
        result.Max_consecutive_up_days = None
        # 最大连续下跌天数
        result.Max_consecutive_down_days = None
        # 最大连续涨幅
        result.Max_consecutive_down_peak = None
        # 盈利期占比
        result.profit_period_ratio = None
        # 亏损期占比
        result.loss_period_ratio = None
        # 盈利天数
        result.profit_period_days = None
        # 亏损期天数
        result.loss_period_days = None


if __name__ == '__main__':
    result = QuantResult()
    result.Annual_active_return = 123
    print(result.Annual_active_return)
