#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Created by Alfred Jiang 2017-07-17
import getopt
import os
import re
import sys


def sub_strings_with_pattern(content, pattern, callback):
    '''
    获取满足某正则表达式全部结果
    :param content: 被查询的内容
    :param pattern: 查询规则
    :param callback: 指定回调函数
    :return: 满足条件的全部内容
    '''
    foundallitems = re.findall(pattern, content)

    if (foundallitems):

        for eachItem in foundallitems:
            callback(eachItem.strip())

    return foundallitems


def get_h_file_from_dir(dir):
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

                operation_with_h_file(filepath)

    return all_h_files


def operation_with_class_name(classname):
    '''

    获取 class 名
    :param classname: 类名字符串
    :return: 返回类名称
    '''
    print('CLASS NAME = ' + classname)


def operation_with_c_function(cfunction):
    print('C Function : ' + cfunction)


alist = []
elist = []
mlist = []


def operation_with_h_file(filepath):
    '''

    获取全部 class 名
    :param filepath: .h 文件路径
    :return: 返回包含全部 class 名的数组
    '''

    file = open(filepath)

    content = re.sub("(/\*(\s|.)*?\*/)|(//.*)", "", file.read())

    patternStr = r'(\w+)\s+[\*,&]*\s*(\w+)\s*\('

    allcfunctions = sub_strings_with_pattern(content, patternStr, operation_with_c_function)

    file.close()

    return

    patternStr = r'%s(.+?)%s' % ('@interface ', ':')

    allclass = sub_strings_with_pattern(file.read(), patternStr, operation_with_class_name)

    if len(allclass) > 1:

        mlist.append(filepath)
    elif len(allclass) == 0:

        elist.append(filepath)
    for item in allclass:
        alist.append(item)

    file.close()

    return alist


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'h:i:',
                                   ['inputproject='])
    except getopt.GetoptError:
        print(
            'usage: \n'
            '\n'
            '$ python scan_all_publish_methods.py -i project_path\n'
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
                '$ python scan_all_publish_methods.py -i project_path\n'
                '\n'
                '-i <optional : input project path, default is current folder>\n'
            )
            sys.exit()
        elif opt == '-i':
            project_path = arg

    print('\n===========================\n')

    all_h_files = get_h_file_from_dir(project_path)

    print('\n===========================\n')

    print('ALL .H FILES COUNT : ' + str(len(all_h_files)))

    print('ALL CLASSES COUNT : ' + str(len(alist)))

    print('\n===========================\n')

    print('NO CLASS IN BELOW PATH : \n')
    for item in elist:
        print(item)

    print('\n===========================\n')

    print('MORE THAN ONE CLASS IN BELOW PATH : \n')
    for item in mlist:
        print(item)

    print('\n')


if __name__ == '__main__':
    main(sys.argv[1:])
