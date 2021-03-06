# -*- coding: utf-8 -*-
import requests
from HTMLParser import HTMLParser

import pdb
class DoubanClient(object):
    def __init__(self):
        object.__init__(self)
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36',
        #            'origin': 'http://www.douban.com'}
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
                   'origin' : 'http://www.dell.com'}
        self.session = requests.session()
        self.session.headers.update(headers)


    def login(self, username, password,
              source='index_nav',
              redir='http://www.dell.com/',
              login='登录'):
        url = 'https://www.dell.com/Identity/global/Login/'
        data = {'EmailAddress': username,
                'Password': password,
                'source': source,
                'redir': redir,
                'login': login}
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
                   'Host' : 'http://www.dell.com'}
        # r =  requests.get(url, data=data, headers=headers)
        r = requests.post(url, data=data, headers=headers)

        print r.content
        self.session.post(url, data=data, headers=headers)
        print(self.session.cookies.items())

    def edit_signature(self, username, signature):
        url = 'https://www.douban.com/people/%s/' % username
        r = self.session.get(url)
        data = {'ck': _get_ck(r.content), 'signature': signature}
        url = 'https://www.douban.com/j/people/%s/edit_signature' % username
        headers = {'referer': url,#可以去除
                   'host': 'www.douban.com',
                   'x-requested-with': 'XMLHttpRequest'}
        r = self.session.post(url, data=data, headers=headers)
        print(r.content)


def _attr(attrs, attrname):
    for attr in attrs:
        print attr
        if attr[0] == attrname:
            return attr[1]
    return None


def _get_captcha(content):

    class CaptchaParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.captcha_id = None
            self.captcha_url = None

        def handle_starttag(self, tag, attrs):
            if tag == 'img' and _attr(attrs, 'id') == 'captcha_image' and _attr(attrs, 'class') == 'captcha_image':
                self.captcha_url = _attr(attrs, 'src')

            if tag == 'input' and _attr(attrs, 'type') == 'hidden' and _attr(attrs, 'name') == 'captcha-id':
                self.captcha_id = _attr(attrs, 'value')

    p = CaptchaParser()
    p.feed(content)
    return p.captcha_id, p.captcha_url


def _get_ck(content):

    class CKParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.ck = None

        def handle_starttag(self, tag, attrs):
            if tag == 'input' and _attr(attrs, 'type') == 'hidden' and _attr(attrs, 'name') == 'ck':
                self.ck = _attr(attrs, 'value')

    p = CKParser()
    p.feed(content)
    return p.ck


if __name__ == '__main__':
    c = DoubanClient()
    c.login('shenjiawei19@sina.com', '!QAZ2wsx')
    # c.edit_signature('55819042', 'python 123213爬虫基础')
