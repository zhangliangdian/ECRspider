#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: zhangliangdian@qq.com
@license: Apache Licence
@file: EricOtherClass.py
@time: 2017/9/14 23:10 
"""
import time

# 用于统计程序运行时间
class Timer(object):
    def __init__(self):
        self.start_time = time.clock()    # start the Clock

    def print_now_time(self):
        print('Now is ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    def print_time_consum(self):
        print('Time Consum ' + str(time.clock()-self.start_time) + 'second')

    def time_consum(self):
        return time.clock()-self.start_time


class CookieProcess(object):
    def raw_to_cookie(self, raw):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        cookies = {}
        items = raw.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            cookies[key] = value
        return cookies


class InputUrls(object):
    def read_urls(self):
        print('请在good_urls.txt文件中写入商品网址链接，每行一条，支持淘宝、天猫、京东')
        # 打开网址列表所在文件
        file = open('./good_urls.txt', 'r')
        # 分割网址
        urls = file.read().split('\n')
        # 合理网址存放处
        urls_list = []
        # 网址非法检查
        # 去除UTF-8-BOM编码带来的首行开头的‘\ufeff’(中文连字符 '﻿')
        if urls[0][0] == '﻿':
            urls[0] = urls[0][1:]
        for url in urls:
            if url is not '':  # 剔除空白行
                if url[0] != '#':  # 忽略#开头的网址，注释行
                    urls_list.append(url)
        return urls_list

    def tmall_read_urls(self):
        urls_list = self.read_urls()
        tmall_urls_list = []
        for url in urls_list:
            if 'tmall.com' in url:
                tmall_urls_list.append(url)
        return tmall_urls_list

    def jd_read_urls(self):
        urls_list = self.read_urls()
        jd_urls_list = []
        for url in urls_list:
            if 'jd.com' in url:
                jd_urls_list.append(url)
        return jd_urls_list

    def taobao_read_urls(self):
        urls_list = self.read_urls()
        taobao_urls_list = []
        for url in urls_list:
            if 'item.taobao.com' in url:
                taobao_urls_list.append(url)
        return taobao_urls_list



if __name__ == "__main__":
    pass  