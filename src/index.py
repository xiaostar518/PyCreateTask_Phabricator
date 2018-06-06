#!/usr/bin/env python
# coding:utf-8

from login import UserLogin
from maniphest import UseManiphest
from project import UseProject
import time

# 登录
user_login = UserLogin()
user_login.start_login()

# #Maniphest
# maniphest = UseManiphest()
# maniphest.enter_maniphest()

time.sleep(0.5)
# Project
project = UseProject()
project.enter_project()
