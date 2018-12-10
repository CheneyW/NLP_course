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

# 分析标注结果
if __name__ == '__main__':
    num, n1, n2, n3 = 0, 0, 0, 0
    with open(OUTPUT, 'r') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    for line in lines:
        if not line:
            continue
        standard, predict = re.split('\t', line)[-2:]
        num += 1
        if standard == predict:
            continue
        if standard == 'O':
            n1 += 1
        elif predict == 'O':
            n2 += 1
        else:
            n3 += 1
    print('错误数/总数 = %d/%d' % (n1 + n2 + n3, num))
    print('非命名实体标注为命名实体数：', n1)
    print('命名实体标注为非命名实体数：', n2)
    print('一类命名实体标注为另一类命名实体数：', n3)
