#!/usr/bin/env python
# coding:utf-8

from login import *
from maniphest import *
from project import *
import time


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


if __name__ == "__main__":
    user_login()

    time.sleep(0.5)
    use_project()
