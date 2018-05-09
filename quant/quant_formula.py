#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
量化计算共通类
"""

import pandas as pd
import numpy as np
import math
from math import sqrt
from sklearn import linear_model
from scipy.stats import norm
from scipy import stats
from collections import Iterable
from pandas import Series
from math import sqrt

# Q值(按日计算时)
q_by_day = 250
# Q值(按周计算时)
q_by_week = 52
# Q值(按月计算时)
q_by_month = 12

Rh = 0.035
Rf = 0.03


def Annual_total_return(date_line, return_line, q=q_by_day):
    """
    计算年化总收益率,几何平均数
    收益为：P=V-C
    收益率为：K=P/C=（V-C）/C=V/C-1
    年化收益率为：Y=（1+K）^N-1=（1+K）^（D/T）-1
    其中N=D/T表示投资人一年内重复投资的次数。
    D表示一年的有效投资时间，
        对银行存款、票据、债券等D=360日，
        对于股票、期货等市场D=250日，
        对于房地产和实业等D=365日。
    :param date_line: 日期序列
    :param return_line: 账户日收益率序列
    :param q: q (日收益:250, 周收益:52, 月收益:12)
    :return: 输出周期化的收益率
    """
    T = len(date_line)
    # 期末
    r_tmp = np.array(return_line) + 1.0
    s = 1
    for x in r_tmp:
        s *= x
    r_annual = math.pow(s, q / T) - 1
    return r_annual


def Annual_total_risk(date_line, return_line, q=q_by_day):
    """
    计算年化总风险
    在金融领域中使用标准差或变异系数描述资产风险程度（真实收益率同期望收益率的离散程度）.
    选择portfolio时期望值越高，标准差越小代表投资组合越优质.
    公式:
        标准差 = Sqrt( Σ(X-E(X))^2 /(N or N-1) )

    :param date_line: 日期序列
    :param return_line: 账户日收益率序列
    :param q: q (日收益:250, 周收益:52, 月收益:12)
    :return: 输出周期化的收益率
    """
    T = len(date_line)
    r_tmp = np.array(return_line)
    # 计算均值
    mean_val = np.mean(return_line)
    # 计算各个值与均值差的平方和
    sum_val = np.sum(np.power(return_line - mean_val, 2))
    # 平均后,开平方根
    std_val = math.pow((sum_val * (q / T)), 1 / 2)
    return std_val


def Annual_active_return(date_line, return_line, index_return_line, q=q_by_day):
    """
    计算年化年化主动收益率
    主动年化收益（Aar） = 投资组合年化收益 – 基准年化收益
        If Aar > 0 优于基准年化
        If Aar < 0 劣于基准年化
        根据投资组合标的不同，基准随之变化

    :param date_line: 日期序列
    :param return_line: 账户日收益率序列
    :param index_return_line: 基准日收益率序列
    :param q: q (日收益:250, 周收益:52, 月收益:12)
    :return: 输出周期化的主动收益率
    """
    T = len(date_line)
    Rp = Annual_total_return(date_line=date_line, return_line=return_line, q=q)
    Rbi = Annual_total_return(date_line=date_line, return_line=index_return_line, q=q)
    return Rp - Rbi


def Annual_active_risk(date_line, return_line, index_return_line, q=q_by_day):
    """
    计算年化主动风险
    :param date_line: 日期序列
    :param return_line: 账户日收益率序列
    :param index_return_line: 基准日收益率序列
    :return: 输出年化主动风险
    """
    re = return_line - index_return_line
    re.dropna(inplace=True)
    return Annual_total_risk(date_line, re, q)


def cumulative_return(date_line, return_line):
    """
    计算累计收益率
    :param date_line: 日期序列
    :param return_line: 账户日收益率序列
    :return: 输出账户和基准的累计日收益率序列
    """
    return_line = list(return_line)
    date_line = list(date_line)
    df = pd.DataFrame({'date': date_line, 'rtn': return_line})
    # 累乘
    df['target_cumret'] = (df['rtn'] + 1).cumprod()
    # 返回最后一条
    return float(df['target_cumret'].tail(1))


def alphabetalinearRegression(return_line, index_return_line, rf=Rf, q=q_by_day):
    """
    计算实现α,实现β
    线性回归 Rpi - Rf = α + β(Rbi - Rf) + ε
    参数说明 α(截距项), β(斜率项), ε(随机误差项)

    :rtype: (float,float)
    :param return_line: 账户日收益率序列
    :param index_return_line: 基准日收益序列
    :param rf: RF值
    :param q: q (日收益:250, 周收益:52, 月收益:12)
    :return: 输出(alpha, beta)
    """

    rf_d = np.power((1 + rf), 1 / q) - 1
    Y = return_line - rf_d
    X = index_return_line - rf_d
    X_tmp = np.array(list(X))
    X_tmp = X_tmp.reshape(-1, 1)

    Y_tmp = np.array(list(Y))
    Y_tmp = Y_tmp.reshape(-1, 1)
    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    result = regr.fit(X_tmp * 100, Y_tmp * 100)
    return (result.coef_[0][0], result.intercept_[0])


def residual_term(return_line, index_return_line):
    """
    计算残差余项风险
    εi= Yi – Y(hat)i
    标准差越小说明拟合的线性方程越准确

    :param return_line: 账户日收益率序列
    :param index_return_line: 基准日收益序列
    :return: 输出残差余项风险
    """
    eps = return_line - index_return_line
    return eps.std()


def IR(date_line, return_line, index_return_line, q=q_by_day):
    """
    计算信息比率IR
        IR = 主动收益 / 主动风险
    :param return_line: 账户日收益率序列
    :param index_return_line: 基准日收益序列
    :return: 输出年化主动收益比年化主动风险
    """

    x = Annual_active_return(date_line, return_line, index_return_line, q)
    y = Annual_active_risk(date_line, return_line, index_return_line, q)
    return x / y


def Skew(return_line):
    """
    计算收益率序列的偏度(正态分布)
    :param return_line: 账户日收益率序列
    :return: 输出收益率序列的偏度
    """
    data = return_line.copy()
    return data.skew()


def Kurt(return_line):
    """
    计算收益率序列的峰度(正态分布)
    :param return_line: 账户日收益率序列
    :return: 输出收益率序列的峰度
    """
    data = return_line.copy()
    return data.kurt()


def volatility(date_line, return_line, q=q_by_day):
    """
    计算收益波动率
    :param date_line: 日期序列
    :param return_line: 账户日收益率序列
    :return: 输出回测期间的收益波动率
    """

    df = pd.DataFrame({'date': date_line, 'rtn': return_line})
    # 计算波动率
    vol = df['rtn'].std() * sqrt(q)
    return vol

def Max_Drawdown_withDate(date_line, capital_line):
    """
    计算最大回撤，及恢复到历史高点所用的期数，如仍未恢复到历史高点则记-1

    :param date_line: 日期序列
    :param capital_line: 账户日收益率序列
    :return: 输出(最大回撤, 开始日期, 结束日期, 修复期数)
    """
    df = pd.DataFrame({'date': date_line, 'capital': capital_line})
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by='date', inplace=True)
    df.reset_index(drop=True, inplace=True)

    df['max2here'] = df['capital'].expanding(min_periods=1).max()
    df['dd2here'] = df['capital'] / df['max2here'] - 1

    # 计算最大回撤和结束时间
    tmp = df.sort_values(by='dd2here').iloc[0][['date', 'dd2here']]
    maxdd = tmp['dd2here']
    end_date = tmp['date']
    # 计算开始时间
    df = df[df['date'] <= end_date]
    start_date = df.sort_values(by='capital', ascending=False).iloc[0]['date']

    # print('最大回撤为：%f, 开始于:%s, 结束于:%s, 共:%s '%(maxdd,start_date,end_date,end_date-start_date))
    delta = str(end_date - start_date)
    return (maxdd, str(start_date), str(end_date), delta[0:len(delta) - 14])
