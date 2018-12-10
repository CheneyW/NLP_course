#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
@project: NLP_lab3
@author: 王晨懿
@student ID: 1162100102
"""
import re
import os
# from nltk.corpus import stopwords

# 停用词文件
STOP_WORDS_LIST1 = os.path.join(os.getcwd(), 'data', 'StopWordList', 'swl1.txt')
STOP_WORDS_LIST2 = os.path.join(os.getcwd(), 'data', 'StopWordList', 'swl2.txt')
# STOP_WORDS = set(stopwords.words('english'))

# 通用词文件
COMMON_WORDS = os.path.join(os.getcwd(), 'data', 'CommonUsedWords', 'list.txt')
# 特征数量
FEATURE_NUM = 12


class Word(object):
    def __init__(self, ch):
        self.ch = ch
        self.features = [0] * FEATURE_NUM

    # 设置特征
    def set_feature(self, idx, f):
        self.features[idx] = f

    # 获取特征
    def get_features(self):
        s = self.ch + '\t'
        for f in self.features:
            s += str(f) + '\t'
        return s


# 提取构词特征的方法
class WordFeature(object):
    @staticmethod
    def contain_digital(word):  # 包含数字
        return 'CD' if re.search(r'[0-9]', word) else 'nCD'

    @staticmethod
    def contain_capital(word):  # 包含大写字母
        return 'CC' if re.search(r'[A-Z]', word) else 'nCC'

    @staticmethod
    def all_capital(word):  # 所有字母都是大写
        return 'AC' if word.isupper() else 'nAC'

    @staticmethod
    def contain_hyphen(word):  # 包含连字符
        return 'CH' if re.search(r'-', word) else 'nCH'

    @staticmethod
    def abbreviated_form(word):  # 字符缩写
        word = re.sub(r'[A-Z]+', 'A', word)
        word = re.sub(r'[a-z]+', 'a', word)
        word = re.sub(r'[0-9.]+', '0', word)
        word = re.sub(r'[^A-Za-z0-9.]+', 'x', word)
        return word


# 停用词
def stop_words_list():
    with open(STOP_WORDS_LIST1, 'r') as f:
        words1 = f.readlines()
    with open(STOP_WORDS_LIST2, 'r') as f:
        words2 = f.readlines()
    return set(w.strip('\n') for w in words1) | set(w.strip('\n') for w in words2)


# 通用词
def common_used_words():
    with open(COMMON_WORDS, 'r') as f:
        words = f.readlines()
    return set(w.strip('\n') for w in words)
