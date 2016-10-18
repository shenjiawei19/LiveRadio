# coding:utf-8
import pymysql
from datetime import datetime, timedelta
import requests
import time
import  socket
import json

hostName = socket.gethostname()
if hostName == r'shenjiawei-Rev-1-0':
    u = 'root'
    p = 'root'
    d = 'LiveRadio'
elif hostName == r'ssf-test.m.ismartv.cn':
    u = 'ssf'
    p = '123456'
    d = 'LiveRadio'

class Net(object):
    def __init__(self):
        self.info,self.pas = self.__GetUrl()
        self.data = self.__format(self.info,self.pas)

    # 获取信息数据
    def __GetUrl(self):
        ten_Ago = (datetime.now() - timedelta(minutes=10)).strftime('%Y%m%d%H%M')
        five_Ago = (datetime.now() - timedelta(minutes=5)).strftime('%Y%m%d%H%M')
        url='http://api.open.letvcloud.com/data/traffic?productline=CDN&domaintype=VOD&startday=%s&endday=%s&granularity=5min&unit=M' % (ten_Ago, five_Ago)
        hds1 = {
            # 'Authorization': 'Basic  ODA4OTI2OmU0ZmUwMjE3YjlkYmJkYjY2ZGQ1Yjc3ZWM3ODAyZjdi',
            'Authorization': 'Basic  ODA4OTI2OjNhYjVhZTkzMGIwNTkxODBkMTNjZjQzZTlhOTQ2ZmQy',
                'Lecloud-api-version': '0.4',
                'Accept': 'application/json'
            }
        req1 = requests.get(url, headers=hds1)

        url='http://api.open.letvcloud.com/data/origin_traffic?productline=CDN&domaintype=VOD&startday=%s&endday=%s&granularity=5min&unit=M' % (ten_Ago, five_Ago)
        hds2 = {
            'Authorization': 'Basic  ODA4OTI2OmU0ZmUwMjE3YjlkYmJkYjY2ZGQ1Yjc3ZWM3ODAyZjdi',
            # 'Authorization': 'Basic  ODA4OTI2OjNhYjVhZTkzMGIwNTkxODBkMTNjZjQzZTlhOTQ2ZmQy',
                'Lecloud-api-version': '0.4',
                'Accept': 'application/json'
            }
        req2 = requests.get(url, headers=hds2)
        print json.loads(req1.content),json.loads(req2.content)
        return json.loads(req1.content),json.loads(req2.content)


    # 格式化信息数据，为了插入数据库
    def __format(self, info,pas):
        if info is not None:
            st = 1
        else:
            st = 0
        band = info['data']['traffic']['valuelist'][0]*8/300
        tm = info['data']['traffic']['timelist'][0]
        timeArray = time.strptime(tm, "%Y%m%d%H%M")
        timeStamp = int(time.mktime(timeArray))
        bypass = pas['data']['traffic']['valuelist'][0]*8/300
        return st, int(band), bypass, timeStamp


def insert_sql(data):
    try:
        conn = pymysql.connect(host='localhost', port=3306, user=u, passwd=p, charset='UTF8', database=d)
        # 获取一个游标对象
        cur = conn.cursor()
        # 插入数据 1:yunfan[cdn.brand] 2: yunfan[cdn.pass]
        sql1 = "INSERT INTO monitor_history (status,special_id,value,his_clock) VALUES (%d,%d,%f,%d)" % \
              (data[0],3,data[1], data[3])
        sql2 = "INSERT INTO monitor_history (status,special_id,value,his_clock) VALUES (%d,%d,%f,%d)" % \
              (data[0],4,data[2], data[3])
        cur.execute(sql1)
        cur.execute(sql2)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print e

def get_monitor(data):
    try:
        conn = pymysql.connect(host='localhost', port=3306, user=u, passwd=p, charset='UTF8', database=d)
        # 获取一个游标对象
        cur = conn.cursor()
        week_ago = data[3]-604800
        # 查询数据
        sql = "SELECT `monitor_history`.`value`, `monitor_history`.`his_clock` " \
              "FROM `monitor_history` INNER JOIN `monitor_special` " \
              "ON (`monitor_history`.`special_id` = `monitor_special`.`id`)" \
              " WHERE `monitor_special`.`name` = 'letv[cdn.brand]' " \
              "and `monitor_history`.`his_clock`=%d"%(week_ago)
        cur.execute(sql)
        # 获取数据
        da = 0
        sql_data = cur.fetchall()
        if len(sql_data) > 0:
            for row in sql_data:
                da = row[0] * 1.2

        if data[1] > da:
            info = "乐视宽带流量周环比大于20% 现值 "+str(data[1])+" 上周 "+str(da)
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
    brand = Net()
    insert_sql(brand.data)
    get_monitor(brand.data)
