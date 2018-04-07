#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
线性回归（1）
典型的相关性分析步骤有三步
第一：绘制散点图
第二：计算相关系数
第三：相关系数检验
样例数据来源：skLearn
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

from common import plotcm
from common import statcm
from common import logcm
from common import loadskcm

# Load the diabetes dataset
# 加载线性回归的样本数据
df_data, df_target = loadskcm.load_diabetes()

# Use only one feature
# np.newaxis 用来增加维度, 只用索引2的特征数据来演示
diabetes_X = df_data[:, np.newaxis, 2]
logcm.print_obj(diabetes_X, '样本提取数据集')

# Split the data and targets into training/testing sets
# 取末尾30个数据为测试数据
diabetes_X_test = diabetes_X[-30:]
logcm.print_obj(diabetes_X_test, 'diabetes_X_test')

# 取测试数据对应的目标值
diabetes_y_test = df_target[-30:]
logcm.print_obj(diabetes_y_test, 'diabetes_y_test')

# 末尾30之外所有数据为训练数据
diabetes_X_train = diabetes_X[:-30]
logcm.print_obj(diabetes_X_train, 'diabetes_X_train')

# 取得训练数据对应的目标值
diabetes_y_train = df_target[:-30]
logcm.print_obj(diabetes_y_train, 'diabetes_y_train')

# 多子图绘制
fig, axes = plt.subplots(2, 2, figsize=(10, 6), sharey=True, sharex=True)
# 设置图片尺寸
fig.set_size_inches(10, 6)
# 总标题
fig.suptitle(u'线性回归（Linear Regression）示例')
# 设置标题(中文字体)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# Plot outputs
# 训练数据的散点图
axes[0][0].scatter(diabetes_X_train, diabetes_y_train, color='black')
axes[0][0].set_title('训练数据散点图')

# Create linear regression object
# 线性回归模型
regr = linear_model.LinearRegression()

# Train the model using the training sets
# 使用训练数据对模型进行训练
regr.fit(diabetes_X_train, diabetes_y_train)

# Make predictions using the testing set
# 使用训练后的模型进行预测
diabetes_y_pred = regr.predict(diabetes_X_test)
logcm.print_obj(diabetes_y_pred, 'diabetes_y_pred')

# Plot outputs
# 训练数据散点图
axes[0][1].scatter(diabetes_X_train, diabetes_y_train, color='black')
# 计算训练数据的相关系数
corr, corr_level = statcm.corr_test(diabetes_X_train, diabetes_y_train)
logcm.print_obj(corr, 'corr : 相关系数')
logcm.print_obj(corr_level, 'corr_level : 相关程度')
text = '相关系数 : %f\n相关程度 : %s' % (corr, corr_level)
plotcm.draw_text(axes[0][0], diabetes_X_train, diabetes_y_train, text,
                 color='r', font_size='9', v_align="bottom", h_align="right")

# 线性回归后的预测直线
axes[0][1].plot(diabetes_X_test, diabetes_y_pred, color='blue', linewidth=3)
axes[0][1].set_title('训练后得到的直线')
text = '回归系数 : %f' % regr.coef_
plotcm.draw_text(axes[0][1], diabetes_X_train, diabetes_y_train, text,
                 color='r', font_size='9', v_align="bottom", h_align="right")

# The coefficients
# 回归系数
# 例如回归方程式Y=bX+a中，斜率b称为回归系数
logcm.print_obj(regr.coef_, 'Coefficients : 回归系数')

# The mean squared error
# 均方误差(测试数据 VS 预测数据)
squared_error = mean_squared_error(diabetes_y_test, diabetes_y_pred)
logcm.print_obj(squared_error, "Mean squared error : 均方误差(测试数据 VS 预测数据)")

# Explained variance score: 1 is perfect prediction
# R2决定系数-拟合优度(测试数据 VS 预测数据)
score = r2_score(diabetes_y_test, diabetes_y_pred)
logcm.print_obj(score, 'Variance score : 差额比分(测试数据 VS 预测数据)')

# Plot outputs
# 测试数据散点图
axes[1][0].scatter(diabetes_X_test, diabetes_y_test, color='black')
axes[1][0].set_title('测试数据散点图')
# 计算测试数据的相关系数
corr, corr_level = statcm.corr_test(diabetes_X_test, diabetes_y_test)
logcm.print_obj(corr, 'corr : 相关系数')
logcm.print_obj(corr_level, 'corr_level : 相关程度')
text = '相关系数 : %f\n相关程度 : %s' % (corr, corr_level)
plotcm.draw_text(axes[1][0], diabetes_X_test, diabetes_y_test, text,
                 color='r', font_size='9', v_align="top", h_align="left")

# Plot outputs
# 测试数据散点图
axes[1][1].scatter(diabetes_X_test, diabetes_y_test, color='black')
# 测试数据预测结果直线
axes[1][1].plot(diabetes_X_test, diabetes_y_pred, color='blue', linewidth=3)
axes[1][1].set_title('测试数据和预测数据对比图')

text = '均方差 : %f （越大越分散）\n拟合优度 : %f （1最好，0最差）' % (squared_error, score)
plotcm.draw_text(axes[1][1], diabetes_X_test, diabetes_y_test, text,
                 color='r', font_size='9', v_align="top", h_align="left")

# 不显示XY轴刻度
plt.xticks(())
plt.yticks(())

# 保存图片
plt.savefig('images/linear_regression1_result.jpg')
# 显示绘制后的图片
plt.show()
