#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
import urlparse
import requests
from read_xls import read_xls_by_file

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_sendurl_with_token(secret):
    '''获取钉钉token'''
    corpid,corpsecret = secret
    request_url = 'https://oapi.dingtalk.com/gettoken?corpid=%s&corpsecret=%s' % (corpid,corpsecret)
    response = requests.get(request_url)
    token = response.json()['access_token']
    send_url = 'https://oapi.dingtalk.com/message/send?access_token=' + token
    return token,send_url

class Ding(object):

    def __init__(self,redmine_post_data,send_url):
        self.send_url = send_url
        #self.users = '1134385402671636'
        #self.body = {'author':'','content':'','form':[],'image':'@lADOADmaWMzazQKA','title':''}
        #self.body = {'author':'','content':'','form':[],'title':'','rich':{'unit':''}}
        self.body = {'author':'','content':'','form':[],'title':''}
        #self.action = json.loads(redmine_post_data)['payload']['action']
        self.data = json.loads(redmine_post_data)
        self.red_data = json.loads(redmine_post_data).values()[0]
        self.header = {"Content-Type": "application/json;charset=utf-8"}
        self.send_data = {'msgtype':'oa','agentid':'157660637','touser':'',
                          'oa':{'body':self.body,'head':{'bgcolor': 'FFBBBBBB','text':'redmine'},
                          'message_url':'','pc_message_url':''}
                         }

    def get_mailaddr(self):
        action = self.data['payload']['action']
        if action == 'opened':
            mail_addr = self.red_data['issue']['assignee']['mail']
        else:
            mail_addr = self.red_data['issue']['author']['mail']
        return  read_xls_by_file(mail_addr)

    def send(self,userid):
        self.send_data['touser'] = userid
        local_url = self.red_data['url']
        local_obj = urlparse.urlparse(local_url)
        myurl = 'http://zmine.zeasn.com'
        message_url = urlparse.urljoin(myurl,local_obj.path)
        status = self.red_data['issue']['status']['name']
        author = self.red_data['issue']['author']['login']
        subject = self.red_data['issue']['subject']
        project = self.red_data['issue']['project']['name']
        try:
            assignee = self.red_data['issue']['assignee']['login']
        except:
            assignee = ''
        try:
            description = self.red_data['issue']['description']
        except:
            description = ''
        try:
            notes = self.red_data['journal']['notes']
        except:
            notes = ''
        self.body['author'] = author
        self.body['content'] = description
        self.body['title'] = subject
        self.body['form'].append({'key':'项目','value':project})
        self.body['form'].append({'key':'指派','value':assignee})
        self.body['form'].append({'key':'状态','value':status})
        #self.body['form'].append({'key':'状态','value':status})
        #self.body['rich']['unit'] = status
        self.body['form'].append({'key':'描述','value':notes})
        self.send_data['oa']['message_url'] = message_url
        self.send_data['oa']['pc_message_url'] = message_url
        

        response = requests.post(self.send_url,data = json.dumps(self.send_data),headers=self.header)
        print response.text
