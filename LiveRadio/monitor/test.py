#!/usr/bin/python
# coding:utf-8

import pymysql

def get_sql():
    date = []
    brand_list = []
    bypass_list = []
    try:
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', charset='UTF8', database='ismartv_cdn')
        # 获取一个游标对象
        cur = conn.cursor()
        # 查询数据
        cur.execute("SELECT bandwidth,bypass, TIME FROM cdn_monitor where channel='upyun' order by time DESC limit 240")
        # 获取数据
        data = cur.fetchall()
        for row in data:
            brand_list.append(row[0])
            bypass_list.append(row[1])
            date.append(row[2])
    except Exception as e:
        print e
