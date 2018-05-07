#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: zhangliangdian@qq.com
@license: Apache Licence
@file: StartSpiders.py
@time: 2017/8/23 23:30
使用 scrapy genspider spiderName 命令新建spider
"""

import scrapy
from scrapy.http import Request
from ECRspider.items import GoodsItem, CommentsItem
from scrapy.conf import settings
from scrapy import log
import json
from ECRspider.EricOtherClass import CookieProcess, InputUrls
import time


class JDSpider(scrapy.Spider):
    name = 'JDSpider'
    allowed_domains = ['jd.com']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'referer': 'https://search.jd.com/Search?keyword=%E6%94%B6%E9%93%B6%E6%9C%BA&enc=utf-8&suggest=2.def.0.V13&wq=shouyj&pvid=eed056318f1646558de7af942dfc6945'
        },
        'ITEM_PIPELINES': {'ECRspider.pipelines.JDPipeline': 300}
    }

    def __init__(self):
        inst_input_urls = InputUrls()
        self.start_urls = inst_input_urls.jd_read_urls()
        inst_cookie_pro = CookieProcess()
        self.cookie = inst_cookie_pro.raw_to_cookie(settings['JD_COOKIES'])
        # 对请求的返回进行处理的配置
        self.meta = {
            'dont_redirect': True,  # 禁止网页重定向
            'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
        }

    def start_requests(self):
        # 带着cookie向网站服务器发请求，表明我们是一个已登录的用户
        yield Request(self.start_urls[0], callback=self.parse, cookies=self.cookie, meta=self.meta)

    def parse(self, response):
        # print(response)
        # print(response.body.decode('gbk'))
        goods_item = GoodsItem()
        goods_item['GOODS_URL'] = response.url
        goods_item['GOODS_ID'] = response.url.split('.html')[0].split('/')[-1]
        goods_item['GOODS_NAME'] = response.xpath('/html/head/title/text()').extract_first()[:-16]  # 去掉“【行情 报价 价格 评测】-京东”

        # get total number of the comments
        totalcom_url = 'http://club.jd.com/ProductPageService.aspx?method=GetCommentSummaryBySkuId&referenceId='+str(goods_item['GOODS_ID'])
        yield scrapy.Request(url=totalcom_url, meta={'item': goods_item}, cookies=self.cookie, callback=self.get_comment_num)

        # ------------------ to get the detail comments ------------------------
        comments_root_url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv933&productId='\
                            + str(goods_item['GOODS_ID']) + '&score=0&sortType=5&pageSize=10&isShadowSku=0&fold=1&page='
        currentPage = 0
        yield scrapy.Request(url=comments_root_url+'0',
                             meta={'good_id':       goods_item['GOODS_ID'],
                                   'root_url':      comments_root_url,
                                   'currentPage':   currentPage,
                                   },
                             cookies=self.cookie,
                             callback=self.detail_comment_parse
                             )
        # 爬取下一个商品的页面
        self.start_urls.pop(0)
        if len(self.start_urls) > 0:
            yield Request(self.start_urls[0], callback=self.parse, cookies=self.cookie, meta=self.meta)

    def get_comment_num(self, response):
        item = response.meta['item']
        response_str = response.body.decode('gbk', 'ignore')
        json_data = json.loads(response_str)
        item['TOTAL_COMMENT'] = json_data['CommentCount']
        yield item

    # 对每条评论进行提取
    def detail_comment_parse(self, response):
        log.msg('----京东-----已经爬取到商品ID为' + str(response.meta['good_id'])+' 的第 ' + str(response.meta['currentPage']) + ' 页评论', level=log.WARNING)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '[Eric] '+'----京东-----已经爬取到商品ID为' + str(response.meta['good_id'])+' 的第 ' + str(response.meta['currentPage']) + ' 页评论')
        comment_item = CommentsItem()
        comment_item['GOODS_ID'] = response.meta['good_id']
        tjson = response.body.decode('gbk', 'ignore')
        # 去除前缀"fetchJSON_comment98vv933("和尾缀");"
        if 'fetchJSON_comment' in tjson:
            tjson = tjson[25:-2]
        tjson = json.loads(tjson)
        # print(tjson)      # 用于Debug下查看json数据结构
        # input()
        maxPage = tjson['maxPage']
        rate_list = tjson['comments']
        comment_item['COMMENTS'] = []
        for rate in rate_list:
            comment = {}
            # 评论时间
            comment['Date'] = rate['creationTime']
            # 初次评论内容
            comment['Content'] = rate['content']
            # 评论用户名
            comment['BuyerName'] = rate['nickname']
            # 用户级别
            comment['BuyerGrade'] = rate['userLevelName']
            # 套餐类型
            # comment['Style'] = rate['productColor'] + '    ' + rate['productSize']
            # 追加评论
            if 'afterUserComment' in rate.keys():
                comment['AppendComment'] = rate['afterUserComment']['hAfterUserComment']['content']
                comment['AppendDays'] = ''
            else:
                comment['AppendComment'] = ''
                comment['AppendDays'] = ''

            comment_item['COMMENTS'].append(comment)
        # 返回评论信息到Pipeline中进行处理
        yield comment_item
        # 爬取下一页评论
        next_page = response.meta['currentPage'] + 1
        if next_page <= maxPage:
            yield scrapy.Request(url=response.meta['root_url'] + str(next_page),
                                 meta={'good_id':       response.meta['good_id'],
                                       'root_url':      response.meta['root_url'],
                                       'currentPage':   next_page,
                                       },
                                 cookies=self.cookie,
                                 callback=self.detail_comment_parse,
                                 )
