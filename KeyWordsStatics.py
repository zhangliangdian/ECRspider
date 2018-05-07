#!/usr/bin/env python
# encoding: utf-8
#
"""
@version: ??
@author: zhangliangdian@gmail.com
@license: Apache Licence 
@file: KeyWordsStatics.py
@time: 2016/9/8 19:57
@description:
"""
import time
import xlrd
import xlsxwriter as wx
from ECRspider import settings
import pymongo
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

'''
用于存储筛选结果的数据 filted_summary 由多重List和Dict嵌套组成，结构较复杂，如下
总体是一个List，每个元素是一个Dict表示一个sheet
[
    { # sheet 1
        'ID':str
        'Title':str
        'Url':str
        'CommentNum':int
        'KeyCommentNum':int
        'FiltedData':  # 是多个Dict的List, 每个Dict表示一个关键词组的筛选结果
            [
                { # 关键词组1
                    'KeyWords': List of str
                    'Num': int
                    'Comment':
                        [   # 以条为单位的完整评论信息
                            [ # 评论1]
                            ...
                            [ # 评论n]
                        ]

                }
                ...
                {  #关键词组n
                }
            ]
    }
    ...
    {   # sheet n
        ...
    }
]
'''


class WriteToExcel(object):
    def __init__(self, filename):
        # 创建Excel文件用于存放爬取的评论
        self.filename = filename
        self.open_excel_file()
        pass

    def open_excel_file(self):
        # path = ''
        # try:
        #     os.makedirs(path)
        # except:
        #     pass
        self.workbook = wx.Workbook(self.filename)

    def close_excel_file(self):
        self.workbook.close()

    def write_to_excel(self, filted_db_doc):
        # ---------------- 设置字体格式与列宽---------------
        title_style = self.workbook.add_format(
            {'font_color': 'white', 'border': 1, 'align': 'center', 'bg_color': '800000', 'font_size': 11,
             'font_name': '微软雅黑', 'bold': True})
        body_style = self.workbook.add_format(
            {'border': 1, 'align': 'left', 'bg_color': 'white', 'font_size': 11, 'font_name': '微软雅黑',
             'text_wrap': True})
        info_body_style = self.workbook.add_format(
            {'border': 1, 'align': 'left', 'bg_color': 'white', 'font_size': 11, 'font_name': '微软雅黑'})

        # ------------------------------------ 评论数量汇总页（首页） -------------------------------------
        '''
        首页汇总各类评论的总数，页面结构如下：
        '商品ID'  '商品名称'  '网址'   '评论总数'  '包含关键词的评论总数'    各类关键词组名称...
        总结：                          队列求和总数     队列求和总数            队列求和总数
        商品信息1：
        商品信息2：
        ...
        '''
        summary_sheet = self.workbook.add_worksheet('统计')

        # ------ 从数据库中提取所有评论的描述
        db_item = filted_db_doc.find_one()
        description_list = []
        for keyword in db_item['KEYWORD']:
            description_list.append(keyword['Description'])

        # --------------------------------------------- 统计页的详单部分 ------------------------------------------
        detail_row_offset = 20  # 内容行，从第detail_row_offset行开始
        summary_sheet.write(detail_row_offset - 2, 0, '注：点击商品ID可跳转到对应sheet', body_style)
        summary_sheet.write(detail_row_offset - 1, 0, '详细次数统计如下：', body_style)

        # ---- 填写标题栏
        column_title = ['商品ID', '商品名称', '网址', '评论总数', '包含关键词的评论总数']
        column_title += description_list
        for idx_column in range(0, len(column_title)):
            summary_sheet.write(detail_row_offset, idx_column, format('%s' % column_title[idx_column]), title_style)
        # 设置列宽
        summary_sheet.set_column(0, len(column_title), 30)  # 设定列的宽度为20
        # summary_sheet.set_column(0, 0, 40)  # 设定列的宽度为40
        # summary_sheet.set_column(2, 2, 60)  # 设定列的宽度为40

        # ---- 填写详单表格内容
        db_item_iter = filted_db_doc.find()
        row_idx = detail_row_offset+1
        sum_total_comment = 0   # 评论总数
        sum_keyword_cnt = 0     # 包含所有关键词的评论总数
        sum_cnt_per_keyword_list = [0]*len(description_list)    # 包含每个关键词组的所有商品的评论总数，数组
        for db_item in db_item_iter:
            row_idx += 1
            # 根据ID号超链接到相应sheet
            summary_sheet.write_url(row_idx, 0, format('internal:%s!A1' % db_item['GOODS_ID']))
            summary_sheet.write(row_idx, 0, db_item['GOODS_ID'], body_style)
            summary_sheet.write(row_idx, 1, db_item['GOODS_NAME'], body_style)
            summary_sheet.write(row_idx, 2, db_item['GOODS_URL'], info_body_style)
            summary_sheet.write(row_idx, 3, db_item['TOTAL_COMMENT'], body_style)
            sum_total_comment += db_item['TOTAL_COMMENT']
            col_idx = 4
            sum_cnt_per_goods = 0   # 包含所有关键词组的每个商品的评论总数
            # 填写每一行
            for keyword in db_item['KEYWORD']:  # 每个关键词组的评论次数
                col_idx += 1
                summary_sheet.write(row_idx, col_idx, keyword['CommentsNum'], body_style)
                sum_cnt_per_goods += keyword['CommentsNum']
                sum_cnt_per_keyword_list[col_idx-5] += keyword['CommentsNum']
            # 填写该行的“包含关键词的评论总数”列
            summary_sheet.write(row_idx, 4, sum_cnt_per_goods, body_style)
            sum_keyword_cnt += sum_cnt_per_goods


        # 填写“累计”行
        summary_sheet.write(detail_row_offset+1, 0, '累计', body_style)
        summary_sheet.write(detail_row_offset+1, 3, sum_total_comment, body_style)  # 评论总数
        summary_sheet.write(detail_row_offset+1, 4, sum_keyword_cnt, body_style)  # 包含关键词的评论总数
        col_idx = 4
        for sum_cnt_per_keyword in sum_cnt_per_keyword_list:
            col_idx += 1
            summary_sheet.write(detail_row_offset+1, col_idx, sum_cnt_per_keyword, body_style)  # 包含每个关键词组的所有商品的评论总数
        # ---------------------------------------------------------------------------------------

        # --------------------------------------------- 统计页的汇总部分 ------------------------------------------
        summary_sheet.write(0, 0, '收银机差评 TOP', title_style)
        summary_sheet.write(0, 1, '出现次数', title_style)
        keywords_sum_list = []
        for idx in range(len(description_list)):
            keywords_sum_list.append([description_list[idx], sum_cnt_per_keyword_list[idx]])
        # keywords_sum_list[ [‘关键词组1’, 次数1],...,[‘关键词组n’, 次数n],], 按次数由多到少排列
        keywords_sum_list.sort(key=lambda k: k[1], reverse=True)    # 按次数从大到小排序
        # 如果少于TOP_NUM个，则全列出，否则只列出TOP_NUM个
        TOP_NUM = 10
        if len(keywords_sum_list) < TOP_NUM:
            top_num_list = keywords_sum_list
        else:
            top_num_list = keywords_sum_list[0:TOP_NUM]
            other_list = keywords_sum_list[TOP_NUM:-1]  # 除了TOP之外，其余归入Others
            other_sum = 0
            for other in other_list:
                other_sum += other[1]
            top_num_list.append(['Others', other_sum])
        # 填入到Excel
        for idx in range(0, len(top_num_list)):
            summary_sheet.write(1 + idx, 0, format('%s' % top_num_list[idx][0]), body_style)
            summary_sheet.write(1 + idx, 1, top_num_list[idx][1], body_style)

        # --------------------------------------------- 统计页的图表绘制 ------------------------------------------
        # 绘制饼图
        top_pie_chart = self.workbook.add_chart({'type': 'pie'})
        # 添加数据
        top_pie_chart.add_series({
            # 'name': '差评关键词分布',
            'categories': ['统计', 1, 0, len(top_num_list), 0],
            'values': ['统计', 1, 1, len(top_num_list), 1],
            'data_labels': {'percentage': True}
        })
        # 添加标题
        top_pie_chart.set_title({'name': '各差评关键词组占比'})
        top_pie_chart.set_style(10)
        # 设置饼图绘图区域相对位置和相对尺寸
        top_pie_chart.set_plotarea({
            'layout': {
                'x':        0.05,
                'y':        0.17,
                'width':    0.4,
                'height':   0.75
            }
        })
        # 设置Legend属性
        top_pie_chart.set_legend({
            'font': {'size': 11},
            'layout': {
                'x':        0.48,
                'y':        0.17,
                'width':    0.5,
                'height':   0.8
            }
        })
        summary_sheet.insert_chart('C1', top_pie_chart, {'x_offset': 10, 'y_offset': 10, 'x_scale': 1.4, 'y_scale': 1.3})



        # ------------------------------------ 按sheet分页 -------------------------------------
        '''
        按sheet分页显示关键词检索类容，每个商品一个sheet，每个sheet格式如下
        '关键词1'：
                    评论1( 用户昵称，评论，评论时间，追评，几天后追评，商家回复 )
                    评论2
                    ...
        '关键词2'：
                    评论1
                    评论2
                    ...
        '''
        db_item_iter = filted_db_doc.find()
        for db_item in db_item_iter:
            detail_sheet = self.workbook.add_worksheet(db_item['GOODS_ID'])  # 创建以商品ID为名字的工作表对象
            # --------------- 页首商品信息 --------------
            detail_sheet.write(0, 0, '商品ID', title_style)
            detail_sheet.write(1, 0, '商品名称', title_style)
            detail_sheet.write(2, 0, '商品链接', title_style)
            detail_sheet.write(3, 0, '带关键词的评论总数', title_style)
            detail_sheet.write(0, 1, db_item['GOODS_ID'], info_body_style)
            detail_sheet.write(1, 1, db_item['GOODS_NAME'], info_body_style)
            detail_sheet.write(2, 1, db_item['GOODS_URL'], info_body_style)
            detail_sheet.write(3, 1, db_item['TOTAL_COMMENT'], info_body_style)
            # ---------------- 评论部分 ----------------
            row_index = 5
            # 填写第一行标题
            column_title = ['关键词描述', '用户昵称', '评论', '评论时间', '追评', '几天后追评', '商家回复']
            for idx_column in range(0, len(column_title)):
                detail_sheet.write(row_index, idx_column, column_title[idx_column], title_style)
            detail_sheet.set_column(0, len(column_title), 20)  # 设定列的宽度为30
            detail_sheet.set_column(2, 2, 60)  # 设定评论列的宽度为60
            detail_sheet.set_column(4, 4, 60)  # 设定评论列的宽度为60
            detail_sheet.set_column(6, 6, 60)  # 设定评论列的宽度为60

            for content_by_keyword in db_item['KEYWORD']:
                # ---- 有评论才填写关键词
                if content_by_keyword['CommentsNum'] > 0:
                    row_index += 1
                    # 在0列填写关键词
                    detail_sheet.write(row_index, 0, content_by_keyword['Description'], body_style)
                    # 填写筛选出的评论
                    for filted_comment in content_by_keyword['Comments']:
                        row_index += 1
                        detail_sheet.write(row_index, 1, filted_comment['BuyerName'], body_style)   #'用户昵称'
                        detail_sheet.write(row_index, 2, filted_comment['Content'], body_style)     #'评论'
                        detail_sheet.write(row_index, 3, filted_comment['Date'], body_style)        #'评论时间'
                        detail_sheet.write(row_index, 4, filted_comment['AppendComment'], body_style)   #'追评'
                        detail_sheet.write(row_index, 5, filted_comment['AppendDays'], body_style)      #'几天后追评'
                        # detail_sheet.write(row_index, 6, filted_comment['Reply'], body_style)       #'商家回复'
            row_index += 3      # 空行


class KeyWordsStatics(object):
    def __init__(self, keyword_file, result_db):
        self.comment_desc_keyw_none_list = self.read_keywords_from_excel(keyword_file)
        # 建立MongoDB连接
        db_connect = pymongo.MongoClient(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
        # 建立数据库
        db = db_connect[settings.MONGODB_DBNAME]
        # 建立文档集合（表）
        self.tmall_db_doc = db[settings.TMALL_MONGODB_DOCNAME]
        self.jd_db_doc = db[settings.JD_MONGODB_DOCNAME]
        self.filted_db_doc = db[result_db]

    def read_keywords_from_txt(self):
        print('------从TXT文件读取评论检索关键词--------')
        # 打开网址列表所在文件，中文类的，需要指明编码方式
        file = open('keywords.txt', 'r', encoding='utf-8')
        # 将评论分行
        keyWords_line = file.read().split('\n')
        # 去除UTF-8-BOM编码带来的首行开头的‘\ufeff’(中文连字符 '﻿')
        if keyWords_line[0][0] == '﻿':
            keyWords_line[0] = keyWords_line[0][1:]
        # 剔除注释行和空白行
        keyWords_line_filted = []
        for keyWord in keyWords_line:
            if keyWord is not '':
                if keyWord[0] != '#':
                    keyWords_line_filted.append(keyWord)

        # 将相近的词作为一类，返回值是List，其元素也是List，近义词组成一个元素List
        # 每行的内容如下：‘描述：容易死机和重启；		包含如下关键词：死机、重启、黑屏、蓝屏’
        keyWordsList_tmp = list(map(lambda x: x.split('；'), keyWords_line_filted))  # map结果是一个惰性迭代器，需要list()才能返回值
        # comment_desc_keyw 数据结构为[ ['描述1',[关键词组1]], ... , ['描述n',[关键词组n]] ]
        comment_desc_keyw = []    # 描述&关键词
        for idx in range( 0,len(keyWords_line_filted) ):
            _description = keyWordsList_tmp[idx][0].split('：')
            _description = _description[1]    # '容易死机和重启'
            _keywords = keyWordsList_tmp[idx][1].split('：')
            _keywords = _keywords[1].split('、')
            comment_desc_keyw.append( [_description, _keywords] )

        print(comment_desc_keyw)
        # return comment_desc_keyw

    def read_keywords_from_excel(self, excel_file):
        print('从Excel文件 %s 中读取评论检索关键词...' % excel_file)
        # 打开网址列表所在文件，中文类的
        excel_book = xlrd.open_workbook(excel_file)
        sheet_content = excel_book.sheet_by_name('keywords')
        num_of_row = sheet_content.nrows
        comment_desc_keyw_none_list = []    # 描述&关键词
        # 逐行读取
        for idx_row in range(4, num_of_row):
            row_data = sheet_content.row_values(idx_row)
            _description = row_data[1]
            _keywords = row_data[2].split('、')
            _non_keywords = row_data[3].split('、')
            comment_desc_keyw_none_list.append([_description, _keywords, _non_keywords])
        print('读取完成，共 %s 个关键词组！' % len(comment_desc_keyw_none_list))
        return comment_desc_keyw_none_list

    def filte_from_db(self, db_doc):
        # -------------------- 对每一件商品进行筛选 ------------------------------
        db_item_iter = db_doc.find()  # 生成一个迭代器
        for db_item in db_item_iter:  # 每一个item是一个商品
            # 可能因保存操作被中断等导致数据库中的db_item的某些Key缺失，直接引用会报错，故先判断
            if 'GOODS_NAME' not in db_item.keys():
                db_item['GOODS_NAME'] = ''
            if 'GOODS_URL' not in db_item.keys():
                db_item['GOODS_URL'] = ''
            if 'TOTAL_COMMENT' not in db_item.keys():
                db_item['TOTAL_COMMENT'] = 0

            self.filted_db_doc.update_one({'GOODS_ID': db_item['GOODS_ID']},
                                          {'$set': {'GOODS_NAME': db_item['GOODS_NAME'],
                                                    'GOODS_URL': db_item['GOODS_URL'],
                                                    'TOTAL_COMMENT': db_item['TOTAL_COMMENT'],
                                                    'KEYWORD': [],
                                                    }
                                           },
                                           upsert=True,    # perform an insert if no documents match the filter
                                          )

            # ------------------------ 对每一条评论描述进行筛选 ----------------------
            for comment_desc_keyw_none in self.comment_desc_keyw_none_list:  # 关键词组列表
                # 在数据库中新建评论的item
                filted_by_words = {'Description':   comment_desc_keyw_none[0],
                                    'HaveKeyWords': comment_desc_keyw_none[1],
                                    'HaveNoWords':  comment_desc_keyw_none[2],
                                    'Comments':     [],
                                   }
                # -------------------- 对每一条Comment进行筛选 ------------------------------
                # 可能因保存操作被中断等导致数据库中的db_item的某些Key缺失，直接引用会报错，故先判断
                if 'COMMENTS' in db_item.keys():
                    for comment in db_item['COMMENTS']:
                        if self.have_words(comment, comment_desc_keyw_none[1]) is True \
                                and self.have_words(comment, comment_desc_keyw_none[2]) is False:
                            # 得到过滤后的comment
                            filted_by_words['Comments'].append(comment)

                filted_by_words['CommentsNum'] = len(filted_by_words['Comments'])
                # 如果该商品评论中包含关键词，则存入数据库
                self.filted_db_doc.update_one({'GOODS_ID':     db_item['GOODS_ID']},
                                              {'$push':   {'KEYWORD': filted_by_words}},
                                               upsert=True,    # perform an insert if no documents match the filter
                                              )


    # 评论中是否包含指定词组，True:包含，False:不含
    def have_words(self, comment, keywords):
        if keywords == ['']:
            return False
        for word in keywords:
            if (word in comment['Content']) or (word in comment['AppendComment']):
                return True
        return False

    def static(self, result_filename):
        # 过滤关键词并存到数据库中
        self.filte_from_db(self.tmall_db_doc)
        self.filte_from_db(self.jd_db_doc)
        # 存储到Excel表中
        inst_excel = WriteToExcel(result_filename)
        inst_excel.write_to_excel(self.filted_db_doc)
        # 读取评论内容的Excel文件
        while True:
            try:
                inst_excel.close_excel_file()
                break
            except Exception as err:
                print(err)
                print('用于存储结果的 ' + result_filename + ' 文件已被打开，请先关闭该文件，并按回车键继续')
                input_word = input()
                if 'exit' in input():
                    break
        print('检索结果已经存储到 ' + result_filename + ' 文件中')

        # 分词 & 画词云
        # inst_cut_words = CutWords()
        # print('正在分词并绘制词云...')
        # inst_cut_words.cut_words(self.filted_db_doc)
        # print('词云绘制完成！')


class CutWords(object):
    def __init__(self):
        pass

    def cut_words(self, filted_db_doc):
        # 直接返回评论字段
        db_item_iter = filted_db_doc.find({}, {'_id': 0, 'KEYWORD.Comments.Content': 1, 'KEYWORD.Comments.AppendComment': 1})
        # ------------------ 提取评论数据到List中 ----------------
        # 由于同一条差评可能包含多个不同关键词，在filted_db_doc中会被多次存储，因此用set数据类型，自动滤除相同内容
        comment_word_set = set([])  # set格式，会自动滤除相同的内容
        for db_item in db_item_iter:
            for Comments in db_item['KEYWORD']:
                for Content in Comments['Comments']:
                    if Content['Content'] != '此用户没有填写评论!':
                        comment_word_set.add(Content['Content'])
                    if Content['AppendComment'] != '':
                        comment_word_set.add(Content['AppendComment'])
        word_list = list(comment_word_set)

        words = [' '.join(jieba.cut(ele)) for ele in word_list]
        new_words = ' '.join(words)
        # print(new_words)
        print("已完成分词，得到%s个词组" % len(new_words))

        # from PIL import Image
        # import numpy as np
        # pic_coloring = np.array(Image.open("cloud.jpg"))
        stopwords = set(["请问", "可以", "亲们", "收银机", "什么", "谢谢", "你们", "怎么样", "有没有", "这个", "大家",
                         "这款", "机器", "机子", "不会", "知道", "一下", "还是", "是不是", "好不好", "收银", "怎样",
                         "怎么", '客服', '就是', '他们', '问题'])
        # print(stopwords)
        wordcloud = WordCloud(font_path="C:\\Windows\\Fonts\\msyh.ttf",
                              background_color="black",
                              max_words=50,
                              stopwords=stopwords,
                              width=1000,
                              height=800,
                              # mask=pic_coloring,
                              ).generate(new_words)

        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()

def boot_words():
    head_words = '''
------------------------------------------------------------------
|                          差评统计程序          	             |
|  1. 本程序用于从评论中统计关键词组个数；                       |
|  2. 关键词组请在keywords_input.xlsx文件中编辑；                |
|  3. 结果存储在FiltedResult.xlsx文件中，请确保该文件已关闭；    |
|                      zhangld@landicorp.com                     |
------------------------------------------------------------------
	'''
    print(head_words)

if __name__ == '__main__':
    boot_words()
    time.clock()
    print('Now is ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    inst_static = KeyWordsStatics(keyword_file='keywords_input.xlsx')
    inst_static.static()
    print('Completed, Time Consuming = ' + str(time.clock()) + 'second')
