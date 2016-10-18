# coding:utf-8
import pymysql
from datetime import datetime, timedelta
import requests
# from monitor.models import History
import json
import socket

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
        self.info = self.__GetUrl()
        self.data = self.__format(self.info)

    # 获取信息数据
    def __GetUrl(self):
        fifteen_Ago = (datetime.now() - timedelta(minutes=15)).strftime('%Y-%m-%d%H:%M:%S')
        ten_Ago = (datetime.now() - timedelta(minutes=10)).strftime('%Y-%m-%d%H:%M:%S')
        fifteen_Ago = fifteen_Ago[:10]+' '+fifteen_Ago[10:]
        ten_Ago = ten_Ago[:10]+' '+ten_Ago[10:]

        url = 'https://api.upyun.com/flow/common_data/?start_time=%s&end_time=%s&flow_source=backsource' % (fifteen_Ago, ten_Ago)
        header = {
            'Authorization': 'Bearer b9968078-66b9-4475-bdbf-6ee9c1e2c4f4',
            }
        req = requests.get(url, headers=header)
        print json.loads(req.content)
        return json.loads(req.content)


    # 格式化信息数据，为了插入数据库
    def __format(self, info):
        if info is not None:
            st = 1
        else:
            st = 0
        bypass = round(info[0]['bytes']*8.0/1024/1024/300,2)
        timeStamp = info[0]['kt']
        return st, bypass, timeStamp


def insert_sql(data):
    try:
        conn = pymysql.connect(host='localhost', port=3306, user=u, passwd=p, charset='UTF8', database=d)
        # 获取一个游标对象
        cur = conn.cursor()
        print "123"
        print (data[0],6,data[1], data[2])
        # 插入数据  5:upyun[cdn.brand] 6:upyun[cdn.pass]
        sql2 = "INSERT INTO monitor_history (status,special_id,value,his_clock) VALUES (%d,%d,%f,%d)" % \
              (data[0],6,data[1], data[2])
        cur.execute(sql2)
        conn.commit()
        cur.close()
        conn.close()
        print "23"
    except Exception as e:
        print e

def get_monitor(data):
    try:
        conn = pymysql.connect(host='localhost', port=3306, user=u, passwd=p, charset='UTF8', database=d)
        # 获取一个游标对象
        cur = conn.cursor()
        print "33"
        week_ago = int(data[2])-604800
        # 查询数据
        sql = "SELECT `monitor_history`.`value`, `monitor_history`.`his_clock` " \
              "FROM `monitor_history` INNER JOIN `monitor_special` " \
              "ON (`monitor_history`.`special_id` = `monitor_special`.`id`)" \
              " WHERE `monitor_special`.`name` = 'upyun[cdn.pass]'" \
              "and `monitor_history`.`his_clock`=%d"%(week_ago)
        print sql
        cur.execute(sql)
        print "2"
        # 获取数据
        da = 0
        sql_data = cur.fetchall()
        if len(sql_data) > 0:
            for row in sql_data:
                print row
                da = row[0] * 0.5
        if data[1] < da:
            info = "又拍流量周环比小于50% 现值 "+str(data[1])+" 上周 "+str(da)
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
    # upyun[cdn.brand],upyun[cdn.pass]
    brand = Net()
    insert_sql(brand.data)
    get_monitor(brand.data)