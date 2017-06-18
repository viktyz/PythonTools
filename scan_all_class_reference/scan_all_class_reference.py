#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Created by Alfred Jiang 2017-06-18

import getopt
import os
import re
import sys

sys.path.append("..")
from la_oc_code.la_oc_code import DFA


def sub_strings_with_pattern(content, pattern, callback):
    '''
    获取满足某正则表达式全部结果
    :param content: 被查询的内容
    :param pattern: 查询规则
    :param callback: 指定回调函数
    :return: 满足条件的全部内容
    '''
    findallitems = re.findall(pattern, content)

    if (findallitems):

        for eachItem in findallitems:
            callback(eachItem.strip())

    return findallitems


def get_h_file_from_dir(dir, callback):
    '''

    获取全部 .h 文件
    :param dir: 指定路径
    :param callback: 指定回调函数
    :return: 返回包含全部 .h 路径的数组
    '''
    all_h_files = []

    for root, dirs, files in os.walk(dir):

        for item in files:

            filepath = os.path.join(root, item)

            extension = os.path.splitext(filepath)[1][1:]

            if extension == 'h':
                all_h_files.append(filepath)

                callback(filepath, root, item)

    return all_h_files


def operation_with_h_file(filepath, p_path, h_name):
    '''

    获取全部 class 名
    :param filepath: .h 文件路径
    :return: 返回包含全部 class 名的数组
    '''

    m_name = os.path.splitext(h_name)[0] + '.m'
    m_filepath = os.path.join(p_path, m_name)

    clist = []
    t_list = []

    if os.path.exists(m_filepath):
        m_dfa = DFA(m_filepath)
        m_dfa.start_convert()
        t_list = m_dfa.get_char()

    h_dfa = DFA(filepath)
    h_dfa.start_convert()
    t_list.extend(h_dfa.get_char())

    for item in t_list:
        print(item)

    return clist


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

    print('\n===========================\n')

    all_h_files = get_h_file_from_dir(project_path, operation_with_h_file)

    print('\n===========================\n')


if __name__ == '__main__':
    main(sys.argv[1:])
