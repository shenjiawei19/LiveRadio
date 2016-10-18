# coding:utf-8

import time

# 得到时间类型数据获取月范围到时间撮
def month_range(date):
    month = date.replace('-','').replace(':','').replace(' ','')[:6]
    timeArray2 = time.strptime(month, "%Y%m")
    timeStamp2 = int(time.mktime(timeArray2))
    timeArray3 = time.strptime(str(int(month)+1), "%Y%m")
    timeStamp3 = int(time.mktime(timeArray3))
    return timeStamp2, timeStamp3

# 得到时间撮数据获取月范围到时间撮
def month_rang(timeStamp):
    timeStamp = float(timeStamp)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y%m", timeArray)
    timeArray2 = time.strptime(otherStyleTime, "%Y%m")
    timeStamp2 = int(time.mktime(timeArray2))
    timeArray3 = time.strptime(str(int(otherStyleTime)+1), "%Y%m")
    timeStamp3 = int(time.mktime(timeArray3))
    return timeStamp2, timeStamp3

# 得到时间类型数据获取月范围到时间撮
def day_range(date):
    day = date.replace('-','').replace(':','').replace(' ','')[:8]
    timeArray2 = time.strptime(day, "%Y%m%d")
    timeStamp2 = int(time.mktime(timeArray2))
    timeArray3 = time.strptime(str(int(day)+1), "%Y%m%d")
    timeStamp3 = int(time.mktime(timeArray3))
    return timeStamp2, timeStamp3

# 得到时间撮数据获取月范围到时间撮
def day_rang(timeStamp):
    timeStamp = float(timeStamp)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y%m%d", timeArray)
    timeArray2 = time.strptime(otherStyleTime, "%Y%m%d")
    timeStamp2 = int(time.mktime(timeArray2))
    timeArray3 = time.strptime(str(int(otherStyleTime)+1), "%Y%m%d")
    timeStamp3 = int(time.mktime(timeArray3))
    return timeStamp2, timeStamp3

if __name__ == '__main__':
    date = "2016-09-11"
    # month_range(date)
    day_range(date)
    date2 = '1472659222'
    month_rang(date2)