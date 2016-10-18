# coding:utf-8
import matplotlib.pyplot as plt
import pymysql
from datetime import datetime, timedelta
import hashlib
import requests
import pylab

class Net(object):
    def __init__(self, name, key, pwd, channel):

        self.m = hashlib.md5()
        import time
        self.p = (time.strftime("%Y%m%d", time.localtime(time.time()))+name+key+pwd)
        self.info = self.__GetUrl(channel)
        self.data = self.__format(self.info)

    # 获取信息数据
    def __GetUrl(self, channel):
        self.m.update(self.p)
        passwd = self.m.hexdigest()

        five_ago = str(datetime.now() + timedelta(minutes=-5))
        five_ago = five_ago[0:10]+five_ago[11:16]
        url = r'http://console.yunfancdn.com/api/cdn.php?u=shiyun&p='+str(passwd)+'&starttime='+five_ago+'&channel='+channel+'&backsource=1'

        r = requests.get(url)
        return eval(r.content)

    # 格式化信息数据，为了插入数据库
    def __format(self,info):
        st = info['status']
        chan = "'"+info['data'][0]['channel']+"'"
        band = info['data'][0]['bandwidth'].values()[0]
        bp = info['data'][0]['bypass'].values()[0]
        tm = "'"+info['data'][0]['bandwidth'].keys()[0]+"'"
        return st, chan, band, bp, tm

def insert_sql(data):
    try:
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', charset='UTF8', database='ismartv_cdn')
        # 获取一个游标对象
        cur = conn.cursor()
        # 插入数据 1、id 2、status 3、channel 4、bandwidth 5、bypass 6、time
        sql = "INSERT INTO cdn_monitor (status,channel,bandwidth,bypass,TIME) VALUES (%d,%s,%f,%f,%s)" % \
              (data[0], data[1], data[2], data[3], data[4])
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print e

def get_sql():
    date = []
    brand_list = []
    bypass_list = []
    try:
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', charset='UTF8', database='ismartv_cdn')
        # 获取一个游标对象
        cur = conn.cursor()
        # 查询数据
        cur.execute("SELECT bandwidth,bypass, TIME FROM cdn_monitor where channel='yf.v.tvxio.com' order by time DESC limit 10")
        # 获取数据
        data = cur.fetchall()
        from datetime import datetime
        for row in data:
            brand_list.append(row[0])
            bypass_list.append(row[1])
            date.append(row[2])
    except Exception as e:
        print e
    print brand_list
    print date
    plt.plot_date(pylab.date2num(date), brand_list, linestyle='-')
    plt.ylabel(u'values')
    plt.xlabel(u'time')
    plt.title(u'brandwith')
    plt.savefig('brandwith.png', format='png')
    plt.close()
    plt.plot_date(pylab.date2num(date), bypass_list, linestyle='-')
    plt.ylabel(u'values')
    plt.xlabel(u'time')
    plt.title(u'bypass')
    plt.savefig('bypass.png', format='png')
    plt.close()


if __name__ == '__main__':
    u = 'shiyun'
    api_key = r'uKKwKJrMAqUGyp9b7LABmQjsdZfXUGAn'
    api_pwd = r'pssQgvOH'
    channel = r'yf.v.tvxio.com'
    brand = Net(u, api_key, api_pwd, channel)
    insert_sql(brand.data)
    get_sql()

