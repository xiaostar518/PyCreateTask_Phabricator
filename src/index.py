#!/usr/bin/env python
# coding:utf-8

from login import *
from maniphest import *
from project import *
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
