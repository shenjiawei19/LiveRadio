# coding:utf-8
import os


def cdn_flow(user,password,ip,port):
    cmd = 'snmpwalk -v2c -c '+user+'@'+password+' '+ip+' IF-MIB::'+port
    a =  os.popen(cmd).readlines()
    a = ['IF-MIB::ifHCOutOctets.35 = Counter64: 2767458230040199\n']
    f = a[0].split(':')
    item = f[2].split('=')[0].strip(' ')
    print item
    result = f[3].strip(' ')
    print result

if __name__ == '__main__':
    a = ['IF-MIB::ifHCOutOctets.35 = Counter64: 2767458230040199\n']
    f = a[0].split(':')
    print f
    item = f[2].split('=')[0].strip(' ')
    print item
    result = f[3].strip(' ')
    print result
    # fd = open('flow_info.txt','r+')
    # for line in fd:
    #     info =line.split(':')
    #     ip = info[0]
    #     port = info[1]
    #     cdn_flow(ip=ip,port=port)