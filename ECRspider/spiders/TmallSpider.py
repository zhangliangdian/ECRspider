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

class TmallSpider(scrapy.Spider):
    name = 'TmallSpider'
    allowed_domains = ['tmall.com', 'taobao.com', 'etao.com']
    custom_settings = {
            'DEFAULT_REQUEST_HEADERS': {
                'referer': 'https://list.tmall.com/search_product.htm?&q=%CA%D5%D2%F8%BB%FA&sort=d&style=g'
            },
            'ITEM_PIPELINES': {'ECRspider.pipelines.TmallPipeline': 300}
        }

    def __init__(self):
        inst_input_urls = InputUrls()
        self.start_urls = inst_input_urls.tmall_read_urls()
        inst_cookie_pro = CookieProcess()
        self.cookie = inst_cookie_pro.raw_to_cookie(settings['TMALL_COOKIES'])
        # 对请求的返回进行处理的配置
        self.meta = {
            'dont_redirect': True,  # 禁止网页重定向
            'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
        }

    # 爬虫的起点
    def start_requests(self):
        # 带着cookie向网站服务器发请求，表明我们是一个已登录的用户
        yield Request(self.start_urls[0], callback=self.parse, cookies=self.cookie, meta=self.meta)

    def parse(self, response):
        # print(response)
        # print(response.body.decode('gbk'))
        goods_item = GoodsItem()
        goods_item['GOODS_URL'] = response.url
        goods_item['GOODS_ID'] = response.xpath('//*[@id="LineZing"]/@itemid').extract_first()
        goods_item['GOODS_NAME'] = response.xpath('//*[@id="J_DetailMeta"]/div/div[1]/div/div[1]/h1/text()').extract_first().strip()
        # get total number of the comments
        totalcom_url = 'https://dsr-rate.tmall.com/list_dsr_info.htm?itemId='+str(goods_item['GOODS_ID'])
        yield scrapy.Request(url=totalcom_url, meta={'item': goods_item}, cookies=self.cookie, callback=self.get_comment_num)

        # ------------------ to get the detail comments ------------------------
        '''网页中带userid的内容为：
        <meta name="microscope-data" content="pageId=1308743026;prototypeId=2;siteId=2; shopId=63641530; userid=631228908;">
        '''
        userid = response.xpath('/html/head/meta[@name="microscope-data"][@content]').extract_first()
        userid = userid.split(';')[-2].split('=')[-1]
        comments_root_url = "https://rate.tmall.com/list_detail_rate.htm?itemId=" + goods_item['GOODS_ID'] + "&sellerId=" \
                            + userid + "&content=1&order=1" + "&currentPage="   # &order=1按时间排序，=3 默认
        currentPage = 1
        yield scrapy.Request(url=comments_root_url+'1',
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
        # jsonp128({"dsr":{"gradeAvg":4.8,"itemId":0,"peopleNum":0,"periodSoldQuantity":0,"rateTotal":2986,"sellerId":0,"spuId":0,"totalSoldQuantity":0}})
        if 'jsonp128' in response_str:
            for idx in range(0, len(response_str)):     # 寻找第一个大括号
                if response_str[idx] == '{':
                    response_str = response_str[idx:-2]   # 取大括号内部的字符串
                    break
            # response_str = response_str[9:-2]   # 取大括号内部的字符串；由于天猫在2017/10/28前在返回的返回的字符串最前面增加了'\r\n'两个字符，因此不再直接指定第一个大括号的位置。
            json_data = json.loads(response_str)
            item['TOTAL_COMMENT'] = json_data['dsr']['rateTotal']
        yield item

    # 对每条评论进行提取
    def detail_comment_parse(self, response):
        log.msg('----天猫-----已经爬取到商品ID为' + str(response.meta['good_id'])+' 的第 ' + str(response.meta['currentPage']) + ' 页评论', level=log.WARNING)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '[Eric] ' + '----天猫-----已经爬取到商品ID为' + str(response.meta['good_id'])+' 的第 ' + str(response.meta['currentPage']) + ' 页评论')
        comment_item = CommentsItem()
        comment_item['GOODS_ID'] = response.meta['good_id']
        tjson = '{' + response.body.decode('gbk', 'ignore').strip() + '}'
        tjson = json.loads(tjson)

        maxPage = tjson['rateDetail']['paginator']['lastPage']
        rate_list = tjson['rateDetail']['rateList']
        comment_item['COMMENTS'] = []
        for rate in rate_list:
            comment = {}
            # 评论时间
            comment['Date'] = rate['rateDate']
            # 初次评论内容
            comment['Content'] = rate['rateContent']
            # 评论用户名
            comment['BuyerName'] = rate['displayUserNick']
            # 用户级别
            comment['BuyerGrade'] = rate['goldUser']
            # 套餐类型
            comment['Style'] = rate['auctionSku']
            # 追加评论
            if rate['appendComment']:   # 非空
                comment['AppendComment'] = rate['appendComment']['content']
                comment['AppendDays'] = rate['appendComment']['days']
            else:
                comment['AppendComment'] = ''
                comment['AppendDays'] = ''
            # 商家回复
            comment['Reply'] = rate['reply']
            comment_item['COMMENTS'].append(comment)
        # 返回评论信息到Pipeline中进行处理
        # print(comment_item)
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
