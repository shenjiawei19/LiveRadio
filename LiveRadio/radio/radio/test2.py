#!/usr/bin/python
# coding:utf-8
import json
import urllib2
from urllib2 import URLError
import sys, argparse
from datetime import datetime,timedelta
from time import mktime,strftime,strptime,time

a = "2016-08-11 14:29:00"
b = mktime(strptime(a,"%Y-%m-%d %H:%M:%S"))
print b
print time()
aa = time()-7*24*3600
print aa
