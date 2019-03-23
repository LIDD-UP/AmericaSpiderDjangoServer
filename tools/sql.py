# -*- coding:utf-8 _*-  
""" 
@author:Administrator
@file: sql.py
@time: 2019/3/22
"""
import pymysql
from AmericaSpiderServer.settings import Config
from flask import current_app
#第一一个数据库连接池的方法的类，用于处理链接，查找， 断开链接等功能
#当使用某种方法的时候直接调用即可
class SQLHelper(object):

    @staticmethod
    #处理链接功能，
    def open(cursor):
        #从当前的app中的配置文件中去获取连接池
        POOL = current_app.config["PYMYSQL_POOL"]
        #链接
        conn = POOL.connection()
        cursor = conn.cursor(cursor=cursor)
        return conn,cursor

    @staticmethod
    #处理关闭连接的功能
    def close(conn,cursor):

        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    #处理查找一个的功能，定义成类方法，
    def fetch_one(cls,sql,args,cursor =pymysql.cursors.DictCursor):
        conn,cursor = cls.open(cursor)
        cursor.execute(sql, args)
        obj = cursor.fetchone()
        cls.close(conn,cursor)
        return obj

    @classmethod
    #处理查找多个的功能
    def fetch_all(cls,sql, args,cursor =pymysql.cursors.DictCursor):
        conn, cursor = cls.open(cursor)
        cursor.execute(sql, args)
        obj = cursor.fetchall()
        cls.close(conn, cursor)
        return obj


sql_help = SQLHelper()
conn, cursor = sql_help.open(pymysql.cursors.DictCursor)