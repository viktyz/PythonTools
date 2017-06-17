#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Created by Alfred Jiang 2017-06-17

import re

oc_name_header = '[A-Za-z0-9]'
oc_name_normal = '[A-Za-z0-9_-]'

SPACE = ' '
DQM = '"'

ASSIGN = "="
LT = "<"
GT = ">"
BANG = "!"
TILDE = "~"
HOOK = "?"
COLON = ":"
EQ = "=="
LE = "<="
GE = ">="
NE = "!="
SC_OR = "||"
SC_AND = "&&"
INCR = "++"
DECR = "--"
PLUS = "+"
MINUS = "-"
STAR = "*"
SLASH = "/"
BIT_AND = "&"
BIT_OR = "|"
XOR = "^"
REM = "%"
LSHIFT = "<<"
PLUSASSIGN = "+="
MINUSASSIGN = "-="
STARASSIGN = "*="
SLASHASSIGN = "/="
ANDASSIGN = "&="
ORASSIGN = "|="
XORASSIGN = "^="
REMASSIGN = "%="
LSHIFTASSIGN = "<<="
RSIGNEDSHIFTASSIGN = ">>="
RUNSIGNEDSHIFTASSIGN = ">>>="
ELLIPSIS = "..."


def covert(s):
    if s == SPACE:
        return 'SPACE'
    elif s == DQM:
        return 'DQM'
    elif s == ASSIGN:
        return 'ASSIGN'
    elif s == LT:
        return 'LT'
    elif s == GT:
        return 'GT'
    elif s == BANG:
        return 'BANG'
    elif s == TILDE:
        return 'TILDE'
    elif s == HOOK:
        return 'HOOK'
    elif s == COLON:
        return 'COLON'
    elif s == EQ:
        return 'EQ'
    elif s == LE:
        return 'LE'
    elif s == GE:
        return 'GE'
    elif s == NE:
        return 'NE'
    elif s == SC_OR:
        return 'SC_OR'

    return s

def flag_w_state(content,h_string,t_string):




def flag_d_state(state, c_flag, t_flag, o_state, r_state):
    if covert(c_flag) in t_flag.keys() and state == o_state:
        state = int(t_flag[covert(c_flag)])
    else:
        state = r_state

    return state


def flag_s_state(state, c_flag, t_flag, o_state, t_state, r_state):
    if len(re.findall(t_flag, c_flag)) and state == o_state:
        state = t_state
    else:
        state = r_state

    return state


def oc_import_declare(content):
    '''
    扫描字符串获取 Objective-C import 列表
    :param content: 待扫描字符串
    :return: 包含全部 import 列表的数组
    '''

    state = 0
    imprt_s = ''

    for i in content:
        if state == 0:
            state = flag_s_state(state, i, '[#]', 0, 1, 0)
        elif state == 1:
            state = flag_s_state(state, i, '[i]', 1, 2, 0)
        elif state == 2:
            state = flag_s_state(state, i, '[m]', 2, 3, 0)
        elif state == 3:
            state = flag_s_state(state, i, '[p]', 3, 4, 0)
        elif state == 4:
            state = flag_s_state(state, i, '[o]', 4, 5, 0)
        elif state == 5:
            state = flag_s_state(state, i, '[r]', 5, 6, 0)
        elif state == 6:
            state = flag_s_state(state, i, '[t]', 6, 7, 0)
        elif state == 7:
            state = flag_d_state(state, i, {
                'SPACE': '8',
                'LT': '9',
                'DQM': '10',
            }, 7, 0)
        elif state == 8:
            state = flag_d_state(state, i, {
                'SPACE': '8',
                'LT': '9',
                'DQM': '10',
            }, 8, 0)
        elif state == 9:
            state = flag_s_state(state, i, oc_name_header, 9, 11, 0)
        elif state == 10:
            state = flag_s_state(state, i, oc_name_header, 10, 12, 0)
        elif state == 11:
            state = flag_s_state(state, i, oc_name_header, 10, 12, 0)

        state = flag_state(state, i, oc_normal_name, 9, 9, 0)
        state = flag_state(state, i, oc_normal_name, 10, 10, 0)
        state = flag_state(state, i, '[]', 8, 8, 0)
        state = flag_state(state, i, oc_normal_name, 9, 9, 0)
        state = flag_state(state, i, oc_normal_name, 10, 10, 0)
        if state != 0:
            imprt_s = imprt_s + i

    return []


def oc_interface_declare(content):
    '''
    扫描字符串获取 Objective-C 类申明
    :param content: 待扫描字符串
    :return: 包含全部类声明的数组
    '''

    # for i in content:

    return []


def oc_interface_extension(content):
    '''
    扫描字符串获取 Objective-C 类扩展
    :param content: 待扫描字符串
    :return: 包含全部类扩展的数组
    '''

    return []


def oc_implementation_define(content):
    '''
    扫描字符串获取 Objective-C 类定义
    :param content: 待扫描字符串
    :return: 包含全部类定义的数组
    '''

    return []


def oc_variable_declare(content):
    '''
    扫描字符串获取 Objective-C 变量申明
    :param content: 待扫描字符串
    :return: 包含全部变量声明的数组
    '''

    return []


def oc_property_declare(content):
    '''
    扫描字符串获取 Objective-C property 变量申明
    :param content: 待扫描字符串
    :return: 包含全部 property 变量声明的数组
    '''

    return []


def oc_method_declare(content):
    '''
    扫描字符串获取 Objective-C 方法申明
    :param content: 待扫描字符串
    :return: 包含全部方法声明的数组
    '''

    return []


def oc_method_define(content):
    '''
    扫描字符串获取 Objective-C 方法定义
    :param content: 待扫描字符串
    :return: 包含全部方法定义的数组
    '''

    return []
