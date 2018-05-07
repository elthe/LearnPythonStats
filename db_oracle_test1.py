#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Oracle DB使用示例。
安装驱动说明：
https://cx-oracle.readthedocs.io/en/latest/installation.html#installing-cx-oracle-on-macos
"""

from common import loadcfgcm
from common.dboraclecm import DbOracleClient

# 配置
default_config = """
{
    "host": "localhost",
    "port": 1521,
    "db": "orcl",
    "user": "root",
    "passwd": "root"
}
"""

# 加载配置文件
cfg = loadcfgcm.load("db_oracle_test1.json", default_config)

# 建立和数据库系统的连接
dbClient = DbOracleClient("oracle", cfg)

# 执行SQL,创建一个表
sql = """
    create table tb_user(
        id number, 
        name varchar2(50),
        password varchar(50),
        primary key(id)
    )
"""
dbClient.execute(sql)

# 插入一条记录
sql = """
    insert into
      tb_user 
    values
      (1,'admin','password')
"""
dbClient.execute(sql)

# 再插入一条数据
param = {'id': 2, 'n': 'admin', 'p': 'password'}
dbClient.execute('insert into tb_user values(:id,:n,:p)', param);

# 一次插入多条数据,参数为字典列表形式
param = [{'id': 3, 'n': 'admin', 'p': 'password'},
         {'id': 4, 'n': 'admin', 'p': 'password'},
         {'id': 5, 'n': 'admin', 'p': 'password'}];
dbClient.executemany('insert into tb_user values(:id,:n,:p)', param);

# 再一次插入多条数据
param = [];
# 生成5条插入数据，参数为元组列表形式
for i in range(6, 11):  # [6,7,8,9,10]
    param.append((i, 'user' + str(i), 'password' + str(i)))
# 插入数据
dbClient.executemany('insert into tb_user values(:1,:2,:3)', param);

# 执行查询 语句
sql = """select * from tb_user"""

# 获取一条记录
one = dbClient.fetchone(sql)
print('1: id:%s,name:%s,password:%s' % one)

# 获取两条记录!!!注意游标已经到了第二条
two = dbClient.fetchmany(sql, {}, 2)
print('2 and 3:', two[0], two[1])

# 获取其余记录!!!注意游标已经到了第四条
three = dbClient.fetchall(sql)
for row in three:
    # 打印所有结果
    print(row)

# print('条件查询')
# cursor.prepare("""select * from tb_user where id <= :id""")
# cursor.execute(None, {'id': 5})
# for row in cursor:  # 相当于fetchall()
#     print(row)

# 执行查询 语句
sql = """drop table tb_user"""
dbClient.execute(sql)


# 执行完成，打印提示信息
print('Completed!')
