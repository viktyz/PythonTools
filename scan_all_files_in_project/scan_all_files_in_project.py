#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Created by Alfred Jiang 2017-03-01
import getopt
import os
import sys

# ignore_dirs = ['.git', 'build', '.framework', '.bundle', '.xcodeproj','.xcassets']
ignore_dirs = ['.git', 'build', '.bundle', '.xcodeproj','.xcassets']


def need_ignore(file_path):
    for item in ignore_dirs:

        if item in file_path:
            return True

    return False


def get_file_from_dir(dir, callback):
    '''

    :param dir: 指定路径
    :param callback: 指定回调函数
    :return: 返回包含全部文件路径的数组
    '''
    for root, dirs, files in os.walk(dir):

        if need_ignore(root):
            continue

        for item in files:
            callback(root, item)


adict = dict()


def group_file_by_extension(root, item):
    '''

    :param root: 文件所在目录
    :param item: 文件名
    :return: 返回包含全部文件路径的数组
    '''
    filepath = os.path.join(root, item)

    itemInfo = dict()
    itemInfo['path'] = filepath
    itemInfo['file'] = item

    extension = os.path.splitext(filepath)[1][1:]

    if len(extension) != 0:

        if extension in adict:

            group = adict[extension]

            eExist = False

            for info in group:

                if item == info['file']:
                    print(
                        'PLEASE CHECK THIS FILE : \n' + item + '\nDUPLICATE FILE IN THIS PATH : \n' + filepath + '\n' +
                        info['path'] + '\n')

                    eExist = True

                    break

            if not eExist:
                group.append(itemInfo)

        else:
            list = []
            list.append(itemInfo)
            adict[extension] = list
    else:
        if 'none_extension' in adict:
            adict['none_extension'].append(itemInfo)
        else:
            list = []
            list.append(itemInfo)
            adict['none_extension'] = list


# 主函数
def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'h:i:',
                                   ['inputproject='])
    except getopt.GetoptError:
        print(
            'usage: \n'
            '\n'
            '$ python scan_all_files_in_project.py -i project_path\n'
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
                '$ python scan_all_files_in_project.py -i project_path\n'
                '\n'
                '-i <optional : input project path, default is current folder>\n'
            )
            sys.exit()
        elif opt == '-i':
            project_path = arg

    get_file_from_dir(project_path, group_file_by_extension)

    print('\n===========================\n')

    icount = 0

    sorted_key = sorted(adict.keys())

    for item in sorted_key:
        icount += len(adict[item])
        print(item + ' : ' + str(len(adict[item])))

    print('\nTOTAL : ' + str(icount))


if __name__ == '__main__':
    main(sys.argv[1:])
