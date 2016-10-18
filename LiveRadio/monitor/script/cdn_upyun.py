# coding:utf-8
import pymysql
from datetime import datetime, timedelta
import requests
# from monitor.models import History
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
        self.info = self.__GetUrl()
        self.data = self.__format(self.info)

    # 获取信息数据
    def __GetUrl(self):
        fifteen_Ago = (datetime.now() - timedelta(minutes=15)).strftime('%Y-%m-%d%H:%M:%S')
        ten_Ago = (datetime.now() - timedelta(minutes=10)).strftime('%Y-%m-%d%H:%M:%S')
        fifteen_Ago = fifteen_Ago[:10]+' '+fifteen_Ago[10:]
        ten_Ago = ten_Ago[:10]+' '+ten_Ago[10:]
        # url= 'https://console.upyun.com/uapi/v2/statistics/?start_time=%s&end_time=%s&flow_srouce=backsource' % (fifteen_Ago, ten_Ago)
        # print url
        url= 'https://console.upyun.com/uapi/v2/statistics/?start_time=%s&end_time=%s&isp=ctn' % (fifteen_Ago, ten_Ago)
        header = {
            'Authorization': 'Bearer b9968078-66b9-4475-bdbf-6ee9c1e2c4f4',
            }
        req = requests.get(url, headers=header)
        return json.loads(req.content)


    # 格式化信息数据，为了插入数据库
    def __format(self, info):
        if info is not None:
            st = 1
        else:
            st = 0
        band = info['data'][0]['bandwidth']/1024/1024
        timeStamp = info['data'][0]['time']
        bypass = 0
        return st,  band, bypass, timeStamp


def insert_sql(data):
    try:
        conn = pymysql.connect(host='localhost', port=3306, user=u, passwd=p, charset='UTF8', database=d)

        # conn = pymysql.connect(host=DATABASES['default']['HOST'], port=3306, user=DATABASES['default']['USER'], passwd=DATABASES['default']['PASSWORD'], charset='UTF8', database=DATABASES['default']['NAME'])
        # 获取一个游标对象
        cur = conn.cursor()
        # 插入数据  5:upyun[cdn.brand] 6:upyun[cdn.pass]
        sql1 = "INSERT INTO monitor_history (status,special_id,value,his_clock) VALUES (%d,%d,%f,%d)" % \
              (data[0],5,data[1], data[3])
        cur.execute(sql1)
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
              " WHERE `monitor_special`.`name` = 'upyun[cdn.brand]' " \
              "and `monitor_history`.`his_clock`=%d"%(week_ago)
        cur.execute(sql)
        # 获取数据
        da = 0
        sql_data = cur.fetchall()
        if len(sql_data) > 0:
            for row in sql_data:
                da = row[0] * 1.2
        if data[1] > da:
            info = "又拍宽带流量周环比大于20% 现值 "+str(data[1])+" 上周 "+str(da)
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

