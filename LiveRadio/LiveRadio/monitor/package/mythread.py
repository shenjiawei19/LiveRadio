# coding:utf-8
#!/usr/bin/env python

import time, threading

class task(threading.Thread):
    def __init__(self,target=None,*args,**kwargs):
        threading.Thread.__init__(self,target=target)
        self.live = True
        self.sleep = kwargs.get('sleep',1)
        self.__target = target
        self.__args = args
        self.__kwargs = kwargs

    def run(self):
        # try:
        while self.live:
            print 2
            if self.__target:
                self.__target(*self.__args, **self.__kwargs)
            print 3
            time.sleep(self.sleep)
        # finally:
        #     del self.__target, self.__args, self.__kwargs
        exit()

    def stop(self):
        self.live = False


def test(test):
    for ip in test:
        thread1 = task(ip)
        thread1.start()
        thread1.join(1)
        thread1.stop()


if __name__ == '__main__':
    eachline = ['1.1.1.1', '222.73.5.54']
    test(eachline)


