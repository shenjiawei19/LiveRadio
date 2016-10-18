# coding:utf-8
import pymysql
import os
import time
import  socket
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


hostName = socket.gethostname()
if hostName == r'shenjiawei-Rev-1-0':
    u = 'root'
    p = 'root'
    d = 'LiveRadio'
elif hostName == r'ssf-test.m.ismartv.cn':
    u = 'ssf'
    p = '123456'
    d = 'LiveRadio'

# 获取监控服务项
def get_service():
    result = []
    try:
        conn = pymysql.connect(host='localhost', port=3306, user=u, passwd=p, charset='UTF8', database=d)

        # 获取一个游标对象
        cur = conn.cursor()
        # "select ms.plugin, mi.id ,mi.host_id from monitor_service ms,monitor_service_items msi,monitor_item mi where ms.id=msi.service_id and mi.id=msi.item_id;"
        sql = "select ms.plugin, mi.id ,mi.host_id " \
              "from monitor_service ms,monitor_service_items msi,monitor_item mi " \
              "where ms.id=msi.service_id and mi.id=msi.item_id"
        cur.execute(sql)
        sql_data = cur.fetchall()
        if len(sql_data) > 0:
            for row in sql_data:
                result.append(list(row))
        cur.close()
        conn.close()
    except Exception as e:
        result = []
        print e
    return result


def insert_sql(value,time,item,host):
    try:
        conn = pymysql.connect(host='localhost', port=3306, user=u, passwd=p, charset='UTF8', database=d)
        # 获取一个游标对象
        cur = conn.cursor()
        sql1 ="select value,his_clock,add_value from monitor_history where hosts_id=%d and items_id=%d order by his_clock desc limit 1;"%(host,item)
        cur.execute(sql1)
        sql_data = cur.fetchall()
        add = interval = 0
        stat =1
        if len(sql_data) > 0:
            result = 0
            for row in sql_data:
                result = row
            if result[0] and result[1]:
                monitor = add = int(value) - int(result[0])
                interval = time - int(result[1])
            else:
                monitor = add = int(result[2])
                value = int(result[0])+int(result[2])
                interval = 300
                stat = 0
            if add <= 0:
                add = int(result[2])
                value = int(result[0]) + int(result[2])
                interval = 300
                stat = 0
        # 插入数据  5:upyun[cdn.brand] 6:upyun[cdn.pass]
        sql2 = "INSERT INTO monitor_history (status,items_id,hosts_id,value,his_clock,add_value,interval_time) " \
               "VALUES (%d,%d,%d,%f,%d,%d,%d)" % \
              (stat,item,host,int(value),time,add,interval)
        cur.execute(sql2)
        conn.commit()
        # 告警
        fd = open('flow.txt', 'a+')
        if monitor <= 0:
            sql3 = "select name from monitor_item where id=%d;" % (item)
            cur.execute(sql3)
            sql_data = cur.fetchall()
            if len(sql_data) > 0:
                for row in sql_data:
                    info = str(row[0])+'宽带异常'
                    fd.writelines(info + '\n')
        fd.write(" ")
        fd.close()
        cur.close()
        conn.close()

    except Exception as e:
        print e


# 执行系统命令
def do_syscmd(cmd):
    for c in cmd:
        a =  os.popen(c[0]).readlines()
        # a = ['IF-MIB::ifHCOutOctets.35 = Counter64: 2767458230060199\n']
        try:
            f = a[0].split(':')
            result = f[3].strip(' ').strip('\n')
            c.append(result)
        except :
            result = 0
            c.append(result)
    return cmd


def send_mail(a):
    from_addr = "shenjiawei@ismartv.cn"
    password = "!QAZ2wsx"
    to_addr = "op@ismartv.cn"
    smtp_server = "smtp.qiye.163.com"
    msg = MIMEText(str(a), 'plain', 'utf-8')

    msg['From'] = _format_addr(u'shenjiawei@ismartv.cn <%s>' % from_addr)
    msg['To'] = _format_addr(u'op@ismartv.cn <%s>' % to_addr)
    msg['Subject'] = Header(u'宽带告警', 'utf-8').encode()

    server = smtplib.SMTP()
    server.connect(smtp_server)
    server.set_debuglevel(0)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

if __name__ == '__main__':
    result = get_service()
    value = do_syscmd(result)
    time = time.time()
    if int(str(int(time)/10)[-1:])>=5:
        d_time = (int(time) / 100 + 1) * 100
    else:
        d_time = (int(time) / 100 ) * 100
    for v in value:
        insert_sql(v[3],d_time,v[1],v[2])
    size = os.path.getsize('flow.txt')
    tt = open('flow.txt', 'r+')
    print size
    if size > 50:
        send_mail(tt.read())
    tt.close()
    os.remove('flow.txt')