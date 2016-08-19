#!/usr/bin/python
# coding:utf-8
import requests
import json
from time import time
import urllib2
from urllib2 import URLError
import sys, argparse


class zabbix_api:
    def __init__(self):
        self.url = 'http://192.168.2.65/api_jsonrpc.php'  # 修改URL
        self.header = {"Content-Type": "application/json"}


    def user_login(self,username,passwd):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": username,  # 修改用户名
                "password": passwd  # 修改密码
            },
            "id": 0
        })
        r = requests.get(self.url, headers=self.header, data=data)
        result = json.loads(r.content)
        self.authID = result['result']
        return self.authID


    def host_get(self, hostName='',username='',passwd=''):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend",
                "filter": {"host": hostName}
            },
            "auth": self.user_login(username,passwd),
            "id": 1
        })
        r = requests.get(self.url,headers=self.header,data=data)
        con = eval(r.content)
        print con

        for host in con['result']:
            status = {"0": "OK", "1": "Disabled"}
            available = {"0": "Unknown", "1": "available", "2": "Unavailable"}
            if len(hostName) == 0:
                print "HostID : %s HostName : %s  Status :%s Available :%s" % (
                    host['hostid'], host['name'], status[host['status']], available[host['available']])
            else:
                print "HostID : %s HostName : %s  Status :%s Available :%s" % (
                    host['hostid'], host['name'], status[host['status']], available[host['available']])
                self.host = host['hostid']
            return host['hostid']

    def items_get(self,key):
        if not self.authID:
            self.user_login()
        else:
            data = json.dumps({
                "jsonrpc": "2.0",
                "method": "item.get",
                "params": {
                    "output": "extend",
                    "hostids": self.host,
                    "search": {
                        "key_": key,
                    },

                },
                "auth": self.authID,
                "id": 1
                })
            r = requests.get(self.url,headers=self.header,data=data)
            con = json.loads(r.content)
            print "123"
            print con
            print con['result'][0]['lastvalue']
            self.itemid = con['result'][0]['itemid']

            return self.itemid

    def history_get(self,key):

        start = time()-1*24*3600
        over = time()-1*24*3600+70
        if not self.authID:
            self.user_login()
        else:
            data = json.dumps({
                "jsonrpc": "2.0",
                "method": "history.get",
                "params": {
                    "output": "extend",
                    "history": 0,
                    "time_from": start,
                    "time_till": over,
                    "itemids": self.items_get(key),
                    "sortfield": "clock",
                    "sortorder": "DESC",
                    # "limit": 10
                },
                "auth": self.authID,
                "id": 1
                })
        r = requests.get(self.url, headers=self.header, data=data)
        con = json.loads(r.content)
        print con['result']
        print "11"
        for n,c in enumerate(con['result']):
            print n,c

if __name__=='__main__':
    host = r'Zabbix server'
    key = "system.cpu.util[,idle]"
    username = 'Admin'
    passwd = 'zabbix'
    zabbix = zabbix_api()
    zabbix.host_get(hostName=host,username=username,passwd=passwd)
    zabbix.history_get(key)

