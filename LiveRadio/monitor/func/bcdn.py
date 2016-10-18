# !/usr/bin/env python
# encoding=utf-8

import urllib2
import json
import datetime
import hashlib

#
ToDay = datetime.datetime.now().strftime('%Y%m%d')


OneDayAgo = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime('%Y-%m-%d')

print OneDayAgo
B_Day = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime('%Y%m%d')

# 又拍
def count_up(first,last):
    LiuLiang=0
    a = '{0}-{1}-{2}'.format(first[0:4],first[4:6],first[6:8])
    OneDayAgo = '{0}-{1}-{2}'.format(last[0:4],last[4:6],last[6:8])
    Url='https://console.upyun.com/uapi/v2/statistics/?bucket_name=shiyun-vod&domain=upyun.v.tvxio.com&start_time=%s 00:00:00&end_time=%s 00:00:00' % (a,OneDayAgo)
    Req=urllib2.Request(Url)
    Req.add_header('Authorization','Bearer b9968078-66b9-4475-bdbf-6ee9c1e2c4f4')

    Data = urllib2.urlopen(Req).read()
    ValJson = json.loads(Data)


    for k in ValJson['data']:
        LiuLiang = LiuLiang + k['bytes']

    # Url='https://console.upyun.com/uapi/v2/statistics/?bucket_name=ne-shiyun-vod&domain=upyun.v.tvxio.com&start_time=%s 00:00:00&end_time=%s 00:00:00' % (a,OneDayAgo)
    Url='https://api.upyun.com/flow/common_data/?bucket_name=ne-shiyun-vod&domain=upyun.v.tvxio.com&start_time=%s 00:00:00&end_time=%s 00:00:00' % (a,OneDayAgo)


    print Url
    Req=urllib2.Request(Url)
    Req.add_header('Authorization','Bearer b9968078-66b9-4475-bdbf-6ee9c1e2c4f4')

    Data = urllib2.urlopen(Req).read()
    ValJson = json.loads(Data)
    print ValJson
    for k in ValJson['data']:
        LiuLiang = LiuLiang + k['bytes']

    LiuLiang=int(LiuLiang)/1024/1024/1024
    return LiuLiang

# 又拍
def count_up(first,last,vod=True):
    LiuLiang=0
    all=0
    a = '{0}-{1}-{2}'.format(first[0:4],first[4:6],first[6:8])
    OneDayAgo = '{0}-{1}-{2}'.format(last[0:4],last[4:6],last[6:8])
    Url='https://console.upyun.com/uapi/v2/statistics/?bucket_name=shiyun-vod&domain=upyun.v.tvxio.com&start_time=%s 00:00:00&end_time=%s 00:00:00' % (a,OneDayAgo)
    Req=urllib2.Request(Url)
    Req.add_header('Authorization','Bearer b9968078-66b9-4475-bdbf-6ee9c1e2c4f4')

    Data = urllib2.urlopen(Req).read()
    ValJson = json.loads(Data)


    for k in ValJson['data']:
        LiuLiang = LiuLiang + k['bytes']
    Url='https://console.upyun.com/uapi/v2/statistics/?bucket_name=ne-shiyun-vod&domain=ne-upyun.v.tvxio.com&start_time=%s 00:00:00&end_time=%s 00:00:00' % (a,OneDayAgo)
    Req=urllib2.Request(Url)
    Req.add_header('Authorization','Bearer b9968078-66b9-4475-bdbf-6ee9c1e2c4f4')

    Data = urllib2.urlopen(Req).read()
    ValJson = json.loads(Data)
    for k in ValJson['data']:
        LiuLiang = LiuLiang + k['bytes']
    LiuLiang=int(LiuLiang)/1024/1024/1024

    Url='https://console.upyun.com/uapi/v2/statistics/?start_time=%s 00:00:00&end_time=%s 00:00:00' % (a,OneDayAgo)
    Req=urllib2.Request(Url)
    Req.add_header('Authorization','Bearer b9968078-66b9-4475-bdbf-6ee9c1e2c4f4')

    Data = urllib2.urlopen(Req).read()
    ValJson = json.loads(Data)
    for k in ValJson['data']:
        all = all + k['bytes']
    all=int(all)/1024/1024/1024
    if vod:
        return LiuLiang
    else:
        return all-LiuLiang

# 云帆
def count_yun(first,last):
    s = "%s 00:00" % first
    e = "%s 00:00" % last
    str_md5 = "%sshiyunuKKwKJrMAqUGyp9b7LABmQjsdZfXUGAnpssQgvOH" % datetime.datetime.now().strftime('%Y%m%d')
    m1 = hashlib.md5()
    m1.update(str_md5)
    p = m1.hexdigest()
    url = 'http://console.yunfancdn.com/api/cdn.php?u=shiyun&p=%s&starttime=%s&endtime=%s&channel=yf.v.tvxio.com' % (p,s,e)
    req = urllib2.Request(url)
    Da = urllib2.urlopen(req).read()
    Da_Js = json.loads(Da)
    Da_day = Da_Js['data'][0]['bandwidth'].values()
    Da_G = sum(Da_day)*300/8/1024
    return Da_G

# 乐视
def count_letv(first,last):
    #乐视°
    FourDayAgo = (datetime.datetime.now() - datetime.timedelta(days = 4)).strftime('%Y%m%d')
    url='http://api.open.letvcloud.com/data/traffic?productline=CDN&domaintype=VOD&startday=%s&endday=%s&granularity=day&unit=G' % (first,last)
    hds = { 'Authorization': 'Basic  ODA4OTI2OjNhYjVhZTkzMGIwNTkxODBkMTNjZjQzZTlhOTQ2ZmQy',
            'Lecloud-api-version' : '0.4',
            'Accept' : 'application/json'
          }
    req = urllib2.Request(url,headers=hds)
    response = urllib2.urlopen(req)
    da_letv = response.read()
    res_json = json.loads(da_letv)
    res_json_last = res_json['data']['traffic']['valuelist'][-1]
    return res_json_last


if __name__ == '__main__':
    print "1"
    # VodTraffic_Upyun()
    # VodTraffic_YunFan()
    # VodTraffic_Letv()