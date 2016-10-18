# coding:utf-8
#!/usr/bin/env python
from monitor.package.mythread import task

import os
import sys
import time

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LiveRadio.settings")

    # 多线程监控

    # fd = open('count','r+')
    # count = fd.readline()
    # count = '1' if count == '0' else '2'
    # fd.write('2')
    # fd.close()
    # global child
    #
    # # 线程方法，可加入循环
    # def i(n):
    #     print n
    #
    # if count == '1':
    #     global child
    #     child = task(target=i(6),sleep=2)
    #     child.start()
    #     child.join(1)
        # child.stop()

    from django.core.management import execute_from_command_line


    execute_from_command_line(sys.argv)
    # thread1 = task(execute_from_command_line(sys.argv))
    # thread1.start()
    # thread1.join(1)
    # thread1.stop()
    #
    # child.stop()
    #
    # fd = open('count', 'w+')
    # fd.truncate()
    # fd.write('0')
    # fd.close()
