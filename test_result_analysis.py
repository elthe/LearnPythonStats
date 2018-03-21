# pandas 使用示例
# pandas ：pannel data analysis（面板数据分析）。
# pandas是基于numpy构建的，为时间序列分析提供了很好的支持。
# pandas中有两个主要的数据结构，一个是Series，另一个是DataFrame。

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from pandas import DataFrame, Series


# Mac下加载CSV文件的方法
path = os.getcwd() + '/data/test_result.csv'
data = pd.read_csv(path)

# DataFrame是一个类似表格的数据结构，
# 索引包括列索引和行索引，包含有一组有序的列，
# 每列可以是不同的值类型（数值、字符串、布尔值等）。
# DataFrame的每一行和每一列都是一个Series，
# 这个Series的name属性为当前的行索引名/列索引名。

df1 = DataFrame(data)
print(df1)
print('----full data loaded---------\n')

# 按分数排倒序，取前20名
dfSort = df1.sort_values(by='score', ascending=False)
dfHead = dfSort.head(20)
print(dfHead)
print('----head 10 of high score in total-----------\n')

# 取倒数20名
dfTail = dfSort.tail(20)
print(dfTail)
print('----tail 10 of high score in total--------------\n')

#按code，对平均分排序
dfGroupSortMean = DataFrame(data, columns=['code', 'score']).groupby('code').mean().sort_values(by='score', ascending=False)
print(dfGroupSortMean)
print('----group data by code with score mean and sort DESC--------------\n')

#按code，对平均分排序
dfGroupSortCount = DataFrame(data, columns=['code', 'score']).groupby('code').count().sort_values(by='score', ascending=False)
print(dfGroupSortCount)
print('----group data by code with count mean and sort DESC--------------\n')

# 按照Code，统计：平均值,合计值，总件数
dfSub = DataFrame(data, columns=['code', 'name', 'score'])
print(dfSub)
print('----pick some columns to make a sub dataframe--------------\n')

# 组合Groupby统计，每个列可以有一个函数
dfGroupMulti = dfSub.groupby('code').agg({'score':'mean', 'name':'count'})
print(dfGroupMulti)
print('----group data by code with mean, count--------------\n')

# 修改显示的列名
dfGroupMulti = dfGroupMulti.rename(columns={'name' : 'count', 'score' : 'mean'})
# 排序
dfGroupSortMulti = dfGroupMulti.sort_values(by='mean', ascending=False)
print(dfGroupSortMulti)
print('----after column rename and sort by mean DESC--------------\n')

# Series 类似于一维数组与字典(map)数据结构的结合。
# 它由一组数据和一组与数据相对应的数据标签（索引index）组成。
# 这组数据和索引标签的基础都是一个一维ndarray数组。
# 可将index索引理解为行索引。
# Series的表现形式为：索引在左，数据在右。

seriesCode = dfHead['code']
print(seriesCode)
print('----pick column code to series--------------\n')

seriesScore = dfTail['score']
print(seriesScore)
print('----pick column score to series--------------\n')

# 绘制报告图
# 多子图绘制
fig, axes = plt.subplots(2, 2, sharex=True)
# 设置图片尺寸
#fig.set_size_inches(10, 6)
# 总标题
fig.suptitle(u'分数分布报表')
# 设置标题(中文字体)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

df2 = DataFrame(data, columns=['code', 'score']).groupby('code').mean().rename(columns={'score' : 'mean'})
df2.plot(kind='bar', ax=axes[0][0], title='mean')

df3 = DataFrame(data, columns=['code', 'score']).groupby('code').max().rename(columns={'score' : 'max'})
df3.plot(kind='bar', ax=axes[1][0], title='max')

df4 = DataFrame(data, columns=['code', 'score']).groupby('code').std().rename(columns={'score' : 'std'})
df4.plot(kind='bar', ax=axes[1][1], title='std')

df5 = DataFrame(data, columns=['code', 'score']).groupby('code').count().rename(columns={'score' : 'count'})
df5.plot(kind='bar', ax=axes[0][1], title='count')

# 保存图片
plt.savefig('images/test_result_analysis_result.jpg')
# 显示绘制后的图片
plt.show()