#!/usr/bin/env python
# coding:utf-8
import cPickle
import json
import re

import requests
from bs4 import BeautifulSoup
from py_excel import *
import platform
import time
import sys

pre_task = "std:maniphest:task."
path_history = "./history_file/"


def excel_message_transfest_postdata(excel_messages):
    with open("./web_files/web_message.json", 'r') as load_f:
        load_dict = json.load(load_f, encoding='UTF-8')
    module = load_dict['task.module']
    foundMethod = load_dict['task.foundMethod']
    HWVersion = load_dict['task.HWVersion']
    priority = load_dict['priority']
    status = load_dict['status']

    data_messages = []
    for excel_message in excel_messages:
        # print "excel_message : ", excel_message

        messages = {}
        for key, value in excel_message.items():
            # print "\n"
            # print "key : %s, value : %s" % (key, value)
            if not value:
                continue
            try:
                if key == 'module':
                    messages[pre_task + "module"] = module[value]
                elif key == 'foundmethod':
                    messages[pre_task + "foundMethod"] = foundMethod[value]
                elif key == 'hwversion':
                    messages[pre_task + "HWVersion"] = HWVersion[value]
                elif key == 'swversion':
                    messages[pre_task + "swVersion"] = value
                elif key == 'fixversion':
                    messages[pre_task + "fixVersion"] = value
                elif key == 'verifyversion':
                    messages[pre_task + "verifyVersion"] = value
                elif key == 'workload':
                    messages[pre_task + "workload"] = value
                elif key == 'rootcause':
                    messages[pre_task + "rootCause"] = value
                elif key == 'status':
                    messages['status'] = status[value]
                elif key == 'priority':
                    messages['priority'] = priority[value]
                elif key == 'priority':
                    messages['priority'] = priority[value]
                else:
                    messages[key] = value
                # print "messages : ", messages
            except Exception, e:
                myPrint("Error : %s does not exist, skip." % e)

        data_messages.append(messages)
        # print "\n"
        # print "\n"

    # print data_messages

    return data_messages


def myPrint(text):
    sys_style = platform.system()
    if sys_style == "Windows":
        # print ("Call Windows tasks")
        print unicode(text, 'utf-8').encode('gbk')
    elif sys_style == "Linux":
        # print ("Call Linux tasks")
        print text
    else:
        # print ("Other System tasks")
        print text


class UseProject:
    def __init__(self):
        with open("./web_files/web_message.json", 'r') as load_f:
            load_dict = json.load(load_f, encoding='UTF-8')
        self.headers = load_dict['headers']
        self.index_url = load_dict['index_url']
        self.project = 'project/query/all/'
        self.project_board = 'project/board/'
        self.projects = None
        self.__metablock__ = 1
        self.session = requests.session()
        self.excel = OperateExcel('./Excel_files/tasks_content.xlsx', './Excel_files/Example.xlsx')

    def load_session(self):
        with open(path_history + 'cookies.txt', 'rb') as f:
            # headers = cPickle.load(f)
            cookies = cPickle.load(f)
        return cookies

    def enter_project(self):
        # session = requests.session()
        get_url = bytes(self.index_url) + bytes(self.project)
        project_page = self.session.get(get_url, headers=self.headers, cookies=self.load_session())
        project_content = project_page.content

        print '\n'
        print '\n'

        # print '-------------------------------project_content--------------------------------------'
        # print project_content

        soup = BeautifulSoup(project_content, "lxml", from_encoding='utf-8')
        # print soup.prettify()
        # print '-------------------------------soup.prettify--------------------------------------'
        # print '-------------------------------soup.prettify--------------------------------------'
        # print '-------------------------------soup.prettify--------------------------------------'
        # print soup.find_all(href=re.compile("/project/view/"))
        self.projects = []
        for project in soup.find_all(href=re.compile("/project/view/"), title=re.compile("")):
            # print bytes(project)
            # print project.find_all("title")
            # soup_project = BeautifulSoup(project, "lxml", from_encoding='utf-8')
            pattern = r'title="(.*?)"'
            title = re.findall(pattern, bytes(project))
            pattern = r'href="/project/view/(.*?)/"'
            href = re.findall(pattern, bytes(project))
            d = {"title": title[0], "href": href[0]}
            self.projects.append(d)

        print '--------------------Select project-----------------------------'
        time.sleep(0.5)

        i = 0
        for project_content in self.projects:
            # print bytes(i) + ": " + project_content["title"]
            myPrint(bytes(i) + ": " + project_content["title"])
            i += 1
        num = self.in_putNum('project', i)
        # print "Selected project is : " + self.projects[num]["title"]
        myPrint("Selected project is : " + self.projects[num]["title"])
        self.enter_selected_project(num)

    def in_putNum(self, text, max, min=0):
        content = "Please input your %s`s number: " % text
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
                return self.in_putNum(text, max)

        else:
            print "The input isn`t digit.\nPlease try again:"
            return self.in_putNum(text, max)

    def enter_selected_project(self, num):
        # session = requests.session()
        get_url = bytes(self.index_url) + bytes(self.project_board) + self.projects[num]["href"] + '/'
        project_board_page = self.session.get(get_url, headers=self.headers, cookies=self.load_session())
        project_board_content = project_board_page.content

        print '\n'
        print '\n'
        # print '-------------------------------project_board_content--------------------------------------'
        # print project_board_content

        self.maniphest_edit(project_board_content)

    def maniphest_edit(self, project_board_content):
        soup = BeautifulSoup(project_board_content, "lxml", from_encoding='utf-8')
        columns = soup.find_all(attrs={"class": "phui-header-header"})
        # print columns

        print '--------------------Select column-----------------------------'
        self.project_columns = []
        i = 0
        for workboard in columns:
            pattern = r'<span class="phui-header-header">(.*?)</span>'
            column_name = re.findall(pattern, bytes(workboard))
            self.project_columns.append(column_name[0])
            # print bytes(i) + " : " + column_name[0]
            myPrint(bytes(i) + " : " + column_name[0])
            i += 1

        if i == 1 and self.project_columns[0] == 'Create Workboard':
            print 'There is no column of this project. Exit.'
            sys.exit(0)

        selected_column_num = self.in_putNum('column', i)
        # print "Selected column is : " + self.project_columns[selected_column_num]
        myPrint("Selected column is : " + self.project_columns[selected_column_num])

        pattern = r'JX.Stratcom.mergeData(.*?);'
        text = re.findall(pattern, project_board_content)
        # print text[0]

        pattern = r'"createURI":"(.*?)"'
        uris = re.findall(pattern, project_board_content)

        self.forms_num = len(uris) / len(self.project_columns)
        # print "forms_num", self.forms_num
        i = 0
        self.formsURI = []
        while (i < self.forms_num):
            # print 'createURI : ' + bytes(i)
            # print uris[i].decode("unicode_escape").replace('\\', '')
            self.formsURI.append(uris[i].decode("unicode_escape").replace('\\', ''))
            i += 1
        # print self.formsURI

        js_content = text[0].decode("unicode_escape").replace('\\', '')

        pattern = r'"columnPHID":"(.*?)"'
        columnPHIDs = re.findall(pattern, js_content)
        # print "columnPHID : ", columnPHIDs

        self.columnsPHID = []
        for colunm in columnPHIDs:
            if colunm not in self.columnsPHID:
                self.columnsPHID.append(colunm)
                # print "column : " + colunm

        pattern = r'"boardPHID":"(.*?)"'
        boardPHID = re.findall(pattern, js_content)
        # print "boardPHID : " + boardPHID[0]

        pattern = r'"projectPHID":"(.*?)"'
        projectPHID = re.findall(pattern, js_content)
        # print "projectPHID : " + projectPHID[0]

        soup = BeautifulSoup(js_content, "lxml")
        # print soup.prettify()
        all_forms = soup.find_all("a",
                                  class_="phabricator-action-view-item", href=re.compile("/maniphest/task/edit/form/"))

        print '\n'
        print '\n'

        print '--------------------Select form-----------------------------'
        time.sleep(0.5)

        self.forms = []
        i = 0
        while (i < self.forms_num):
            pattern = r'</span>(.*?)</a>'
            form = re.findall(pattern, bytes(all_forms[i]))
            self.forms.append(form[0])
            # print bytes(i) + " : " + form[0]
            myPrint(bytes(i) + " : " + form[0])
            i += 1
        # print self.forms

        selected_form_num = self.in_putNum('form', i)
        # print "Selected form is : " + self.forms[selected_form_num]
        myPrint("Selected form is : " + self.forms[selected_form_num])

        # print "\n\n\n----------------------------------\n\n\n"

        pattern = r'name="__csrf__" value="(.*?)"'
        __csrf__ = re.findall(pattern, project_board_content)
        self.phabricator_Csrf = __csrf__[0]
        # print 'X-Phabricator-Csrf : ' + self.phabricator_Csrf

        pattern = r'"/project/board/(.*?)/"'
        var = re.findall(pattern, project_board_content)
        self.phabricator_var = '/project/board/' + var[0] + '/'
        # print 'X-Phabricator-Via : ' + self.phabricator_var

        # print "columns : " + self.project_columns[selected_column_num]
        # print "columnPHID : " + self.columnsPHID[selected_column_num]
        # print "boardPHID : " + boardPHID[0]
        # print "projectPHID : " + projectPHID[0]
        # print "Selected form is : " + self.forms[selected_form_num]
        # print "Selected formPHID is : " + self.formsURI[selected_form_num]

        pattern = r'/maniphest/task/edit/form/(.*?)/'
        edit_url = re.findall(pattern, self.formsURI[selected_form_num])
        post_url = bytes(self.index_url) + "maniphest/task/edit/form/" + edit_url[0] + "/"
        # print post_url

        postEditData = {
            "responseType": "card",
            "columnPHID": self.columnsPHID[selected_column_num],
            "projects": projectPHID[0],
            "visiblePHIDs": "",
            "order": "natural",
            "__wflow__": "true",
            "__ajax__": "true",
            "__metablock__": self.__metablock__

        }

        self.postEditHeaders = self.headers
        self.postEditHeaders["X-Phabricator-Csrf"] = self.phabricator_Csrf
        self.postEditHeaders["X-Phabricator-Via"] = self.phabricator_var
        # print self.postEditHeaders

        # post edit page
        edit_page = self.session.post(post_url, data=postEditData, headers=self.postEditHeaders,
                                      cookies=self.load_session())
        edit_content = edit_page.content.decode("unicode_escape").replace('\\', '')

        # print edit_content
        self.__metablock__ += 1

        # post create page
        soup = BeautifulSoup(edit_content, "lxml")
        # print soup.prettify()

        __csrf__ = soup.find('input', {'name': '__csrf__'}).get('value')
        __form__ = soup.find('input', {'name': '__form__'}).get('value')
        __dialog__ = soup.find('input', {'name': '__dialog__'}).get('value')
        editEngine = soup.find('input', {'name': 'editEngine'}).get('value')
        responseType = soup.find('input', {'name': 'responseType'}).get('value')
        columnPHID = soup.find('input', {'name': 'columnPHID'}).get('value')
        order = soup.find('input', {'name': 'order'}).get('value')
        visiblePHIDs = soup.find('input', {'name': 'visiblePHIDs'}).get('value')
        column_ = soup.find('input', {'name': 'column[]'}).get('value')
        visiblePHIDs = soup.find('input', {'name': 'visiblePHIDs'}).get('value')

        # print "__csrf__ : ", __csrf__
        # print "__form__ : ", __form__
        # print "__dialog__ : ", __dialog__
        # print "editEngine : ", editEngine
        # print "responseType : ", responseType
        # print "columnPHID : ", columnPHID
        # print "order : ", order
        # print "visiblePHIDs : ", visiblePHIDs
        # print "column_ : ", column_
        # print "visiblePHIDs : ", visiblePHIDs

        self.postCreateData = {
            "__csrf__": __csrf__,
            "__form__": __form__,
            "__dialog__": __dialog__,
            "editEngine": editEngine,
            "responseType": responseType,
            "columnPHID": columnPHID,
            "order": order,
            "visiblePHIDs": "",
            "column[]": column_,

            "__wflow__": "true",
            "__ajax__": "true",
            "__metablock__": self.__metablock__

        }

        print '\n'
        print '\n'

        print '--------------------Load excel-----------------------------'
        time.sleep(0.5)

        # self.set_task_data_excel()
        postTaskDatas = self.get_task_data_excel()

        print '\n'
        print '\n'

        print '--------------------Create tasks-----------------------------'
        time.sleep(0.5)

        self.send_post_many_data(post_url, postTaskDatas)

        # data = {
        #     '__csrf__': __csrf__,
        #     '__form__': __form__,
        #     '__dialog__': __dialog__,
        #     '__submit__': 'true',
        #     'filePHIDs': 'PHID-FILE-gmyxr46fs6mzuhfeoieh',
        #     '__wflow__': 'true',
        #     '__ajax__': 'true',
        #     '__metablock__': self.__metablock__,
        # }
        #
        # self.phabricator_var1 = '/project/view/' + var[0] + '/'
        # print 'X-Phabricator-Via1 : ' + self.phabricator_var1
        #
        # # self.set_task_data_excel()
        # self.postTaskDatas = self.get_task_data_excel()
        # post_url = bytes(self.index_url) + "file/uploaddialog/"
        # myHeaders = self.headers
        # myHeaders["X-Phabricator-Csrf"] = self.phabricator_Csrf
        # myHeaders["X-Phabricator-Via"] = self.phabricator_var1
        # edit_page = self.session.post(post_url, data=data,
        #                               headers=myHeaders,
        #                               cookies=self.load_session())
        # edit_content = edit_page.content.decode("unicode_escape").replace('\\', '')
        # print edit_content
        # self.__metablock__ += 1

    def send_post_many_data(self, post_url, postTaskDatas):
        create_success = []
        create_fail = []
        for post_task_data in postTaskDatas:
            result = self.create_task(post_url, post_task_data)
            if result:
                create_success.append(post_task_data)
            else:
                create_fail.append(post_task_data)

        if create_fail:
            if self.try_again_post():
                self.send_post_many_data(post_url, create_fail)
            else:
                print 'Fail tasks is cancel.'
                print 'Create tasks over!!!'
        else:
            print 'Create tasks success.'
            print 'Create tasks over!!!'

    def set_task_data_excel(self):
        task_content = []
        task_content.append({"title": ["测试title1", "测试title2"]})
        task_content.append({"description": ["测试description1", "测试description2"]})

        self.excel.export_excel(task_content)

    def get_task_data_excel(self):
        # postTaskData = {
        #     "title": "我的测试10",
        #     "description": "我是个测试而已"
        # }

        excel_messages = self.excel.load_excel()

        postTaskData = excel_message_transfest_postdata(excel_messages)
        return postTaskData

    def create_task(self, post_url, postTaskData):
        # send post message for create task
        edit_page = self.session.post(post_url, data=dict(self.postCreateData, **postTaskData),
                                      headers=self.postEditHeaders,
                                      cookies=self.load_session())
        self.__metablock__ += 1
        edit_content = edit_page.content.decode("unicode_escape").replace('\\', '')
        # print edit_content

        pattern = r'<div class="phui-info-view-body">(.*?)</div>'
        error = re.findall(pattern, edit_content)

        pattern = r'"objectPHID":"(.*?)",'
        success = re.findall(pattern, edit_content)
        # print 'error : ', error
        # print 'success : ', success
        if success:
            print 'Create task ------- title : %s ------- is success.' % postTaskData['title']
            return True
        elif error:
            print 'Create task ------- title : %s ------- is fail.\n Error : %s' % (postTaskData['title'], error[0])
            return False
        else:
            print 'Create task ------- title : %s ------- is fail.' % postTaskData['title']
            return False

    def try_again_post(self):
        word = raw_input("Do you want try again? Y/n ")
        print "Received is : ", word
        if word.isalpha():
            if word == 'Y' or word == 'y':
                return True
            elif word == 'N' or word == 'n':
                return False
            else:
                print "The letter is wrong."
                print '\n'
                print 'Please try again.'
                return self.try_again_post()

        else:
            print "The input isn`t letter."
            print '\n'
            print 'Please try again.'
            return self.try_again_post()
