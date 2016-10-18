# coding:utf-8
from datetime import datetime, timedelta
import hashlib
import requests
import json


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
        print url + "ok"
        r = requests.get(url)
        return json.loads(r.content)


    # 格式化信息数据，为了插入数据库
    def __format(self, info):
        st = info['status']
        chan = "'" + info['data'][0]['channel'] + "'"
        band = info['data'][0]['bandwidth'].values()[0]
        bp = info['data'][0]['bypass'].values()[0]
        tm = "'" + info['data'][0]['bandwidth'].keys()[0] + "'"
        return st, chan, band, bp, tm


if __name__ == '__main__':
    u = 'shiyun'
    api_key = r'uKKwKJrMAqUGyp9b7LABmQjsdZfXUGAn'
    api_pwd = r'pssQgvOH'
    channel = r'yf.v.tvxio.com'
    brand = Net(u, api_key, api_pwd, channel=channel)
    # print brand.info
    print brand.data
