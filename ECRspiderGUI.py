#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: zhangliangdian@qq.com
@license: Apache Licence
@file: ECRspiderGUI.py
@time: 2017/9/19 13:46 
"""
import tkinter as tk
from KeyWordsStatics import KeyWordsStatics
from ExportFromDB import ExportToExcel
from ECRspider import settings
import scrapy
from ECRspider.EricOtherClass import Timer
import threading
import os
import pymongo

# ----------------------- 用于参数设置的GUI ----------------------
class ECRspiderGUI(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GUI for ECRspider V0.04:  zhangld@landicorp.com")
        self.create_introduction_widgets()
        self.create_cookies_widgets()
        self.create_spider_widgets()
        self.create_auto_process_widgets()
        self.create_statics_widgets()
        self.create_export_widgets()
        self.create_db_widgets()
        tk.Label(self.root, text='').grid(row=6, column=0, columnspan=4)
        # root.geometry('300x200')
        # # 运行数据库
        # 建立MongoDB连接
        db_connect = pymongo.MongoClient(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
        # 建立数据库
        self.db = db_connect[settings.MONGODB_DBNAME]

    def run(self):
        self.root.mainloop()

    def quit(self):
        scrapy.exceptions.CloseSpider(reason='cancelled')

    # ---- 简要说明
    def create_introduction_widgets(self):
        intro_labelfram = tk.LabelFrame(self.root, text='简要说明')
        intro_labelfram.grid(padx=30, pady=3, ipady=5)
        label_text = '''用于抓取天猫、京东、淘宝上的商品评论的爬虫程序，基于Python + Scrapy + MongoDB实现。
相关文件说明如下：
1. good_urls.txt：在其中写入需要爬取的商品链接，每行一个；
2. NegativeKeywords.xlsx：进行“差评”筛选的关键词； PositiveKeywords.xlsx：进行“好评”筛选的关键词；
3. NegativeReviewsResult.xlsx：“差评”筛选和统计结果；  PositiveReviewsResult.xlsx：“好评”筛选和统计结果；
4. xx_Comments.xlsx：从数据库中导出的评论的excel文件，xx指Tmall、JD等；
5. 由于电商网站对爬虫敏感，在使用爬虫前，先用自己账号登录对应网站，在浏览器中将其cookie拷贝到setting.py文件或下面的输入框中，
   通常cookie的有效期只有几天。'''
        tk.Label(intro_labelfram, text=label_text, justify=tk.LEFT, borderwidth=1).grid(padx=10)

    # ---- 更新cookies
    def create_cookies_widgets(self):
        cookie_labelfram = tk.LabelFrame(self.root, text='更新cookies')
        cookie_labelfram.grid(row=1, padx=30, pady=3, sticky=tk.NW)
        # ------
        label_text = 'cookies的有效期通常只有几天，如果需要更新，请在如下输入框内填写新的cookies'
        tk.Label(cookie_labelfram, text=label_text).grid(row=0, column=0, columnspan=3)
        # ------
        tk.Label(cookie_labelfram, text='天猫的cookie: ').grid(row=1, column=0)
        self.tmall_cookie_entry = tk.Entry(cookie_labelfram, width=83)
        self.tmall_cookie_entry.grid(row=1, column=1)
        tk.Button(cookie_labelfram, text='  更新天猫  ', command=self.update_tmall_cookie).grid(row=1, column=2, padx=10)
        # ------
        tk.Label(cookie_labelfram, text='京东的cookie: ').grid(row=2, column=0)
        self.jd_cookie_entry = tk.Entry(cookie_labelfram, width=83)
        self.jd_cookie_entry.grid(row=2, column=1)
        tk.Button(cookie_labelfram, text='  更新京东  ', command=self.update_jd_cookie).grid(row=2, column=2, padx=10)
        # ------
        tk.Button(cookie_labelfram, text='  ----- 更新全部 -----  ', command=self.update_all_cookie).grid(row=3, columnspan=3, padx=10, pady=3)

    # ---- 启动爬虫
    def create_spider_widgets(self):
        spider_labelfram = tk.LabelFrame(self.root, text='启动爬虫')
        spider_labelfram.grid(row=2, padx=30, pady=3, sticky=tk.NW)
        # -------
        label_text = ' 如果需要重新爬取商品评论数据，请点击对应按键；新增评论会被追加到数据库中；       ' \
                     '                                                                   '
        tk.Label(spider_labelfram, text=label_text).grid(row=0, column=0, columnspan=3)
        # -------
        tk.Button(spider_labelfram, text='  ----- 爬取全部 -----  ', command=self.crawl_all_spider).grid(row=1, column=0, padx=10, pady=3)
        tk.Button(spider_labelfram, text='  爬取天猫评论  ', command=self.crawl_tmall_spider).grid(row=1, column=1, padx=10)
        tk.Button(spider_labelfram, text='  爬取京东评论  ', command=self.crawl_jd_spider).grid(row=1, column=2, padx=10)

    # ---- 自动处理
    def create_auto_process_widgets(self):
        tk.Button(self.root, text='自动处理\r\n爬取完毕后，自动统计与导出', command=self.auto_process).grid(row=2, column=1, padx=10, pady=3)

    # ---- 统计评论
    def create_statics_widgets(self):
        statics_labelfram = tk.LabelFrame(self.root, text='统计评论（差评和好评）')
        statics_labelfram.grid(row=3, padx=30, pady=3, sticky=tk.NW)
        # -------
        label_text = '点击按键，将对爬取到的评论数据进行关键词分析，结果保存到数据库及NegativeReviewsResult.xlsx或PositiveReviewsResult.xlsx文件中  '
        tk.Label(statics_labelfram, text=label_text).grid(row=0, column=0, columnspan=3)
        tk.Button(statics_labelfram, text='  ----- 统计全部 -----  ', command=self.statics_all).grid(row=1, column=0, padx=10, pady=3)
        tk.Button(statics_labelfram, text='  统计差评   ', command=self.statics_negative).grid(row=1, column=1, padx=10, pady=3)
        tk.Button(statics_labelfram, text='   统计好评   ', command=self.statics_positive).grid(row=1, column=2, padx=10, pady=3)

    # ---- 导出商品信息及原始评论数据
    def create_export_widgets(self):
        statics_labelfram = tk.LabelFrame(self.root, text='导出数据')
        statics_labelfram.grid(row=4, padx=30, pady=3, sticky=tk.NW)
        # -------
        label_text = ' 点击“导出数据”按键，将把数据库中爬取的商品信息及评论数据导出到 xx_Comments.xlsx 文件中                                     '
        tk.Label(statics_labelfram, text=label_text).grid(row=0, column=0)
        tk.Button(statics_labelfram, text='  ----- 导出数据 -----  ', command=self.export_data).grid(row=1, column=0, padx=10, pady=3)

    # ---- 数据库删除
    def create_db_widgets(self):
        statics_labelfram = tk.LabelFrame(self.root, text='数据删除（慎重）')
        statics_labelfram.grid(row=5, padx=30, pady=3, sticky=tk.NW)
        # -------
        label_text = '  数据库中的数据是追加的，当旧数据不再用时，可以点击“删除”按键删除数据库中对应内容                                              '
        tk.Label(statics_labelfram, text=label_text).grid(row=0, column=0, columnspan=4)
        tk.Button(statics_labelfram, text='  删除天猫评论数据  ', command=self.delete_tmall_db_doc).grid(row=1, column=0, padx=10, pady=3)
        tk.Button(statics_labelfram, text='  删除京东评论数据  ', command=self.delete_jd_db_doc).grid(row=1, column=1, padx=10, pady=3)
        tk.Button(statics_labelfram, text='  删除筛选结果  ', command=self.delete_filted_db_doc).grid(row=1, column=2, padx=10, pady=3)
        tk.Button(statics_labelfram, text='  ----- 全部删除 -----  ', command=self.delete_all_db_doc).grid(row=1, column=3, padx=10, pady=3)

# ----------------------------- 更新cookie的函数
    def update_tmall_cookie(self):
        tmall_cookie = self.tmall_cookie_entry.get()
        if tmall_cookie == '':
            print('cookie不能为空')
            return
        if len(tmall_cookie.split('\n')) > 1:
            print('cookie只能是单行，请检查')
            return
        # -------- 文件读取
        with open('ECRspider/settings.py', 'r', encoding='utf-8') as file:
            content_lines = file.read().split('\n')
        # -------- 文本处理
        new_content = ''
        for content_per_line in content_lines:
            if len(content_per_line) > 16:
                if content_per_line[0:16] == 'TMALL_COOKIES = ':    # 查找并替换
                    new_content += 'TMALL_COOKIES = "' + tmall_cookie + '"\n'
                else:
                    new_content += content_per_line + '\n'
            else:
                new_content += content_per_line + '\n'
        # ------- 文件写入
        with open('ECRspider/settings.py', 'w', encoding='utf-8') as file:
            file.write(new_content)
        print('tmall.com的cookies更新完成！')

    def update_jd_cookie(self):
        jd_cookie = self.jd_cookie_entry.get()
        if jd_cookie == '':
            print('cookie不能为空')
            return
        if len(jd_cookie.split('\n')) > 1:
            print('cookie只能是单行，请检查')
            return
        # -------- 文件读取
        with open('ECRspider/settings.py', 'r', encoding='utf-8') as file:
            content_lines = file.read().split('\n')
        # -------- 文本处理
        new_content = ''
        for content_per_line in content_lines:
            if len(content_per_line) > 13:
                if content_per_line[0:13] == 'JD_COOKIES = ':    # 查找并替换
                    new_content += 'JD_COOKIES = "' + jd_cookie + '"\n'
                else:
                    new_content += content_per_line + '\n'
            else:
                new_content += content_per_line + '\n'
        # ------- 文件写入
        with open('ECRspider/settings.py', 'w', encoding='utf-8') as file:
            file.write(new_content)
        print('jd.com的cookies更新完成！')

    def update_all_cookie(self):
        self.update_tmall_cookie()
        self.update_jd_cookie()

# ----------------------------- 开始爬取的函数（爬虫会导致界面长时间卡死，要开线程做）
    def crawl_tmall_spider(self):
        timer = Timer()
        timer.print_now_time()
        os.system('scrapy crawl TmallSpider -s LOG_FILE=ScrapyLog.txt')
        print('天猫爬取完成！用时 ' + str(timer.time_consum()) + ' 秒')

    def crawl_jd_spider(self):
        timer = Timer()
        timer.print_now_time()
        os.system('scrapy crawl JDSpider -s LOG_FILE=ScrapyLog.txt')
        print('京东爬取完成！用时 ' + str(timer.time_consum()) + ' 秒')

    def crawl_all_spider(self):
        self.crawl_tmall_spider()
        self.crawl_jd_spider()
        print('天猫和京东爬取都已完成！')

# ----------------------------- 自动处理，爬取完成后，自动统计并导出数据
    def auto_process(self):
        self.crawl_all_spider()
        self.statics_all()
        self.export_data()

# ----------------------------- 筛选评论
    def statics_negative(self):
        inst_static = KeyWordsStatics(keyword_file='NegativeKeywords.xlsx', result_db=settings.Neg_MONGODB_DOCNAME)
        inst_static.static('NegativeReviewsResult.xlsx')

    def statics_positive(self):
        inst_static = KeyWordsStatics(keyword_file='PositiveKeywords.xlsx', result_db=settings.Pos_MONGODB_DOCNAME)
        inst_static.static('PositiveReviewsResult.xlsx')

    def statics_all(self):
        self.statics_negative()
        self.statics_positive()

# ----------------------------- 原始评论导出
    def export_data(self):
        print('正在将MongoDB中的数据导出到Excel中...')
        # ----------- 导出天猫数据 --------------------
        inst_ExportToExcel = ExportToExcel(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT,
                                           db_name=settings.MONGODB_DBNAME, doc_name=settings.TMALL_MONGODB_DOCNAME,
                                           file_name='Tmall_Comments.xlsx')
        inst_ExportToExcel.all_to_excel()
        # ----------- 导出京东数据 --------------------
        inst_ExportToExcel = ExportToExcel(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT,
                                           db_name=settings.MONGODB_DBNAME, doc_name=settings.JD_MONGODB_DOCNAME,
                                           file_name='JD_Comments.xlsx')
        inst_ExportToExcel.all_to_excel()
        print('导出完成！')

# ----------------------------- 数据库操作
    def delete_tmall_db_doc(self):
        self.db[settings.TMALL_MONGODB_DOCNAME].drop()
        print('天猫原始评论数据已经删除！')

    def delete_jd_db_doc(self):
        self.db[settings.JD_MONGODB_DOCNAME].drop()
        print('京东原始评论数据已经删除！')

    def delete_filted_db_doc(self):
        self.db[settings.Neg_MONGODB_DOCNAME].drop()
        self.db[settings.Pos_MONGODB_DOCNAME].drop()
        print('筛选结果数据已经删除！')

    def delete_all_db_doc(self):
        self.db[settings.TMALL_MONGODB_DOCNAME].drop()
        self.db[settings.JD_MONGODB_DOCNAME].drop()
        self.db[settings.Neg_MONGODB_DOCNAME].drop()
        self.db[settings.Pos_MONGODB_DOCNAME].drop()
        print('所有数据都已删除！')


if __name__ == '__main__':
    inst_ECRspiderGUI = ECRspiderGUI()
    inst_ECRspiderGUI.run()
    inst_ECRspiderGUI.quit()
    print('-----------ECRspider 运行结束-------------')
