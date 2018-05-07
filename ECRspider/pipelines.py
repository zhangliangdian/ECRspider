# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from scrapy.conf import settings

class EcrspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class TmallPipeline(object):
    def __init__(self):
        # 建立MongoDB连接
        db_connect = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        # 建立数据库
        db = db_connect[settings['MONGODB_DBNAME']]
        # 建立文档集合（表）
        self.db_doc = db[settings['TMALL_MONGODB_DOCNAME']]

    # spider打开时自动执行
    def open_spider(self, spider):
        pass

    # spider关闭时自动执行
    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # 合并同一个GOODS_ID下的信息，使用update()
        if 'GOODS_NAME' in dict(item).keys():  # 商品信息
            # print(item)
            self.db_doc.update_one({'GOODS_ID': item['GOODS_ID']},
                                   {'$set':   { 'GOODS_NAME':   item['GOODS_NAME'],
                                                'GOODS_URL':    item['GOODS_URL'],
                                                'TOTAL_COMMENT': item['TOTAL_COMMENT'],
                                                }
                                    },
                                   upsert=True,    # perform an insert if no documents match the filter
                                   )
        elif 'COMMENTS' in dict(item).keys():  # 评论追加
            # print(item)
            for comment in item['COMMENTS']:
                # 如果数据库中不存在该评论，则添加；以买家和评论日期为准
                exist = self.db_doc.find_one({'GOODS_ID': item['GOODS_ID'],
                                             'COMMENTS': {'$elemMatch': {'BuyerName': comment['BuyerName'], 'Date': comment['Date']}}
                                             })
                # print('--------------exist---------------')
                # # print(exist)
                if exist is None:
                    # print('exist is None')
                    self.db_doc.update_one({'GOODS_ID': item['GOODS_ID']},
                                           {'$push':   {'COMMENTS': comment}},
                                           upsert=False,    # perform an insert if no documents match the filter
                                           )
        # return item

    def readdb(self):
        result = self.db_doc.find_one({'GOODS_ID': '44236805503'})
        print(result)


class JDPipeline(object):
    def __init__(self):
        # 建立MongoDB连接
        db_connect = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        # 建立数据库
        db = db_connect[settings['MONGODB_DBNAME']]
        # 建立文档集合（表）
        self.db_doc = db[settings['JD_MONGODB_DOCNAME']]

    # spider打开时自动执行
    def open_spider(self, spider):
        pass

    # spider关闭时自动执行
    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # 合并同一个GOODS_ID下的信息，使用update()
        if 'GOODS_NAME' in dict(item).keys():  # 商品信息
            self.db_doc.update({'GOODS_ID': item['GOODS_ID']},
                                   {'$set':   {'GOODS_NAME':   item['GOODS_NAME'],
                                                'GOODS_URL':    item['GOODS_URL'],
                                                'TOTAL_COMMENT': item['TOTAL_COMMENT'],
                                                }
                                    },
                                   upsert=True,    # perform an insert if no documents match the filter
                                   )
        elif 'COMMENTS' in dict(item).keys():  # 评论追加
            for comment in item['COMMENTS']:
                # 如果数据库中不存在该评论，则添加；以买家和评论日期为准
                exist = self.db_doc.find_one({'GOODS_ID': item['GOODS_ID'],
                                             'COMMENTS': {'$elemMatch': {'BuyerName': comment['BuyerName'], 'Date': comment['Date']}}
                                             })
                if exist is None:
                    # print('Add new comments')
                    # print(comment)
                    self.db_doc.update_one({'GOODS_ID': item['GOODS_ID']},
                                           {'$push':   {'COMMENTS': comment}},
                                           upsert=False,    # perform an insert if no documents match the filter
                                           )
        # return item


class TaobaoPipeline(object):
    def __init__(self):
        # 建立MongoDB连接
        db_connect = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        # 建立数据库
        db = db_connect[settings['MONGODB_DBNAME']]
        # 建立文档集合（表）
        self.db_doc = db[settings['TAOBAO_MONGODB_DOCNAME']]

    # spider打开时自动执行
    def open_spider(self, spider):
        pass

    # spider关闭时自动执行
    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # 合并同一个GOODS_ID下的信息，使用update()
        if 'GOODS_NAME' in dict(item).keys():  # 商品信息
            self.db_doc.update({'GOODS_ID': item['GOODS_ID']},
                                   {'$set':   {'GOODS_NAME':   item['GOODS_NAME'],
                                                'GOODS_URL':    item['GOODS_URL'],
                                                'TOTAL_COMMENT': item['TOTAL_COMMENT'],
                                                }
                                    },
                                   upsert=True,    # perform an insert if no documents match the filter
                                   )
        elif 'COMMENTS' in dict(item).keys():  # 评论追加
            self.db_doc.update({'GOODS_ID': item['GOODS_ID']},     # item['COMMENTS']是list
                                    {'$push':   {'COMMENTS': {'$each': item['COMMENTS']}}},
                                    upsert=False,    # perform an insert if no documents match the filter
                                    )
        # return item


if __name__ == "__main__":
    # testdb = TmallPipeline()
    # testdb.readdb()
    db_connect = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
    # 建立数据库
    db = db_connect['test']
    # 建立文档集合（表）
    db_doc = db['test']
    db_doc.drop()
    a = { 'user':1,
          'test': ['zld','LL'],
        'profile_set' :
          [
            { 'name' : 'nick', 'options' : 0 },
            { 'name' : 'joe',  'options' : 2 },
            { 'name' : 'burt', 'options' : 1 }
          ]
        }
    db_doc.insert(a)

    re = db_doc.find_one({'user':2})
    print(re)

    # print(db_doc.find_one())
    # add_array = [{ 'name' : 'nick', 'options' : 0 }, { 'name' : 'zld', 'options' : 0 }]
    # db_doc.update_one({'user':1},     # item['COMMENTS']是list
    #                    {'$addToSet':   {'profile_set':  {'$each':add_array}}},      # $addToSet会自动排重
    #                    upsert=True,    # perform an insert if no documents match the filter
    #                    )
    # db_doc.update_one({'user':1},     # item['COMMENTS']是list
    #                    {'$addToSet':   {'test':  'zld--'}},      # $addToSet会自动排重
    #                    upsert=True,    # perform an insert if no documents match the filter
    #                    )
    print(db_doc.find_one())

