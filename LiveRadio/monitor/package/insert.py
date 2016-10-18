# coding:utf-8
import pymysql
from datetime import datetime, timedelta
import hashlib
import requests
import json
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


class cdn(object):

    # name表示api所需用户名
    # key表示api的key值
    # pwd表示api的密码
    # channel表示api的频道号

    def __init__(self,**kwargs):
        self.username = kwargs.get('username',None)
        self._password =kwargs.get('password',None)
        self.key = kwargs.get('key',None)
        self.channel = kwargs.get('channel',None)


    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        pass


    def getinfo(self):
        return self.format_date()

    def format_date(self):
        pass

    def insert(self,sql='',host=None, port=3306, user='root', password='root', charset='UTF8', database=None):
        try:
            conn = pymysql.connect(host=host, port=port, user=user, passwd=password, charset=charset,
                                   database=database)
            # 获取一个游标对象
            cur = conn.cursor()
            # 插入数据 1、id 2、status 3、channel 4、bandwidth 5、bypass 6、time
            # sql = "INSERT INTO cdn_monitor (status,channel,bandwidth,bypass,TIME) VALUES (%d,%s,%f,%f,%s)" % \
            #       (data[0], data[1], data[2], data[3], data[4])
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as error:
            print error

if __name__ == '__main__':
    a = cdn(username = "222",password = "333")
