#!/usr/bin/python
# coding:utf-8
import json
import urllib2
from urllib2 import URLError
import sys, argparse


class zabbix_api:
    def __init__(self):
        self.url = 'http://192.168.2.65/api_jsonrpc.php'  # 修改URL
        self.header = {"Content-Type": "application/json"}

    def user_login(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": "Admin",  # 修改用户名
                "password": "zabbix"  # 修改密码
            },
            "id": 0
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "33[041m 用户认证失败，请检查 !33[0m", e.code
        else:
            response = json.loads(result.read())
            result.close()
            # print response['result']
            self.authID = response['result']
            return self.authID


    def host_get(self, hostName=''):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend",
                "filter": {"host": hostName}
            },
            "auth": self.user_login(),
            "id": 1
        })


        request = urllib2.Request(self.url, data)
        print "1"
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
            else:
                pass
        response = json.loads(result.read())
        print response
        result.close()
        print "主机数量: %s" % (len(response['result']))
        for host in response['result']:
            status = {"0": "OK", "1": "Disabled"}
            available = {"0": "Unknown", "1": "available", "2": "Unavailable"}
            # print host
            if len(hostName) == 0:
                print "HostID : %s HostName : %s  Status :%s Available :%s" % (
                host['hostid'], host['name'], status[host['status']], available[host['available']])
            else:
                print "HostID : %s HostName : %s  Status :%s Available :%s" % (
                host['hostid'], host['name'], status[host['status']], available[host['available']])
            return host['hostid']


    def hostgroup_get(self, hostgroupName=''):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "extend",
                "filter": {
                    "name": hostgroupName
                }
            },
            "auth": self.user_login(),
            "id": 1,
        })


        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            # print result.read()
            response = json.loads(result.read())
            result.close()
            # print response()
            for group in response['result']:
                if len(hostgroupName) == 0:
                    print "hostgroup: %s,tgroupid : %s" % (group['name'], group['groupid'])
                else:
                    print "hostgroup: %s,tgroupid : %s" % (group['name'], group['groupid'])
                    self.hostgroupID = group['groupid']
                    return group['groupid']


    def template_get(self, templateName=''):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": "extend",
                "filter": {
                    "name": templateName
                }
            },
            "auth": self.user_login(),
            "id": 1,
        })


        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
            # print response
            for template in response['result']:
                if len(templateName) == 0:
                    print "template : 33[31m%s33[0mt id : %s" % (template['name'], template['templateid'])
                else:
                    self.templateID = response['result'][0]['templateid']
                    print "Template Name : 33[31m%s33[0m " % templateName
                    return response['result'][0]['templateid']


    def hostgroup_create(self, hostgroupName):
        if self.hostgroup_get(hostgroupName):
            print "hostgroup 33[42m%s33[0m is exist !" % hostgroupName
            sys.exit(1)
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostgroup.create",
            "params": {
                "name": hostgroupName
            },
            "auth": self.user_login(),
            "id": 1
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
            print "33[042m 添加主机组:%s33[0m hostgroupID : %s" % (hostgroupName, response['result']['groupids'])


    def host_create(self, hostip, hostgroupName, templateName):
        if self.host_get(hostip):
            print "33[041m该主机已经添加!33[0m"
            sys.exit(1)
        group_list = []
        template_list = []
        for i in hostgroupName.split(','):
            var = {}
            var['groupid'] = self.hostgroup_get(i)
            group_list.append(var)
        for i in templateName.split(','):
            var = {}
            var['templateid'] = self.template_get(i)
            template_list.append(var)
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": hostip,
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": hostip,
                        "dns": "",
                        "port": "10050"
                    }
                ],
                "groups": group_list,
                "templates": template_list,
            },
            "auth": self.user_login(),
            "id": 1
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
            print "添加主机 : 33[42m%s31[0m tid :33[31m%s33[0m" % (hostip, response['result']['hostids'])


    def host_disable(self, hostip):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.update",
            "params": {
                "hostid": self.host_get(hostip),
                "status": 1
            },
            "auth": self.user_login(),
            "id": 1
        })


        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
            print '----主机现在状态------------'
            print self.host_get(hostip)


    def host_delete(self, hostid):
        hostid_list = []
        # print type(hostid)
        for i in hostid.split(','):
            var = {}
            var['hostid'] = self.host_get(i)
            hostid_list.append(var)
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.delete",
            "params": hostid_list,
            "auth": self.user_login(),
            "id": 1
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except Exception, e:
            print e
        else:
            result.close()
            print "主机 33[041m %s33[0m 已经删除 !" % hostid

if __name__ == "__main__":
    host = r'Zabbix server'
    zabbix = zabbix_api()
    zabbix.host_get(hostName=host)
    '''
    zabbix = zabbix_api()
    parser = argparse.ArgumentParser(description='zabbix api ', usage='%(prog)s [options]')
    parser.add_argument('-H', '--host', nargs='?', dest='listhost', default='host', help='查询主机')
    parser.add_argument('-G', '--group', nargs='?', dest='listgroup', default='group', help='查询主机组')
    parser.add_argument('-T', '--template', nargs='?', dest='listtemp', default='template', help='查询模板信息')
    parser.add_argument('-A', '--add-group', nargs=1, dest='addgroup', help='添加主机组')
    parser.add_argument('-C', '--add-host', dest='addhost', nargs=3,
                        metavar=('192.168.2.1', 'test01,test02', 'Template01,Template02'), help='添加主机,多个主机组或模板使用分号')
    parser.add_argument('-d', '--disable', dest='disablehost', nargs=1, metavar=('192.168.2.1'), help='禁用主机')
    parser.add_argument('-D', '--delete', dest='deletehost', nargs='+', metavar=('192.168.2.1'), help='删除主机,多个主机之间用分号')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    if len(sys.argv) == 1:
        print parser.print_help()
    else:
        args = parser.parse_args()
        if args.listhost != 'host':
            if args.listhost:
                zabbix.host_get(args.listhost)
            else:
                zabbix.host_get()
        if args.listgroup != 'group':
            if args.listgroup:
                zabbix.hostgroup_get(args.listgroup)
            else:
                zabbix.hostgroup_get()
        if args.listtemp != 'template':
            if args.listtemp:
                zabbix.template_get(args.listtemp)
            else:
                zabbix.template_get()
        if args.addgroup:
            zabbix.hostgroup_create(args.addgroup[0])
        if args.addhost:
            zabbix.host_create(args.addhost[0], args.addhost[1], args.addhost[2])
        if args.disablehost:
            zabbix.host_disable(args.disablehost)
        if args.deletehost:
            zabbix.host_delete(args.deletehost[0])
'''
'''    #!/usr/bin/python
    #新增帮助信息，可直接执行脚本
    zabbix=zabbix_api()
    #获取所有主机列表
    zabbix.host_get()
    #查询单个主机列表
    zabbix.host_get('192.168.2.1')
    #获取所有主机组列表
    zabbix.hostgroup_get()
    #查询单个主机组列表
    zabbix.hostgroup_get('test01')
    #获取所有模板列表
    zabbix.template_get()
    #查询单个模板信息
    zabbix.template_get('Template OS Linux')
    #添加一个主机组
    zabbix.hostgroup_create('test01')
    #添加一个主机，支持将主机添加进多个组，多个模板，多个组、模板之间用逗号隔开，如果添加的组不存在，新创建组
    zabbix.host_create('192.168.2.1', 'test01', 'Template OS Linux')
    zabbix.host_create('192.168.2.1', 'Linux servers,test01 ', 'Template OS Linux,Template App MySQL')
    #禁用一个主机
    zabbix.host_disable('192.168.2.1')
    #删除host,支持删除多个，之间用逗号
    zabbix.host_delete('192.168.2.1,192.168.2.2')
    '''
