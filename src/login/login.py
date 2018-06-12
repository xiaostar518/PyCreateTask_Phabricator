#!/usr/bin/env python
# coding:utf-8
import cPickle
import json
import os
import re
import requests
import sys

path_history = "./history_file/"


class UserLogin:

    def __init__(self):
        with open("./web_files/web_message.json", 'r') as load_f:
            load_dict = json.load(load_f, encoding='UTF-8')
            # print(load_dict)
            self.headers = load_dict['headers']
            self.index_url = load_dict['index_url']
            self.login_url = 'auth/login/password:self/'

        with open("./user_message.txt", 'r') as load_f:
            load_dict = json.load(load_f, encoding='UTF-8')
            self.username = load_dict['username']
            self.password = load_dict['password']

    def get_csrf(self, session):
        '''动态参数:_csrf'''
        try:
            index_page = session.get(self.index_url, headers=self.headers)
        except Exception, e:
            print 'The website is wrong. Please check your setting for web.'
            print 'Error message : ', e
            sys.exit(0)
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

    def delete_cookies(self):
        if os.path.exists(path_history + 'cookies.txt'):
            os.remove(path_history + 'cookies.txt')

    def save_last_account(self, account):
        with open(path_history + 'account.txt', 'wb') as f:
            cPickle.dump(account, f)

            print 'current_account writen: account.txt'

    def load_last_account(self):
        if os.path.exists(path_history + 'account.txt'):
            with open(path_history + 'account.txt', 'rb') as f:
                account = cPickle.load(f)
            return account
        else:
            return False

    def save_session(self, session):
        with open(path_history + 'cookies.txt', 'wb') as f:
            cPickle.dump(session.cookies.get_dict(), f)

            print 'cookies writen: cookies.txt'

    def load_session(self):
        with open(path_history + 'cookies.txt', 'rb') as f:
            cookies = cPickle.load(f)
        return cookies

    def use_cookies_login(self):
        session = requests.session()
        try:
            login_page = session.get(self.index_url, headers=self.headers, cookies=self.load_session())
        except:
            print 'Cookies is failure.'
            print 'Logging in with an account and password.'
            print 'waiting ...'

            self.use_account_pass_login()
        else:
            login_content = login_page.content

            pattern = r'Login to Phabricator'
            isLogin = re.findall(pattern, login_content)
            # for isLogin1 in isLogin:
            #     print 'isLogin1 : ' + isLogin1

            pattern = r'Authentication Failure'
            isLoginAuth = re.findall(pattern, login_content)
            if (not isLogin) and (not isLoginAuth):
                # print login_content
                print "Cookies Login Success"
                print 'current_account : ' + self.load_last_account()
            else:
                self.use_account_pass_login()

    def use_account_pass_login(self):
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
        # for isLogin1 in isLogin:
        #     print 'isLogin1 : ' + isLogin1
        if not isLogin:
            self.save_session(session)
            # print login_content
            print "Login Success"
            print 'current_account : ' + self.load_last_account()
        else:
            self.save_session(session)
            pattern = r'<div class="phui-info-view-body">(.*?)</div>'
            error_message = re.findall(pattern, login_content)

            # print login_content
            print 'Login Failed'
            print 'Error message: ', error_message[0]
            sys.exit(0)

    def start_login(self):
        print '--------------------Start Login-----------------------------'
        if (os.path.exists(path_history + 'cookies.txt') and (
                self.load_last_account() and self.load_last_account() == self.username)):
            self.use_cookies_login()
        else:
            self.save_last_account(self.username)
            self.delete_cookies()
            self.use_account_pass_login()
