#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@project: NLP_lab3
@author: 王晨懿
@student ID: 1162100102
"""
import re
import os
from MyClass import Word
from MyClass import WordFeature
from MyClass import stop_words_list
from MyClass import common_used_words

DATA_PATH = os.path.join(os.getcwd(), 'data')
# 全局特征训练文件
GLOBAL_FEATURE = os.path.join(DATA_PATH, 'global_feature.txt')
# 测试集
TEST1 = os.path.join(DATA_PATH, 'Genia4ERtest', 'Genia4EReval1.raw')
TEST2 = os.path.join(DATA_PATH, 'Genia4ERtest', 'Genia4EReval2.iob2')
# 测试集特征文件
TEST_FEATURE = os.path.join(DATA_PATH, 'test.txt')


# 提取测试集特征
class ExtractTestFeature(object):
    def __init__(self, file_path, out_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
        self.lines = lines
        self.freq_words = set()
        self.freq_frond, self.freq_back = set(), set()

        self.get_global_feature()
        out = self.extract_feature()
        with open(out_path, 'w') as f:
            f.write(out)

    # 提取特征
    def extract_feature(self):
        out = ''
        stop_words = stop_words_list()
        common_words = common_used_words()
        for l in self.lines:
            if l.startswith('#'):
                out += l
                continue
            line = l.strip('\n')
            if not line:
                out += '\n'
                continue
            word, label = re.split('\t', line)
            w = Word(word)
            # 构词特征
            w.set_feature(0, WordFeature.contain_digital(word))
            w.set_feature(1, WordFeature.contain_capital(word))
            w.set_feature(2, WordFeature.all_capital(word))
            w.set_feature(3, WordFeature.contain_hyphen(word))
            # 缩写形式
            w.set_feature(4, WordFeature.abbreviated_form(word))
            # 停用词
            w.set_feature(5, 'SW' if word in stop_words else 'nSW')
            # 通用词
            w.set_feature(6, 'CW' if word in common_words else 'nCW')
            # 全局特征
            w.set_feature(7, 'FW' if word in self.freq_words else 'nFW')  # 词频
            if len(word) >= 3:
                w.set_feature(8, word[:3])  # 前缀
                w.set_feature(9, word[-3:])  # 后缀
            else:
                w.set_feature(8, 'NP')
                w.set_feature(9, 'NS')
            w.set_feature(10, 'FB' if word in self.freq_frond else 'nFB')  # 前边界词
            w.set_feature(11, 'BB' if word in self.freq_back else 'nBB')  # 后边界词
            out += w.get_features() + label + '\n'
        return out

    # 读取全局特征文件
    def get_global_feature(self, path=GLOBAL_FEATURE):
        with open(path, 'r') as f:
            model = [x.strip('\n') for x in f.readlines()]
        self.freq_words = set(model[model.index('<FREQ>') + 1:model.index('</FREQ>')])
        self.freq_frond = set(model[model.index('<FrontBound>') + 1:model.index('</FrontBound>')])
        self.freq_back = set(model[model.index('<BackBound>') + 1:model.index('</BackBound>')])


if __name__ == '__main__':
    # 提取测试集的特征
    ExtractTestFeature(TEST2, TEST_FEATURE)
