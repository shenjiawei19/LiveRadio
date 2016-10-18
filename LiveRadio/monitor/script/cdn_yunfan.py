# coding:utf-8
import pymysql
from datetime import datetime, timedelta
import hashlib
import requests
import json
from requests.exceptions import ConnectionError
import time
import  socket

hostName = socket.gethostname()
if hostName == r'shenjiawei-Rev-1-0':
    us = 'root'
    p = 'root'
    d = 'LiveRadio'
elif hostName == r'ssf-test.m.ismartv.cn':
    us = 'ssf'
    p = '123456'
    d = 'LiveRadio'

class Net(object):
    def __init__(self, name, key, pwd, channel):
        self.m = hashlib.md5()
        import time
        self.p = (time.strftime("%Y%m%d", time.localtime(time.time()))+name+key+pwd)
        self.info = self.getinfo(channel)
        self.data = self.__format(self.info)

    # 获取信息数据
    def getinfo(self, channel):
        self.m.update(self.p)
        passwd = self.m.hexdigest()

        five_ago = str(datetime.now() + timedelta(minutes=-5))
        five_ago = five_ago[0:10]+five_ago[11:16]
        ten_ago = str(datetime.now() + timedelta(minutes=-10))
        ten_ago = five_ago[0:10]+ten_ago[11:16]
        url = r'http://console.yunfancdn.com/api/cdn.php?u=shiyun&p='+str(passwd)+'&starttime='\
              +ten_ago+'&endtime='+five_ago+'&channel='+channel+'&backsource=1'
        try:
            r = requests.get(url)
            return json.loads(r.content)
        except ConnectionError as e :
            return {}


    # 格式化信息数据，为了插入数据库
    def __format(self,info):
        try:
            st = info['status']
            # chan = "'"+info['data'][0]['channel']+"'"
            band = info['data'][0]['bandwidth'].values()[0]
            bp = info['data'][0]['bypass'].values()[0]
            tm = info['data'][0]['bandwidth'].keys()[0]
            timeArray = time.strptime(tm, "%Y-%m-%d %H:%M")
            timeStamp = int(time.mktime(timeArray))
            return st, band, bp, timeStamp
        except KeyError as e:
            print e
            return 0


# 数据库插入信息
def insert_sql(data):
    try:
        conn = pymysql.connect(host='localhost', port=3306, user=us, passwd=p, charset='UTF8', database=d)
        # 获取一个游标对象
        cur = conn.cursor()
        # 插入数据 1:yunfan[cdn.brand] 2: yunfan[cdn.pass]
        sql1 = "INSERT INTO monitor_history (status,special_id,value,his_clock) VALUES (%d,%d,%f,%d)" % \
              (data[0],1,data[1], data[3])
        sql2 = "INSERT INTO monitor_history (status,special_id,value,his_clock) VALUES (%d,%d,%f,%d)" % \
              (data[0],2,data[2], data[3])
        cur.execute(sql1)
        cur.execute(sql2)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print e

def get_monitor(data):
    try:
        conn = pymysql.connect(host='localhost', port=3306, user=us, passwd=p, charset='UTF8', database=d)
        # 获取一个游标对象
        cur = conn.cursor()
        week_ago = data[3]-604800
        # 查询数据
        sql = "SELECT `monitor_history`.`value`, `monitor_history`.`his_clock` " \
              "FROM `monitor_history` INNER JOIN `monitor_special` " \
              "ON (`monitor_history`.`special_id` = `monitor_special`.`id`)" \
              " WHERE `monitor_special`.`name` = 'yunfan[cdn.brand]' " \
              "and `monitor_history`.`his_clock`=%d"%(week_ago)
        cur.execute(sql)
        # 获取数据
        da = 0
        sql_data = cur.fetchall()
        if len(sql_data) > 0:
            for row in sql_data:
                da = row[0] * 1.2
        if data[1] > da:
            info = "云帆宽带流量周环比大于20% 现值 "+str(data[1])+" 上周 "+str(da)
            fd = open('monitor.txt','a+')
            fd.writelines(info+'\n')
            fd.close()
        else:
            pass
    except Exception as e:
        print e
        return 0
    return 0

if __name__ == '__main__':
    u = 'shiyun'
    api_key = r'uKKwKJrMAqUGyp9b7LABmQjsdZfXUGAn'
    api_pwd = r'pssQgvOH'
    channel = r'yf.v.tvxio.com'
    # 1:yunfan[cdn.brand] 2: yunfan[cdn.pass]
    brand = Net(u, api_key, api_pwd, channel=channel)
    insert_sql(brand.data)
    get_monitor(brand.data)
