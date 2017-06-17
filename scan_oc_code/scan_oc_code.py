#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Created by Alfred Jiang 2017-06-17

import re
from enum import Enum


class States(Enum):
    origin = 0

    start_sharp = 1
    start_at = 2
    start_dqm = 3
    start_import = 4

    start_import_dqm = 3001
    start_import_lt = 3002
    start_import_dqm_end = 3003
    start_import_rt = 3004

    n_c_string = 1000
    n_c_number_1 = 1001
    n_c_number_2 = 1002
    n_c_array = 1003
    n_c_dictionary = 1004
    n_c_keyword = 1005

    n_c_space = 1006

    s_string = 2001
    s_number_1 = 2002
    s_number_2 = 2003
    s_array = 2004
    s_dictionary = 2005
    s_keyword = 2006

    s_sharp = 2007

OC_IMPORT_LIST = [
    "#import",
    "#include",
    "#if",
    "#elif",
    "#endif"
]

OC_KEYWORD_LIST_1 = [
    "@implementation",
    "@interface",
    "@protocol",
    "@encode",
    "@synchronized",
    "@selector",
    "@end",
    "@defs",
    "@class",
    "@try",
    "@throw",
    "@catch",
    "@finally",
    "@private",
    "@package",
    "@public",
    "@protected",
    "@property",
    "@synthesize",
    "@dynamic",
    "@optional",
    "@required",
    "@autoreleasepool",
    "@compatibility_alias",
    "@"
]

OC_SEPARATOR_LIST = ['{', '}', '[', ']', '(', ')', '~', ',', ';', '.', '?', ':', ' ', '>', '<']

OC_OPERATOR_LIST = ['+', '++', '-', '--', '+=', '-=', '*', '*=', '%', '%=', '->', '|', '||', '|=', '/',
                    '/=', '>', '<', '>=', '<=', '=', '==', '!=', '!', '&']


class DFA:
    content = ''  # 文件内容
    line_number = 0  # 记录行号
    state = 0  # 状态
    c_state = States

    error_message = []  # 保存错误信息,存储元组,元组第一个参数是行号,第二个参数是错误字符
    annotate_message = []  # 注释信息,存储元组,元组第一个参数是行号,第二个参数是注释
    char_message = []  # 识别的字符串,存储元组,元组第一个参数是类型,第二个参数是该字符串

    def __init__(self, file_content):
        self.content = file_content
        self.state = 0
        self.line_number = 0
        self.error_message = []
        self.annotate_message = []
        self.char_message = []

    def start_convert(self):

        self.remove_comment()
        self.remove_line_break()
        self.remove_duplicate_space()

        lines = self.content.split('\n')

        string = ''
        for line in lines:  # 一行行的处理
            self.line_number += 1  # 每处理一行行号加一
            line_length = len(line)
            i = 0

            while i < line_length:
                ch = line[i]  # 读取该行的一个字符
                i += 1
                if self.state == self.c_state.origin.value:  # 初始状态
                    string = ch

                    if ch == '@':
                        self.state = self.c_state.start_at.value
                    elif ch == '#':
                        self.state = self.c_state.start_sharp.value
                    elif ch == '"':
                        self.state = self.c_state.start_dqm.value
                    elif ch.isspace():
                        self.state = self.c_state.n_c_space.value

                elif self.state == self.c_state.start_sharp.value:

                    while ch.isalpha():
                        string += ch
                        if i < line_length:
                            ch = line[i]
                            i += 1
                        else:
                            break
                    self.state = self.c_state.s_sharp.value

                elif self.state == self.c_state.s_sharp.value:

                    if string in OC_IMPORT_LIST:

                        t_info = '(引用关键字,' + string + ')'
                    else:
                        t_info = '(待确认,' + string + ')'

                    self.char_message.append(t_info)
                    string = ''  # 回到初始情况
                    self.state = self.c_state.start_import.value  # 回到状态
                    i -= 2

                elif self.state == self.c_state.start_import.value:

                    if ch == '"':
                        self.state = self.c_state.start_import_dqm.value
                    elif ch == '<':
                        self.state = self.c_state.start_import_lt.value

                elif self.state == self.c_state.start_import_dqm.value:

                    while ch != '"':
                        string += ch
                        if i < line_length:
                            ch = line[i]
                            i += 1
                        else:
                            break
                    self.state = self.c_state.start_import_dqm_end.value
                    i -= 1

                elif self.state == self.c_state.start_import_dqm_end.value:

                    if string == '/':
                        print('error')

                    t_info = '(引用内容,' + string + ')'
                    self.char_message.append(t_info)
                    string = ''  # 回到初始情况
                    self.state = self.c_state.origin.value  # 回到状态

                elif self.state == self.c_state.start_import_lt.value:

                    while ch != '>':
                        string += ch
                        if i < line_length:
                            ch = line[i]
                            i += 1
                        else:
                            break
                    self.state = self.c_state.start_import_rt.value
                    i -= 1

                elif self.state == self.c_state.start_import_rt.value:

                    if string == '/':
                        print('error')

                    t_info = '(引用内容,' + string + ')'
                    self.char_message.append(t_info)
                    string = ''  # 回到初始情况
                    self.state = self.c_state.origin.value  # 回到状态

                elif self.state == self.c_state.n_c_space.value:

                    while ch.isspace():
                        if i < line_length:
                            ch = line[i]
                            i += 1
                        else:
                            break
                    self.state = self.c_state.origin.value  # 回到状态
                    i -= 1

                elif self.state == self.c_state.start_at.value:  # @开头

                    if ch == '"':
                        self.state = self.c_state.n_c_string.value  # 字符串 - 备选
                    elif ch.isdigit:
                        self.state = self.c_state.n_c_number_1.value  # Number - 备选
                    elif ch == '(':
                        self.state = self.c_state.n_c_number_2.value  # Number - 备选
                    elif ch == '[':
                        self.state = self.c_state.n_c_array.value  # Array - 备选
                    elif ch == "{":
                        self.state = self.c_state.n_c_dictionary.value  # Dictionary - 备选
                    elif ch.isalpha:
                        self.state = self.c_state.n_c_keyword.value  # 关键字 - 备选
                    else:
                        self.state = self.c_state.origin.value  # 未知，恢复初始

                elif self.state == self.c_state.n_c_string.value:

                    pch = line[(i - 2)]

                    while not (ch == '"' and pch != '\\'):
                        string += ch
                        if i < line_length:
                            ch = line[i]
                            i += 1
                        else:
                            break

                    if i > line_length:
                        self.state = self.c_state.origin.value  # 未知，恢复初始
                    elif ch == '"':
                        self.state = 8  # 关键字 - 确认

    def get_error(self):  # 获取错误信息
        return self.error_message

    def get_annotate(self):  # 获取注释信息
        return self.annotate_message

    def get_char(self):  # 获取识别信息
        return self.char_message

    def remove_duplicate_space(self):

        self.content = re.sub(' +', ' ', self.content)

    def remove_comment(self):

        self.content = re.sub("(/\*(\s|.)*?\*/)|(//.*)", "", self.content)

    def remove_line_break(self):

        self.content = re.sub("\n", " ", self.content)


if __name__ == '__main__':

    file_object = open("/Users/viktyz/Documents/Git/PythonTools/AFNetworking/AFHTTPSessionManager.m")
    dfa = DFA(file_object.read())
    dfa.start_convert()

    content = dfa.get_char()
    for item in content:
        print(item)
    content = dfa.get_annotate()
    for item in content:
        print(item)
    content = dfa.get_error()
    for item in content:
        print(item)

    file_object.close()
