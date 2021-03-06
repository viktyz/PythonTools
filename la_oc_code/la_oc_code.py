#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Created by Alfred Jiang 2017-06-17

import getopt
import re
import sys

from enum import Enum


def special(char):
    if char.isdigit() or char.isalpha() or char == '_':
        return False
    else:
        return True


class States(Enum):
    origin = 0
    not_special_char = 1  # 非特殊符号


class DFA:
    content = ''  # 文件内容
    c_state = States
    state = 0  # 状态
    file_path = ''

    char_message = []  # 识别的字符串,存储元组,元组第一个参数是类型,第二个参数是该字符串

    def __init__(self, file):

        self.file_path = file;
        self.state = self.c_state.origin.value
        self.char_message = []

    def start_convert(self):
        try:
            file_object = open(self.file_path, 'r')
            self.content = file_object.read()
            print('Scanning : ' + self.file_path)
        except:
            print('Failed to Read File (Please check encoding): ' + self.file_path)
            return
        finally:
            file_object.close()

        self.remove_comment()
        self.remove_line_break()
        self.remove_duplicate_space()

        string = ''
        content_length = len(self.content)
        i = 0

        while i < content_length:
            ch = self.content[i]  # 读取该行的一个字符
            i += 1
            if self.state == self.c_state.origin.value:  # 初始状态
                string = ch

                if special(ch):

                    t_info = ('特殊符号', string)
                    self.char_message.append(t_info)
                    string = ''
                else:
                    self.state = self.c_state.not_special_char.value
                    string = ''
                    i -= 1

            elif self.state == self.c_state.not_special_char.value:

                while not special(ch):
                    string += ch
                    if i < content_length:
                        ch = self.content[i]
                        i += 1
                    else:
                        break

                if len(string) != 0:
                    t_info = ('字符串', string)
                    self.char_message.append(t_info)
                    string = ''

                if i != content_length:
                    self.state = self.c_state.origin.value
                    i -= 1

    def get_char(self):  # 获取识别信息
        return self.char_message

    def remove_duplicate_space(self):
        self.content = re.sub(' +', ' ', self.content)

    def remove_comment(self):
        self.content = re.sub("(/\*(\s|.)*?\*/)|(//.*)", "", self.content)

    def remove_line_break(self):
        self.content = re.sub("\n", " ", self.content)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'h:p:',
                                   ['path='])
    except getopt.GetoptError:
        print(
            'usage: \n'
            '\n'
            '$ python la_oc_code.py -p file_path\n'
            '\n'
            '-p <optional : input file path>\n'
        )
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(
                'usage: \n'
                '\n'
                '$ python la_oc_code.py -p file_path\n'
                '\n'
                '-p <optional : input file path>\n'
            )
            sys.exit()
        elif opt == '-p':
            project_path = arg

    print('\n===========================\n')

    dfa = DFA(project_path)

    dfa.start_convert()

    content = dfa.get_char()
    for item in content:
        print(item)

    print('\n')


if __name__ == '__main__':
    main(sys.argv[1:])
