#!/usr/bin/env python
# coding:utf-8

from login import *
from maniphest import *
from project import *
import time
from py_excel import *
from getusername import *
import sys
import os
import cPickle

export_xlsx = './Excel_files/all_username.xlsx'


def user_login():
    # 登录
    user_login = UserLogin()
    user_login.start_login()


def use_mainphest():
    # Maniphest
    maniphest = UseManiphest()
    maniphest.enter_maniphest()


def use_project():
    # Project
    project = UseProject()
    project.enter_project()


def select_function():
    print '\n'
    print '\n'
    print "Do you want anything?"
    print "0 : Get all username"
    print "1 : Import and create task"


def in_putNum(max, min=0):
    content = "Please input your chosen number: "
    num = raw_input(content)
    print "Received is : ", num
    if num.isdigit():
        num = int(num)
        if max > num >= min:
            return num
        else:
            print "The number is wrong."
            print '\n'
            print "Please try again:"
            return in_putNum(max)

    else:
        print "The input isn`t digit.\nPlease try again:"
        return in_putNum(max)


def get_web_username():
    get_username = GetUsername()

    print '\n'
    print '\n'
    print '-------------------------------loading username start-----------------------------'
    usernames = get_username.get_username()

    # for username in usernames:
    #     print username

    if usernames:
        get_username.save_username_and_phid(usernames)

    return usernames


def export_excel(usernames):
    print '\n'
    print '\n'
    print '-------------------------------save username--------------------------------------'
    operateExcel = OperateExcel()
    operateExcel.export_username_excel(export_xlsx, usernames)


# def load_username_and_phid():


if __name__ == "__main__":
    user_login()

    time.sleep(0.5)

    select_function()

    num = in_putNum(max=2, min=0)

    if num == 0:
        usernames = get_web_username()
        users = []
        for username in usernames:
            for user, phid in username.items():
                print user
                # print 'user : ', user
                # print 'phid : ', phid
                users.append(user)
        # print users
        print '-------------------------------loading username end-------------------------------'

        time.sleep(0.5)
        if usernames:
            export_excel(users)
        else:
            print 'Username is null.'
            print 'Exit.'
    elif num == 1:
        # sys.exit(0)
        use_project()
