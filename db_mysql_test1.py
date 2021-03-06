#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mysql DB使用示例。
# https://github.com/PyMySQL/PyMySQL/
"""

import pymysql
import traceback
from common import loadcfgcm
from common.dbmysqlcm import DbMysqlClient

# 配置
default_config = """
{
    "host": "localhost",
    "port": 3306,
    "db": "test",
    "charset":"utf8",
    "user": "root",
    "passwd": "root"
}
"""

# 加载配置文件
cfg = loadcfgcm.load("db_mysql_test1.json", default_config)

try:
    # 获取一个数据库连接,with关键字 表示退出时,conn自动关闭
    # with 嵌套上一层的with 要使用closing()
    # 建立和数据库系统的连接
    dbClient = DbMysqlClient("mysql", cfg)

    print("connect database successfully")

    # 删除表
    dbClient.execute("DROP TABLE IF EXISTS  COMPANY")
    # 创建表
    sql = """
             CREATE TABLE IF NOT EXISTS COMPANY
           (ID INTEGER  PRIMARY KEY NOT NULL  auto_increment,
           NAME           TEXT    NOT NULL,
           AGE            INT     NOT NULL,
           ADDRESS        CHAR(50),
           SALARY         REAL);
    """
    dbClient.execute(sql)

    print("create table successfully")

    # 添加数据
    # 在一个conn.execute里面里面执行多个sql语句是非法的
    dbClient.executemany("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) VALUES ( %s, %s, %s, %s )",
                    [('Paul', 32, 'California', 20000.00),
                     ('Allen', 25, 'Texas', 15000.00),
                     ('Teddy', 23, 'Norway', 20000.00),
                     ('Mark', 25, 'Rich-Mond ', 65000.00),
                     ('David', 27, 'Texas', 85000.00),
                     ('Kim', 22, 'South-Hall', 45000.00),
                     ('James', 24, 'Houston', 10000.00)])

    # 提交,否则重新运行程序时,表中无数据
    dbClient.commit()
    print("insert successfully")

    # 查询表
    sql = """
        select id,NAME,AGE,ADDRESS,SALARY FROM COMPANY
     """

    dbClient.execute(sql)

    for row in dbClient.fetchall():
        print("-" * 50)  # 输出50个-,作为分界线
        print("%-10s %s" % ("id", row[0]))  # 字段名固定10位宽度,并且左对齐
        print("%-10s %s" % ("name", row[1]))
        print("%-10s %s" % ("age", row[2]))
        print("%-10s %s" % ("address", row[3]))
        print("%-10s %s" % ("salary", row[4]))

except pymysql.Error as e:
    print("Mysql Error:", e)
    traceback.print_exc()
