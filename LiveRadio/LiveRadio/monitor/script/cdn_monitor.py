# coding:utf-8
import os
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import  socket

hostName = socket.gethostname()
if hostName == r'shenjiawei-Rev-1-0':
    u = 'root'
    p = 'root'
    d = 'LiveRadio'
elif hostName == r'ssf-test.m.ismartv.cn':
    u = 'ssf'
    p = '123456'
    d = 'LiveRadio'

def send_mail(a):
    from_addr = "shenjiawei@ismartv.cn"
    password = "!QAZ2wsx"
    to_addr = "op@ismartv.cn"
    smtp_server = "smtp.qiye.163.com"
    msg = MIMEText(str(a), 'plain', 'utf-8')

    msg['From'] = _format_addr(u'shenjiawei@ismartv.cn <%s>' % from_addr)
    msg['To'] = _format_addr(u'op@ismartv.cn <%s>' % to_addr)
    msg['Subject'] = Header(u'商用CDN告警', 'utf-8').encode()

    server = smtplib.SMTP()
    server.connect(smtp_server)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


if __name__ == '__main__':
    size = os.path.getsize('monitor.txt')
    if size > 50:
        tt = open('monitor.txt', 'rw+')
        send_mail(tt.read())
        tt.writelines('')
        tt.close()



