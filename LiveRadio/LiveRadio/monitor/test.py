# coding:utf-8

import time
import threading

# (1472659200, 1475251200)

conn = {}
conn.setdefault('AUTOCOMMIT', True)
print conn

dict = {"a" : "apple", "b" : "banana"}
print dict
dict2 = {"c" : "grape", "d" : "orange"}
dict.update(dict2)
print dict

