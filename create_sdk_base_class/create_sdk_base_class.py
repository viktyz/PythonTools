#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Created by Alfred Jiang 2017-02-22

import codecs
import getopt
import json
import os
import re
import sys


# 输出类继承关系表

# 常规继承关系节点
# {
#     'class_name': '',
#     'super_class_name':'',
#     'file_path':''
# }

# 继承自 NSObject 父类表示最终节点
# 'super_class_name':'NSObject',


def load_json_file(file_path):
    '''

    :param file_path: 加载的 JSON 数据文件路径
    :return: 返回 JSON 字典
    '''
    if not os.path.isfile(file_path):
        return ''

    with open(file_path, 'r') as json_file:
        json_data = json.load(json_file)

        return json_data


def save_json_data(json_data, file_path):
    '''

    :param json_data: 需要保存的 JSON 数据
    :param file_path: 需要保存的 JSON 文件路径
    :return: None
    '''
    if json_data == None:
        return

    with open(file_path, 'w') as json_file:
        json.dump(json_data, json_file)


def format_json_file(file_path, to_path):
    '''

    :param file_path: 需要格式化的 JSON 文件路径
    :return: None
    '''

    if len(to_path) == 0:
        to_path = file_path

    json_data = load_json_file(file_path)

    f_json_data = json.dumps(json_data, indent=4)

    with open(to_path, 'w') as json_file:
        json_file.write(f_json_data)


class scanner:
    def start(self, dir_path, output_file_path):
        '''

        :param dir_path: 待扫描根目录
        :param output_file_path: 扫描结果输出路径
        :return: None
        '''
        self.all_class_list = []

        self.output_file_path = output_file_path

        self.filter_all_h_files(dir_path)

    def filter_all_h_files(self, dir):
        '''

        :param dir: 待扫描根目录
        :return: None
        '''
        for root, dirs, files in os.walk(dir):

            for item in files:

                file_path = os.path.join(root, item)

                extension = os.path.splitext(file_path)[1][1:]

                if extension == 'h':
                    self.operate_with_h_file(file_path)

        save_json_data(self.all_class_list, self.output_file_path)

    def operate_with_h_file(self, file_path):
        '''

        :param file_path: 待处理 h 文件路径
        :return: None
        '''
        print(file_path)

        patternStr = r'%s(.+?)%s' % ('@interface ', '\n')

        with codecs.open(file_path, 'r', encoding='utf-8', errors='ignore') as file:

            allclass = self.sub_strings_with_pattern(file.read(), patternStr)

            file.close()

            for item in allclass:

                if ' : ' in item:
                    string = item.rstrip('{').rstrip('{}')

                    string = self.operate_with_protocol(string)

                    class_name, super_class_name = self.operate_with_class_line(string)

                    self.add_class_info(class_name, super_class_name, file_path)

    def add_class_info(self, class_name, super_class_name, file_path):
        '''

        :param class_name: 类名
        :param super_class_name: 父类名
        :param file_path: 类所在文件路径
        :return: None
        '''
        index = len(self.all_class_list)

        dic_info = dict()
        dic_info['index'] = index
        dic_info['class_name'] = class_name
        dic_info['super_class_name'] = super_class_name
        dic_info['file_path'] = file_path

        self.all_class_list.append(dic_info)

    def operate_with_protocol(self, string):
        '''

        :param string: 待处理字符串
        :return: 返回已处理结果
        '''
        patternStr = r'\<(.+?)\>'

        result = self.remove_strings_with_pattern(string, patternStr)

        if '//' in result:
            index = result.index('//')

            result = result[:index]

        return result.strip()

    def operate_with_class_line(self, string):
        '''

        :param string: 待处理字符串
        :return: 类名与父类名
        '''
        string = re.sub(r'\s+', ' ', string)

        item_list = string.split(' ')

        return item_list[0], item_list[2]

    def sub_strings_with_pattern(self, content, pattern):

        foundallitems = re.findall(pattern, content)

        return foundallitems

    def remove_strings_with_pattern(self, content, pattern):

        result, number = re.subn(pattern, '', content)

        return result


class merge:
    def start(self, framework_class_path, project_class_path, output_file_path):
        '''

        :param framework_class_path: 系统 SDK 类信息列表
        :param project_class_path: 工程中类信息列表
        :param output_file_path:
        :return: None
        '''
        self.all_class_list = []

        self.output_file_path = output_file_path

        framework_class_list = load_json_file(framework_class_path)

        project_class_path = load_json_file(project_class_path)

        for project_class_item in project_class_path:

            for framework_class_item in framework_class_list:

                if project_class_item['super_class_name'] == framework_class_item['class_name']:
                    self.add_class_info(project_class_item['class_name'], project_class_item['super_class_name'],
                                        project_class_item['file_path'], framework_class_item['file_path'])

        save_json_data(self.all_class_list, self.output_file_path)

    def add_class_info(self, class_name, super_class_name, file_path, framework_path):
        '''

        :param class_name: 类名
        :param super_class_name: 父类名
        :param file_path: 类所在文件路径
        :param framework_path: 类所在系统 SDK 文件路径
        :return: None
        '''
        index = len(self.all_class_list)

        dic_info = dict()
        dic_info['index'] = index
        dic_info['class_name'] = class_name
        dic_info['super_class_name'] = super_class_name
        dic_info['file_path'] = file_path
        dic_info['framework_path'] = framework_path

        self.all_class_list.append(dic_info)


class objective_c_class_creater:
    def create_sdk(self, prefix_name='', need_merge_class_path='', sdk_name='', directory_path=''):
        '''

        :param prefix_name: 自定义 SDK 前缀（推荐 3 个大写字符）
        :param need_merge_class_path: 待处理类信息列表文件路径
        :param sdk_name: 自定义 SDK 名称
        :param directory_path:  自定义 SDK 保存根目录
        :return: None
        '''
        if len(need_merge_class_path) == 0:
            return

        self.sdk_name = sdk_name
        self.directory_path = directory_path
        self.prefix_name = prefix_name

        class_list = load_json_file(need_merge_class_path)

        for class_info_item in class_list:
            self.create_class(class_info_item['super_class_name'], class_info_item['framework_path'])

    def create_class(self, super_class_name, framework_path):
        '''

        :param super_class_name: 带处理父类
        :param framework_path: 类所在系统 SDK 文件路径
        :return: None
        '''

        if len(self.directory_path) == 0:

            if len(self.sdk_name) == 0:
                s_directory_path = os.getcwd() + '/' + self.prefix_name + 'SDK'
            else:
                s_directory_path = os.getcwd() + '/' + self.sdk_name

        if not os.path.exists(s_directory_path):
            os.mkdir(s_directory_path)

        f_name = self.framework_info_with_path(framework_path)

        f_prefix = f_name[:2]

        if f_prefix.isupper():
            f_directory_path = s_directory_path + '/' + self.prefix_name + f_name[2:]
        else:
            f_directory_path = s_directory_path + '/' + self.prefix_name + f_name

        if not os.path.exists(f_directory_path):
            os.mkdir(f_directory_path)

        calss_name = self.prefix_name + super_class_name[2:]

        h_name = f_directory_path + '/' + calss_name + '.h'
        m_name = f_directory_path + '/' + calss_name + '.m'

        if os.path.exists(h_name) or os.path.exists(m_name):
            return

        h_class_info = \
            '//\n// USEASSampleClass.h\n// ...\n//\n// Created by ...\n// Copyright ...\n//\n\n#import <USEASSample/USEASSample.h>\n\n@interface USEASSampleClass : USEASSampleSuperClass\n\n@end'

        m_class_info = \
            '//\n// USEASSampleClass.m\n// ...\n//\n// Created by ...\n// Copyright ...\n//\n\n#import "USEASSampleClass.h"\n\n@implementation USEASSampleClass\n\n@end'

        h_class_info = re.sub('USEASSample/USEASSample.h', f_name + '/' + f_name + '.h', h_class_info)
        h_class_info = re.sub('USEASSampleClass', calss_name, h_class_info)
        h_class_info = re.sub('USEASSampleSuperClass', super_class_name, h_class_info)

        m_class_info = re.sub('USEASSampleClass', calss_name, m_class_info)

        with open(h_name, 'wt') as f:

            f.write(h_class_info)

        with open(m_name, 'wt') as f:

            f.write(m_class_info)

    def framework_info_with_path(self, framework_path):
        '''

        :param framework_path: 类所在系统 SDK 文件路径
        :return: 系统 SDK framework 名称
        '''
        item_list = framework_path.split('/')

        f_name = ''

        for item in item_list:

            if '.framework' in item:
                f_name = item.split('.')[0]

                break

        return f_name


# 主函数
def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'h:p:s:i:f:',
                                   ['prefixname=', 'sdkname=', 'inputproject=', 'folderpath='])
    except getopt.GetoptError:
        print(
            'usage: \n'
            '\n'
            '$ python create_sdk_base_class.py -p AFL\n'
            '\n'
            '-p <required : prefix name>\n'
            '-s <optional : sdk name, default is "prefix name + SDK" >\n'
            '-i <optional : input project path, default is current folder>\n'
            '-f <optional : sdk folder path, default is current folder>\n'
        )
        sys.exit(2)

    project_path = os.getcwd()
    prefix_name = ''
    folder_name = ''
    folder_path = ''

    for opt, arg in opts:
        if opt == '-h':
            print(
                'usage: \n'
                '\n'
                '$ python create_sdk_base_class.py -p AFL\n'
                '\n'
                '-p <required : prefix name>\n'
                '-s <optional : sdk name, default is "prefix name + SDK" >\n'
                '-i <optional : input project path, default is current folder>\n'
                '-f <optional : sdk folder path, default is current folder>\n'
            )
            sys.exit()
        elif opt == '-p':
            prefix_name = arg
        elif opt == '-s':
            folder_name = arg
        elif opt == '-i':
            project_path = arg
        elif opt == '-f':
            folder_path = arg

    if len(prefix_name) == 0:
        print(
            'usage: \n'
            '\n'
            '$ python create_sdk_base_class.py -p AFL\n'
            '\n'
            '-p <required : prefix name>\n'
            '-s <optional : sdk name, default is "prefix name + SDK" >\n'
            '-i <optional : input project path, default is current folder>\n'
            '-f <optional : sdk folder path, default is current folder>\n'
        )
        return

    if len(folder_name) == 0:
        folder_name = prefix_name + 'SDK'

    # 第一步：扫描 class 信息
    class_scanner = scanner()

    # 扫描获取 iOS SDK framework 全部 class 信息
    framework_path = '/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk/System/Library/Frameworks/'

    framework_class_path = os.getcwd() + '/' + folder_name + '/framework_class_list.json'

    if not os.path.exists(os.getcwd() + '/' + folder_name):
        os.mkdir(os.getcwd() + '/' + folder_name)

    class_scanner.start(framework_path, framework_class_path)

    # 扫描获取 iOS 工程 全部 class 信息

    project_class_path = os.getcwd() + '/' + folder_name + '/project_class_list.json'

    if not os.path.exists(os.getcwd() + '/' + folder_name):
        os.mkdir(os.getcwd() + '/' + folder_name)

    class_scanner.start(project_path, project_class_path)

    # 第二步：合并 class 信息，输出待处理列表
    class_merge = merge()

    merge_class_path = os.getcwd() + '/' + folder_name + '/merge_class_list.json'

    if not os.path.exists(os.getcwd() + '/' + folder_name):
        os.mkdir(os.getcwd() + '/' + folder_name)

    class_merge.start(framework_class_path, project_class_path, merge_class_path)

    # 第三步：创建 SDK 基类库
    oc_creater = objective_c_class_creater()
    oc_creater.create_sdk(prefix_name, merge_class_path, folder_name, folder_path)

    # 第四步：格式化输出部分信息
    format_json_file(project_class_path, '')
    format_json_file(merge_class_path, '')
    format_json_file(framework_class_path, '')


if __name__ == '__main__':
    main(sys.argv[1:])
