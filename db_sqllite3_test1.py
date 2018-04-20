#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DB使用示例。
"""

import sqlite3
import traceback

try:
    # 如果表不存在,就创建
    with sqlite3.connect('./temp/db/test.db') as conn:

        print("Opened database successfully")

        # 删除表
        conn.execute("DROP TABLE IF EXISTS  COMPANY")

        # 创建表
        sql = """
                 CREATE TABLE IF NOT EXISTS COMPANY
               (ID INTEGER  PRIMARY KEY       AUTOINCREMENT,
               NAME           TEXT    NOT NULL,
               AGE            INT     NOT NULL,
               ADDRESS        CHAR(50),
               SALARY         REAL);
        """
        conn.execute(sql)

        print("create table successfully")

        # 添加数据
        conn.executemany("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) VALUES (?, ?, ?, ? )",
                         [('Paul', 32, 'California', 20000.00),
                          ('Allen', 25, 'Texas', 15000.00),
                          ('Teddy', 23, 'Norway', 20000.00),
                          ('Mark', 25, 'Rich-Mond ', 65000.00),
                          ('David', 27, 'Texas', 85000.00),
                          ('Kim', 22, 'South-Hall', 45000.00),
                          ('James', 24, 'Houston', 10000.00)])
        # conn.execute("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY)\
        # VALUES ( 'Paul', 32, 'California', 20000.00 )")
        #
        # conn.execute("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY)\
        # VALUES ('Allen', 25, 'Texas', 15000.00 )")
        #
        # conn.execute("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY)\
        # VALUES ('Teddy', 23, 'Norway', 20000.00 )")
        #
        # conn.execute("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY)\
        # VALUES ( 'Mark', 25, 'Rich-Mond ', 65000.00 )")
        #
        # conn.execute("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY)\
        # VALUES ( 'David', 27, 'Texas', 85000.00 )");
        #
        # conn.execute("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY)\
        # VALUES ( 'Kim', 22, 'South-Hall', 45000.00 )")
        #
        # conn.execute("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY)\
        # VALUES ( 'James', 24, 'Houston', 10000.00 )")

        # 提交,否则重新运行程序时,表中无数据
        conn.commit()
        print("insert successfully")

        # 查询表
        sql = """
            select id,NAME,AGE,ADDRESS,SALARY FROM COMPANY
         """

        result = conn.execute(sql)

        for row in result:
            print("-" * 50)  # 输出50个-,作为分界线
            print("%-10s %s" % ("id", row[0]))  # 字段名固定10位宽度,并且左对齐
            print("%-10s %s" % ("name", row[1]))
            print("%-10s %s" % ("age", row[2]))
            print("%-10s %s" % ("address", row[3]))
            print("%-10s %.2f" % ("salary", row[4]))
            # or
            # print('{:10s} {:.2f}'.format("salary", row[4]))


except sqlite3.Error as e:
    print("sqlite3 Error:", e)
    traceback.print_exc()
