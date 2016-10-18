# coding:utf-8
#!/usr/bin/env python
import os
import pymysql
pymysql.install_as_MySQLdb()


# class Singleton(object):
#     def __new__(cls, *args, **kwargs):
#         if not hasattr(cls, '_instance'):
#             orig = super(Singleton, cls)
#             cls._instance = orig.__new__(cls, *args, **kwargs)
#         return cls._instance
#
#
# class MyClass(Singleton):
#     a = 1
#
# print os.getcwd()
#
# count = open('/home/shenjiawei/projects/LiveRadiocount','r+').readline()
# print count
