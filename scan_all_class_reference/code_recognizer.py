#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Created by Alfred Jiang 2017-06-17

t_s_index = 0   # 识别到首个命中字符索引

state_0 = 0 # 状态 0 ：未识别任何命中
state_1 = 1 # 状态 1 ：命中但未完成状态
state_2 = 2 # 状态 2 : 命中完成



def scan_oc_code(content):

    for i in content:

