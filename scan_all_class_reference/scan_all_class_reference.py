#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Created by Alfred Jiang 2017-06-18

import getopt
import os
import sys
from enum import Enum

sys.path.append("..")
from la_oc_code.la_oc_code import DFA

OC_KEYWORDS = ['YES', 'NO', 'BOOL', 'TRUE', 'FALSE', 'NULL', 'IBOutlet']
OC_SDK_PREFIX = ['NS', 'UI', 'CF', 'CG', 'AL', 'PH', 'CV', 'CT', 'CA', 'AB', 'CA', 'MK', 'CL', 'AV', 'CC', 'CD']


# TEST_PREFIX = ['JD', 'MA', 'QQ', 'DD', 'FM', 'CJ', 'SD', 'AD', 'AF', 'AN', 'CH','SB','SH','SV']

class SectionStates(Enum):
    undefined_section = 0  # 未定义区域
    interface_section = 1  # interface 区域
    implement_section = 2  # implement 区域

    state_at = 3
    state_end = 4


class OCClass:
    root_dir = ''
    c_state = SectionStates
    class_list = []  # 所有疑似 class 列表
    class_info = {}  # 所有疑似 class 信息

    def __init__(self, directory):

        self.root_dir = directory

    def start_scan(self):

        self.filter_h_file_from_dir(self.root_dir)

    def filter_h_file_from_dir(self, directory):

        all_h_files = []

        for root, dirs, files in os.walk(directory):

            for item in files:

                filepath = os.path.join(root, item)

                extension = os.path.splitext(filepath)[1][1:]

                if extension == 'h':
                    all_h_files.append(filepath)

                    self.operation_with_h_file(filepath, root, item)

        return all_h_files

    def operation_with_list(self, t_list):

        # 找出所有疑似类

        state = self.c_state.undefined_section.value
        i = 0

        while i < len(t_list):

            item = t_list[i]
            ch = str(item[1])
            i += 1

            if state == self.c_state.undefined_section.value:

                if ch == '@':
                    state = self.c_state.state_at.value

            elif state == self.c_state.state_at.value:

                if ch == 'interface':

                    state = self.c_state.interface_section.value

                elif ch == 'implementation':

                    state = self.c_state.implement_section.value

                else:

                    state = self.c_state.undefined_section

            elif state == self.c_state.interface_section.value or state == self.c_state.implement_section.value:

                pre_ch = ''
                pre_2_ch = ''
                next_ch = ''
                next_2_ch = ''

                if i < len(t_list):
                    next_item = t_list[i]
                    next_ch = str(next_item[1])

                if (i + 1) < len(t_list):
                    next_2_item = t_list[(i + 1)]
                    next_2_ch = str(next_2_item[1])

                if i > 1:
                    pre_item = t_list[(i - 2)]
                    pre_ch = str(pre_item[1])

                if i > 2:
                    pre_2_item = t_list[(i - 3)]
                    pre_2_ch = str(pre_2_item[1])

                prefix = ch[0:2]

                if prefix.isupper() \
                        and prefix not in OC_SDK_PREFIX \
                        and ch[0].isalpha() \
                        and ch not in OC_KEYWORDS \
                        and not ch.isupper() \
                        and next_ch != ']' \
                        and next_ch != ':' \
                        and next_ch != '(' \
                        and next_ch != ')' \
                        and next_ch != '.' \
                        and next_ch != ';' \
                        and next_ch != ',' \
                        and next_2_ch != '=' \
                        and next_2_ch != ':' \
                        and next_2_ch != '&' \
                        and next_2_ch != '|' \
                        and pre_ch == ' ' \
                        and pre_2_ch != 'define' \
                        and pre_2_ch != 'protocol':
                    self.update_class_info(item)

    def update_class_info(self, item):

        class_name = item[1]

        if class_name in self.class_info.keys():
            class_item = self.class_info[class_name]
            class_item['count'] += 1
        else:
            dic = {
                'name': class_name,
                'count': 1
            }
            self.class_info[class_name] = dic

    def operation_with_h_file(self, filepath, p_path, h_name):
        '''

        获取全部 class 名
        :param filepath: .h 文件路径
        :return: 返回包含全部 class 名的数组
        '''

        m_name = os.path.splitext(h_name)[0] + '.m'
        m_filepath = os.path.join(p_path, m_name)

        t_list = []

        if os.path.exists(m_filepath):
            m_dfa = DFA(m_filepath)
            m_dfa.start_convert()
            t_list = m_dfa.get_char()

        h_dfa = DFA(filepath)
        h_dfa.start_convert()
        t_list.extend(h_dfa.get_char())

        self.operation_with_list(t_list)

    def get_class_list(self):  # 获取识别信息
        return self.class_list

    def get_reference(self, min_count=9999999):

        t_list = []
        for item_key in self.class_info.keys():
            item = self.class_info[item_key]
            if int(item['count']) <= min_count:
                t_list.append((item['name'], item['count']))

        return t_list


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'h:i:',
                                   ['inputproject='])
    except getopt.GetoptError:
        print(
            'usage: \n'
            '\n'
            '$ python oc_file_operation.py -i project_path\n'
            '\n'
            '-i <optional : input project path, default is current folder>\n'
        )
        sys.exit(2)

    project_path = os.getcwd()

    for opt, arg in opts:
        if opt == '-h':
            print(
                'usage: \n'
                '\n'
                '$ python oc_file_operation.py -i project_path\n'
                '\n'
                '-i <optional : input project path, default is current folder>\n'
            )
            sys.exit()
        elif opt == '-i':
            project_path = arg

    oc_class = OCClass(project_path)

    print('\n============== 开始扫描 ==============\n')

    oc_class.start_scan()

    print('\n============== 疑似类申明 ==============\n')

    list = oc_class.get_reference()
    content = sorted(list, key=lambda x: x[0])
    for index, value in enumerate(content):
        print(value[0])
        # print((index, value[0], value[1]))

    print('\n', len(content))
    print('\n============== End ==============\n')


if __name__ == '__main__':
    main(sys.argv[1:])
