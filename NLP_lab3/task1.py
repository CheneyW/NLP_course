#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
@project: NLP_lab3
@author: 王晨懿
@student ID: 1162100102
"""
import re
import os
import time
from MyClass import Word
from MyClass import WordFeature
from MyClass import stop_words_list
from MyClass import common_used_words

DATA_PATH = os.path.join(os.getcwd(), 'data')
GLOBAL_FEATURE = os.path.join(DATA_PATH, 'global_feature.txt')
TRAIN = os.path.join(DATA_PATH, 'Genia4ERtraining', 'Genia4ERtask1.iob2')
TRAIN_FEATURE = os.path.join(DATA_PATH, 'train.txt')


# 提取训练集特征
class ExtractTrainFeature(object):
    def __init__(self, file_path, out_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
        self.lines = lines
        self.freq_words = set()  # 关键词
        self.freq_frond, self.freq_back = set(), set()  # 前后边界词

        self.global_feature()
        self.print_model()
        out = self.extract_feature()
        with open(out_path, 'w') as f:
            f.write(out)

    # 生成全局特征
    def global_feature(self):
        words, frond_bound, back_bound = {}, {}, {}
        pre_word = '#'  # 表示非命名实体类别
        for l in self.lines:
            line = l.strip('\n')
            if not line or line.startswith('#'):
                continue
            w, label = re.split('\t', line)
            if label == 'O':
                if pre_word != '#':
                    back_bound[pre_word] = 1 if pre_word not in back_bound.keys() else back_bound[pre_word] + 1  # 后边界
                pre_word = '#'
                continue
            pre_word = w
            words[w] = 0 if w not in words.keys() else words[w] + 1  # 词频
            if label.startswith('B-'):
                frond_bound[w] = 1 if w not in frond_bound.keys() else frond_bound[w] + 1  # 前边界

        self.freq_words = set(key for key, value in words.items() if value > 20)
        self.freq_frond = set(key for key, value in frond_bound.items() if value > 5)
        self.freq_back = set(key for key, value in back_bound.items() if value > 5)

    # 将训练得到的全局特征保存在文件
    def print_model(self, path=GLOBAL_FEATURE):
        model_freq = '<FREQ>\n'  # 常用词
        for w in self.freq_words:
            model_freq += w + '\n'
        model_freq += '</FREQ>\n\n'

        model_front = '<FrontBound>\n'  # 前边界词
        for w in self.freq_frond:
            model_front += w + '\n'
        model_front += '</FrontBound>\n\n'

        model_back = '<BackBound>\n'  # 后边界词
        for w in self.freq_back:
            model_back += w + '\n'
        model_back += '</BackBound>\n\n'

        with open(path, 'w') as f:
            f.write(model_freq + model_front + model_back)

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


if __name__ == '__main__':
    t0 = time.time()
    # 提取训练集的特征,并生成全局特征模板
    ExtractTrainFeature(TRAIN, TRAIN_FEATURE)
    t1 = time.time()
    print(t1 - t0, 'seconds')
