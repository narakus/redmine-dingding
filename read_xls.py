#!/usr/bin/env python
#-*- coding: utf-8 -*-

import xlrd

def read_xls_by_file(redmine_mail):
    result = {'userid':None,'status':False}
    data = xlrd.open_workbook('你的企业通讯录文件')
    table = data.sheets()[0]
    for item in range(table.nrows):
       if item == 0:
           continue
       ding_mail = table.cell(item,7).value
       if redmine_mail == ding_mail:
          result['userid'] = table.cell(item,0).value
          result['status'] = True
    return result


if __name__ == '__main__':
    m = read_xls_by_file('测试邮箱地址')
    print m
