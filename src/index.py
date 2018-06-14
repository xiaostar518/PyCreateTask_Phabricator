#!/usr/bin/env python
# coding:utf-8

from login import *
from maniphest import *
from project import *
import time
from py_excel import *
from getusername import *
import sys

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


def load_username():
    get_username = GetUsername()
    get_username.get_username()


def export_excel():
    username_content = []
    username_content.append("12424324432dddfdf")
    username_content.append("23121dfsdff")
    username_content.append("243ffgfgfgf")
    operateExcel = OperateExcel()
    operateExcel.export_username_excel(export_xlsx, username_content)


if __name__ == "__main__":
    user_login()

    time.sleep(0.5)

    select_function()

    num = in_putNum(max=2, min=0)

    if num == 0:
        load_username()
        # export_excel()
    elif num == 1:
        # sys.exit(0)
        use_project()
