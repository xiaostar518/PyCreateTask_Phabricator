#!/usr/bin/env python
# coding:utf-8
import cPickle
import json
import os
import re
import requests

path_history = "./history_file/"
usernames_file = './usernames_file/'


class GetUsername:
    def __init__(self):
        with open("./web_files/web_message.json", 'r') as load_f:
            load_dict = json.load(load_f, encoding='UTF-8')
        self.headers = load_dict['headers']
        self.index_url = load_dict['index_url']
        self.username_datasource = 'typeahead/browse/PhabricatorPeopleDatasource/'
        self.i = 1

    def save_username_and_phid(self, usernames):
        if not os.path.exists(usernames_file):
            os.makedirs(usernames_file)
        if os.path.exists(usernames_file + 'username'):
            os.remove(usernames_file + 'username')
        with open(usernames_file + 'username', 'wb') as f:
            cPickle.dump(usernames, f)

        print 'Username message writen: username'

    def load_username_and_phid(self):
        if os.path.exists(usernames_file):
            with open(usernames_file + 'username', 'rb') as f:
                usernames = cPickle.load(f)
            return usernames
        else:
            return False

    def load_session(self):
        with open(path_history + 'cookies', 'rb') as f:
            # headers = cPickle.load(f)
            cookies = cPickle.load(f)
        return cookies

    def get_username(self, usernames=[], next_url=''):
        session = requests.session()
        get_url = bytes(self.index_url) + bytes(self.username_datasource) + next_url

        # print 'get_url : ' + get_url

        data = {
            "exclude": "",
            "__wflow__": "true",
            "__ajax__": "true",
            "__metablock__": self.i + 1
        }
        username_page = session.post(get_url, data=data, headers=self.headers, cookies=self.load_session())
        username_content = username_page.content.decode("unicode_escape").replace('\\', '')

        # print '\n'
        # print '\n'
        # print '-------------------------------username_content--------------------------------------'
        # print username_content

        pattern = re.compile(r'<div class="typeahead-browse-item grouped">(.*?)<div class="result-type">')
        users = re.findall(pattern, username_content)
        for user in users:
            # print user
            temp = {}
            pattern = re.compile(r'phid&quot;:&quot;(.*?)&quot;')
            phid = re.findall(pattern, user)
            # print 'phid : ', phid[0]

            pattern = re.compile(r'<div class="result-name">(.*?)</div>')
            name = re.findall(pattern, user)
            # print 'username : ', name[0]
            temp[name[0].replace(' ', '')] = phid[0]
            usernames.append(temp)

        pattern = re.compile(
            r'a href="/typeahead/browse/PhabricatorPeopleDatasource/(.*?)" class="typeahead-browse-more"')
        next_page = re.findall(pattern, username_content)
        # print 'next_page : ', next_page

        if next_page:
            # print next_page[0].replace('&amp;', '&')
            return self.get_username(usernames=usernames, next_url=next_page[0].replace('&amp;', '&'))

        else:
            # for username in usernames:
            #     print username

            return usernames
