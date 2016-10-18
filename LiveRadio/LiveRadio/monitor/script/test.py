# !/usr/bin/env python
# encoding=utf-8


import urllib2
import json
import datetime
import hashlib

#
ToDay = datetime.datetime.now().strftime('%Y%m%d')

#Ò»ÌìÇ°

OneDayAgo = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime('%Y-%m-%d')

print OneDayAgo
a = '2016-10-01'
B_Day = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime('%Y%m%d')

# 又拍
def VodTraffic_Upyun():
    print "you"
    print "start"+str(a)
    print "end"+str(OneDayAgo)
    Url='https://console.upyun.com/uapi/v2/statistics/?bucket_name=shiyun-vod&domain=upyun.v.tvxio.com&start_time=%s 00:00:00&end_time=%s 23:59:59' % (a,OneDayAgo)

    Req=urllib2.Request(Url)
    Req.add_header('Authorization','Bearer b9968078-66b9-4475-bdbf-6ee9c1e2c4f4')

    Data = urllib2.urlopen(Req).read()
    ValJson = json.loads(Data)

    LiuLiang=0
    for k in ValJson['data']:
        LiuLiang = LiuLiang + k['bytes']
    LiuLiang=int(LiuLiang)/1024/1024/1024
    print "又拍"+str(LiuLiang)
    return LiuLiang

# 云帆
def VodTraffic_YunFan():
    s = "%s 00:00" % OneDayAgo
    e = "%s 23:59" % OneDayAgo
    str_md5 = "%sshiyunuKKwKJrMAqUGyp9b7LABmQjsdZfXUGAnpssQgvOH" % ToDay
    m1 = hashlib.md5()
    m1.update(str_md5)
    p = m1.hexdigest()
    print "s"+str(s)
    url = 'http://console.yunfancdn.com/api/cdn.php?u=shiyun&p=%s&starttime=%s&endtime=%s&channel=yf.v.tvxio.com' % (p,s,e)
    req = urllib2.Request(url)
    Da = urllib2.urlopen(req).read()
    Da_Js = json.loads(Da)
    Da_day = Da_Js['data'][0]['bandwidth'].values()
    Da_G = sum(Da_day)*300/8/1024
    print "云帆"+str(Da_G)
    return Da_G

# 乐视
def VodTraffic_Letv():
    #乐视°
    FourDayAgo = (datetime.datetime.now() - datetime.timedelta(days = 4)).strftime('%Y%m%d')
    print FourDayAgo
    url='http://api.open.letvcloud.com/data/traffic?productline=CDN&domaintype=VOD&startday=%s&endday=%s&granularity=day&unit=G' % (FourDayAgo,B_Day)
    hds = { 'Authorization': 'Basic  ODA4OTI2OjNhYjVhZTkzMGIwNTkxODBkMTNjZjQzZTlhOTQ2ZmQy',
            'Lecloud-api-version' : '0.4',
            'Accept' : 'application/json'
          }
    req = urllib2.Request(url,headers=hds)
    response = urllib2.urlopen(req)
    da_letv = response.read()
    res_json = json.loads(da_letv)
    res_json_last = res_json['data']['traffic']['valuelist'][-1]
    print "乐视"+str(res_json_last)
    return res_json_last


if __name__ == '__main__':
    VodTraffic_Upyun()
    VodTraffic_YunFan()
    VodTraffic_Letv()