#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: zhangliangdian@qq.com
@license: Apache Licence
@file: ExportFromDB.py
@time: 2017/9/15 0:04 
"""

import pymongo
from ECRspider import settings
import xlsxwriter as wx


class ExportToExcel(object):
    def __init__(self, host, port, db_name, doc_name, file_name):
        # 建立MongoDB连接
        db_connect = pymongo.MongoClient(host=host, port=port)
        # 建立数据库
        db = db_connect[db_name]
        # 建立文档集合（表）
        self.db_doc = db[doc_name]
        self.excel_file_name = file_name
        pass

    def all_to_excel(self):
        self.open_excel_file()
        item_iter = self.db_doc.find()  # 生成一个迭代器
        for item in item_iter:  # 每一个item是一个商品
            self.write_item_to_excel(item)
        self.close_excel_file()

    def open_excel_file(self):
        self.workbook = wx.Workbook(self.excel_file_name)

    def close_excel_file(self):
        self.workbook.close()

    def write_item_to_excel(self, item):
        worksheet = self.workbook.add_worksheet(item['GOODS_ID'])  # 创建一个工作表对象
        # ---------------- 设置字体格式与列宽---------------
        title_style = self.workbook.add_format(
            {'font_color': 'white', 'border': 1, 'align': 'center', 'bg_color': '800000', 'font_size': 11,
             'font_name': '微软雅黑', 'bold': True})
        body_style = self.workbook.add_format(
            {'border': 1, 'align': 'left', 'bg_color': 'white', 'font_size': 11, 'font_name': '微软雅黑',
             'text_wrap': True})
        info_body_style = self.workbook.add_format(
            {'border': 1, 'align': 'left', 'bg_color': 'white', 'font_size': 11, 'font_name': '微软雅黑'})


        # ---------------- 写商品信息 --------------------
        worksheet.write(0, 0, '商品名称', title_style)
        worksheet.write(0, 1, item['GOODS_NAME'], info_body_style)
        worksheet.write(1, 0, '商品链接', title_style)
        worksheet.write(1, 1, item['GOODS_URL'], info_body_style)
        worksheet.write(2, 0, '评价总数', title_style)
        worksheet.write(2, 1, item['TOTAL_COMMENT'], body_style)

        # --------------- 写评论 ----------------------
        title_list = ['买家昵称',  '评论时间', '评论内容', '几天后追评', '追评内容']
        width_list = [10, 20, 50, 10, 50]
        for col_idx in range(0, len(title_list)):
            worksheet.write(4, col_idx, title_list[col_idx], title_style)
            worksheet.set_column(col_idx, col_idx, width_list[col_idx])  # 设定列的宽度

        start_line = 5
        comment_key_list = ['BuyerName', 'Date', 'Content', 'AppendDays', 'AppendComment']
        if 'COMMENTS' in item.keys():
            for comment in item['COMMENTS']:
                for col_idx in range(0, len(comment_key_list)):
                    worksheet.write(start_line, col_idx, comment[comment_key_list[col_idx]], body_style)
                start_line += 1


if __name__ == "__main__":
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

    pass