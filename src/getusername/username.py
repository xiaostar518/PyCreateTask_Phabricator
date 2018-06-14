#!/usr/bin/env python
# coding:utf-8
import cPickle
import json
import os
import re
import requests

path_history = "./history_file/"


class GetUsername:
    def __init__(self):
        with open("./web_files/web_message.json", 'r') as load_f:
            load_dict = json.load(load_f, encoding='UTF-8')
        self.headers = load_dict['headers']
        self.index_url = load_dict['index_url']
        self.username_datasource = 'typeahead/browse/PhabricatorPeopleDatasource/'

    def save_username(self, account):
        if not os.path.exists(path_history):
            os.makedirs(path_history)

        with open(path_history + 'username.txt', 'wb') as f:
            cPickle.dump(account, f)

            print 'username writen: username.txt'

    def load_username(self):
        if os.path.exists(path_history + 'username.txt'):
            with open(path_history + 'username.txt', 'rb') as f:
                account = cPickle.load(f)
            return account
        else:
            return False

    def load_session(self):
        with open(path_history + 'cookies.txt', 'rb') as f:
            # headers = cPickle.load(f)
            cookies = cPickle.load(f)
        return cookies

    def get_username(self):
        session = requests.session()
        get_url = bytes(self.index_url) + bytes(self.username_datasource)
        data = {
            "exclude": "",
            "__wflow__": "true",
            "__ajax__": "true",
            "__metablock__": "1"
        }
        username_page = session.post(get_url, data=data, headers=self.headers, cookies=self.load_session())
        username_content = username_page.content.decode("unicode_escape").replace('\\', '')

        print '\n'
        print '\n'
        print '-------------------------------username_content--------------------------------------'
        print username_content

        pattern = re.compile(r'<div class="result-name">(.*?)</div>')
        usernames = re.findall(pattern, username_content)
        for username in usernames:
            print username
