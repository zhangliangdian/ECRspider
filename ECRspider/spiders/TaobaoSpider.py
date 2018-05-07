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

class TaobaoSpider(scrapy.Spider):
    name = 'TaobaoSpider'
    allowed_domains = ['tmall.com', 'taobao.com', 'etao.com']
    custom_settings = {
            'DEFAULT_REQUEST_HEADERS': {
                'referer': 'https://item.taobao.com/item.htm?spm=a230r.1.14.20.76bf523UhgHoT&id=524605950148&ns=1&abbucket=15'
            },
            'ITEM_PIPELINES': {'ECRspider.pipelines.TaobaoPipeline': 200}
        }

    def __init__(self):
        inst_input_urls = InputUrls()
        self.start_urls = inst_input_urls.taobao_read_urls()
        inst_cookie_pro = CookieProcess()
        self.cookie = inst_cookie_pro.raw_to_cookie(settings['TAOBAO_COOKIES'])
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
        # eg url: https://item.taobao.com/item.htm?spm=a230r.1.14.15.76bf523d1yomc&id=524605950148&ns=1&abbucket=15#detail
        goods_item['GOODS_ID'] = response.url.split('id=')[1].split('&')[0]
        goods_item['GOODS_NAME'] = response.xpath('/html/head/title/text()').extract_first()[:-4]  # 去掉“-淘宝网”

        # get total number of the comments
        totalcom_url = 'https://rate.taobao.com/detailCount.do?callback=jsonp100&itemId='+str(goods_item['GOODS_ID'])
        yield scrapy.Request(url=totalcom_url, meta={'item': goods_item}, cookies=self.cookie, callback=self.get_comment_num)

        # ------------------ to get the detail comments ------------------------
        '''网页中带userid的内容为：
        <meta name="microscope-data" content="pageId=1308743026;prototypeId=2;siteId=2; shopId=63641530; userid=631228908;">
        '''
        userid = response.xpath('/html/head/meta[@name="microscope-data"][@content]').extract_first()
        userid = userid.split(';')[-2].split('=')[-1]
        comments_root_url = 'https://rate.taobao.com/feedRateList.htm?auctionNumId=' + str(goods_item['GOODS_ID']) \
                            + '&userNumId=' + userid + '&pageSize=20&rateType=&attribute=&sku=&hasSku=false&folded=0' \
                                                       '&callback=jsonp_tbcrate_reviews_list&orderType=sort_weight&currentPageNum='
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
        # jsonp100({"count":3196})
        if 'jsonp100' in response_str:
            response_str = response_str[9:-1]   # 取大括号内部的字符串
            json_data = json.loads(response_str)
            item['TOTAL_COMMENT'] = json_data['count']
        yield item

    # 对每条评论进行提取
    def detail_comment_parse(self, response):
        log.msg('----淘宝-----已经爬取到商品ID为' + str(response.meta['good_id'])+' 的第 ' + str(response.meta['currentPage']) + ' 页评论', level=log.WARNING)
        print('----淘宝-----已经爬取到商品ID为' + str(response.meta['good_id'])+' 的第 ' + str(response.meta['currentPage']) + ' 页评论')
        comment_item = CommentsItem()
        comment_item['GOODS_ID'] = response.meta['good_id']
        tjson = response.body.decode('gbk', 'ignore').strip()[1:-1]     # 去掉首位的空字符和小括号
        tjson = json.loads(tjson)
        # print(tjson)    # 用于Debug下查看json数据结构
        # input()
        maxPage = tjson['maxPage']
        rate_list = tjson['comments']
        comment_item['COMMENTS'] = []
        for rate in rate_list:
            comment = {}
            # 评论时间
            comment['Date'] = rate['date']
            # 初次评论内容
            comment['Content'] = rate['content']
            # 评论用户名
            comment['BuyerName'] = rate['user']['nick']
            # 用户级别
            comment['BuyerGrade'] = rate['user']['vipLevel']
            # 套餐类型
            comment['Style'] = rate['auction']['sku']
            # 追加评论
            if rate['append']:   # 非空
                comment['AppendComment'] = rate['append']['content']
                comment['AppendDays'] = rate['append']['dayAfterConfirm']
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
