# pandas 使用示例
# pandas ：pannel data analysis（面板数据分析）。
# pandas是基于numpy构建的，为时间序列分析提供了很好的支持。
# pandas中有两个主要的数据结构，一个是Series，另一个是DataFrame。

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
print('------------------')

# 取前N个
dfHead = df1.head(10)
print(dfHead)
print('------------------')

# 取末尾N个
dfTail = df1.tail(10)
print(dfTail)
print('------------------')

# 按照Code，统计：平均值,合计值，总件数
dfGroup = DataFrame(data, columns=['code', 'score']).groupby('code').agg([np.mean, np.sum, np.count_nonzero])
print(dfGroup)
print(type(dfGroup))
#dfGroup.sort_values(by=['code'])
#print(dfGroup)
#print(DataFrame(data, columns=['code', 'score']).groupby('code').sum())
#print(DataFrame(data, columns=['code', 'score']).groupby('code').count())
#dfGroup2 = dfGroup.reset_index()
#print(type(dfGroup2))
#dfGroup2.sort()
#print(dfGroup2)
#print(dfGroup2.sort_values(by = ['score']))

# Series 类似于一维数组与字典(map)数据结构的结合。
# 它由一组数据和一组与数据相对应的数据标签（索引index）组成。
# 这组数据和索引标签的基础都是一个一维ndarray数组。
# 可将index索引理解为行索引。
# Series的表现形式为：索引在左，数据在右。

seriesCode = dfHead['code']
print(seriesCode)
print('------------------')

seriesScore = dfTail['score']
print(seriesScore)
print('------------------')

