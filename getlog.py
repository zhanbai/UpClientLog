#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
About: Pull download the log lists.
Author: XIAO
Date: 2016-08-22
'''

import requests
import json
import sys
import re
import time

api = 'https://api.upyun.com'

def getopt():
    access_token = sys.argv[1]
    date = sys.argv[2]
    bucket_name = sys.argv[3]
    domain = ''

    num = len(sys.argv[1:])

    if num == 4:
        domain = sys.argv[4]

    return (access_token, date, bucket_name, domain)

def getlog(access_token, bucket_name, date, domain):
    headers = {
        'Authorization': 'Bearer ' + access_token        
    }

    response = requests.get(api + '/analysis/archives/?bucket_name=' + bucket_name + '&date=' + date + '&domain=' + domain, headers = headers)
    response = json.loads(response.text)
    datas = response['data']
    
    fo = open('log_lists.txt', 'w')
    if datas:
        for data in datas:
            fo.write(data['url'] + "\n")
            print data['url']
    else:
        print '--- 不存在相关日志下载列表 ---'
        sys.exit()

    fo.close()

def getday(date):
    if re.search('~', date):
        date = date.split('~')
        start_date = time.mktime(time.strptime(date[0], '%Y-%m-%d'))
        end_date = time.mktime(time.strptime(date[1], '%Y-%m-%d'))
        day = int((end_date - start_date) / 86400)
        
        i = 0
        date = []

        while (i <= day):
            date.append(time.strftime('%Y-%m-%d', time.localtime(start_date + i*86400)))
            i = i + 1
    else:
        date_temp = date
        date = []
        date.append(date_temp)

    return date

num = len(sys.argv[1:])

if num < 3:
    print '---'
    print '--- 请检查是否正确输入了必选项 access_token date 和 bucket_name 参数的值 ---'
    print '---'
    sys.exit()

access_token, date, bucket_name, domain = getopt()
date = getday(date)

for date in date:
    getlog(access_token, bucket_name, date, domain)

print '--- 日志下载列表写入文件完成 ---'
