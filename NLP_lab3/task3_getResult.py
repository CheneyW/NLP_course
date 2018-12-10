#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
@project: NLP_lab3
@author: 王晨懿
@student ID: 1162100102
"""
import re
import os

# crf++ 输出测试文件
OUTPUT = os.path.join(os.getcwd(), 'data', 'output.txt')
# 更改格式后的输出结果
RESULT = os.path.join(os.getcwd(), 'data', 'result.txt')

#  更改测试结果的格式，只保留词以及命名实体标记
if __name__ == '__main__':
    with open(OUTPUT, 'r')as f:
        lines = f.readlines()

    out = ''
    for l in lines:
        line = l.strip('\n')
        if not line:
            out += '\n'
            continue
        item = re.split('\t', line)
        if len(item) < 2:
            raise Exception(l)
        out += item[0] + '\t' + item[-1] + '\n'

    with open(RESULT, 'w') as f:
        f.write(out)
