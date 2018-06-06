#!/usr/bin/env python
# coding:utf-8
import cPickle
import json
import os
import re
import requests


class UserLogin:

    def __init__(self):
        with open("web_message.json", 'r') as load_f:
            load_dict = json.load(load_f, encoding='UTF-8')
            # print(load_dict)
            self.headers = load_dict['headers']
            self.index_url = load_dict['index_url']
            self.login_url = 'auth/login/password:self/'

        with open("../user_message.txt", 'r') as load_f:
            load_dict = json.load(load_f, encoding='UTF-8')
            self.username = load_dict['username']
            self.password = load_dict['password']

    def get_csrf(self, session):
        '''动态参数:_csrf'''
        index_page = session.get(self.index_url, headers=self.headers)
        html = index_page.content

        # print 'html -------------------------'
        # print html
        # print 'html -------------------------\n'

        pattern = r'"current":"(.*?)"'
        _csrf = re.findall(pattern, html)

        # print '_csrf -------------------------'
        # print _csrf[0]
        # print '_csrf -------------------------\n'

        return _csrf[0]

    def save_session(self, session):
        with open('./cookies/cookies.txt', 'wb') as f:
            cPickle.dump(session.cookies.get_dict(), f)

            print 'cookies writen：cookies.txt'

    def load_session(self):
        with open('./cookies/cookies.txt', 'rb') as f:
            cookies = cPickle.load(f)
        return cookies

    def use_cookies_login(self):
        session = requests.session()
        login_page = session.get(self.index_url, headers=self.headers, cookies=self.load_session())
        login_content = login_page.content

        pattern = r'Login to Phabricator'
        isLogin = re.findall(pattern, login_content)
        for isLogin1 in isLogin:
            print 'isLogin1 : ' + isLogin1
        if not isLogin:
            print login_content
            print "cookies Login Success"
        else:
            self.usr_account_pass_login()

    def usr_account_pass_login(self):
        session = requests.session()
        _csrf = self.get_csrf(session)

        postdata = {
            '__csrf__': _csrf,
            '__form__': '1',
            '__dialog__': '1',
            'username': self.username,
            'password': self.password
        }
        # print self.index_url
        # print self.login_url
        post_url = bytes(self.index_url) + bytes(self.login_url)
        login_page = session.post(post_url, data=postdata, headers=self.headers)
        login_content = login_page.content

        pattern = r'Login to Phabricator'
        isLogin = re.findall(pattern, login_content)
        for isLogin1 in isLogin:
            print 'isLogin1 : ' + isLogin1
        if not isLogin:
            self.save_session(session)
            print login_content
            print "Login Success"
        else:
            self.save_session(session)
            login_content = login_page.content

            print login_content
            print 'Login Failed'
            exit(0)

    def start_login(self):
        if os.path.exists('./cookies/cookies.txt'):
            self.use_cookies_login()
        else:
            self.usr_account_pass_login()
