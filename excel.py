#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Abstract: excel operation

import os
import random
import string
import datetime
from cStringIO import StringIO

import xlrd
import xlwt


def to_str(s):
    '''
    数据转utf8
    '''
    if isinstance(s, unicode):
        return s.encode("utf-8")
    return s


class Excel(object):
    '''
    excel processing
    '''

    def __init__(self, home='/tmp', trans=None):
        self.home = home
        self.trans = trans

    def load(self, file_name):
        '''
        assume the first line is title
        file_name: file name
        '''
        title, data = [], []
        work_book = xlrd.open_workbook(file_name)
        sheet = work_book.sheet_by_index(0)
        for c in xrange(sheet.ncols):
            title.append(sheet.cell(0, c).value)
        for r in xrange(1, sheet.nrows):
            unit = {}
            for c in xrange(sheet.ncols):
                unit[title[c]] = sheet.cell(r, c).value
            data.append(unit)
        return data

    def load2(self, head, file_name=None, body=None):
        '''
            加载excel
            @head 标题头
            @file_name 文件名
            @body 文件数据
        '''
        if file_name is None and body is None:
            raise Exception("No file name or body")
        # 如果没有文件,则根据body写入文件
        if file_name is None:
            file_name = self.tmp_filename()
            with open(file_name, 'w+b') as codefp:
                codefp.write(body)
        title, data = [], []
        work_book = xlrd.open_workbook(file_name)
        sheet = work_book.sheet_by_index(0)
        for c in xrange(sheet.ncols):
            title.append(sheet.cell(0, c).value)
        for r in xrange(1, sheet.nrows):
            unit = {}
            for c in xrange(sheet.ncols):
                for k, v in head:
                    if title[c].encode('utf-8') == v:
                        cell = sheet.cell(r, c)
                        # 如果是日期类型
                        if cell.ctype == xlrd.XL_CELL_DATE:
                            unit[k] = to_str(self._get_date(cell.value))
                        else:
                            unit[k] = to_str(cell.value)
            data.append(unit)
        os.remove(file_name)
        return data

    def get_titles(self, file_path):
        """"""
        title = []
        work_book = xlrd.open_workbook(file_path)
        sheet = work_book.sheet_by_index(0)
        for c in xrange(sheet.ncols):
            title.append(sheet.cell(0, c).value)
        return title

    def tmp_filename(self):
        return os.path.join(self.home,
                            ''.join(random.sample(string.lowercase, 10)))

    def _get_date(self, vtime):
        '''
            excel日期处理
        '''
        if isinstance(vtime, float):
            vtime = int(vtime)
        s_date = datetime.date(1899, 12, 31).toordinal() - 1
        d = datetime.date.fromordinal(s_date + vtime)
        return d.strftime("%Y-%m-%d")

    def generate(self, title, data, sep=1,
                 callback=None, time_format='%Y-%m-%d'):
        '''
        generate excel content
        title: excel title
        data: data result，list
        sep: width ratio
        '''
        work_book = xlwt.Workbook('UTF-8')
        sheet = work_book.add_sheet('sheet', True)
        ncols = len(title)
        # write title
        title_style = self.get_title_style()
        for j in xrange(ncols):
            sheet.col(j).width = 3333 * sep
            sheet.write(0, j, title[j][1], title_style)
        nrows = len(data)
        text_style = self.get_text_style()
        for i in xrange(nrows):
            for j in xrange(ncols):
                key = title[j][0]
                val = callback(data[i], key) if callback else data[i].get(key, '')
                val = self.trans_to_name(key, val)
                if isinstance(val, datetime.datetime):
                    val = val.strftime(time_format)
                sheet.write(i + 1, j, val, text_style)

        output = StringIO()
        work_book.save(output)
        output.seek(0)
        return output.read()

    def get_title_style(self):
        '''
        excel title style
        '''
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        style.font = font
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        style.alignment = alignment
        return style

    def get_text_style(self):
        '''
        excel text style
        '''
        style = xlwt.XFStyle()
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        style.alignment = alignment
        return style

    def trans_to_name(self, key, value):
        result = value
        # 对问题类型特殊处理
        if key == "err_type":
            book_error_dict = self.trans[key]
            if value:
                error_types = [x for x in value.split(",") if x]
                result = "错误类型如下:"
                for x in xrange(len(error_types)):
                    result = "%s%s:%s;" % (result,
                                           x+1,
                                           book_error_dict.get(error_types[x],
                                                               ""))
            return result
        if self.trans and self.trans.get(key, None):
            trans_dict = self.trans[key]
            result = trans_dict.get(str(value), value)
        return result


if __name__ == '__main__':
    title = [('name', '姓名'), ('age', '年龄'), ('gender', '性别')]
    data = [{'name': 'liangsix', 'age': 10, 'gender': '男'},
            {'name': '梁六', 'age': 12, 'gender': '男'}]
    f = open('test.xls', 'wb')
    f.write(Excel().generate(title, data))
    f.close()
