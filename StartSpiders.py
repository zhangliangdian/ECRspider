#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: zhangliangdian@qq.com
@license: Apache Licence
@file: StartSpiders.py
@time: 2017/8/23 23:30 
"""

from scrapy import cmdline

# 天猫
# cmdline.execute("scrapy crawl TmallSpider --nolog".split())
# cmdline.execute("scrapy crawl TmallSpider".split())
# cmdline.execute("scrapy crawl TmallSpider -s LOG_FILE=TmallScrapyLog.txt".split())

# 京东
cmdline.execute("scrapy crawl JDSpider".split())
# cmdline.execute("scrapy crawl JDSpider -s LOG_FILE=JDScrapyLog.txt".split())

# 淘宝
# cmdline.execute("scrapy crawl TaobaoSpider".split())
# cmdline.execute("scrapy crawl TaobaoSpider -s LOG_FILE=TaobaoScrapyLog.txt".split())
