# -*- coding: utf-8 -*-
# Copyright 2020 yinzhiwu@126.com.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import re

punc = [",", ".", "。", ",", "!", "!", "?", "？", ";", "；"]
dat = {"年", "月", "日", "周", "时", "分", "秒",
       "头", "只", "条", "顶", "个", "朵", "颗", "棵", "件", "道", "块", "匹", "支", "枝",
       "台", "副", "幅", "双", "瓶", "声", "位", "列", "手", "场", "片", "张", "把", "座", "面", "首", "叶",
       "艘", "次", "封", "轮", "潭", "群", "对", "架", "捆", "盘", "套", "篇"}

windows_length = 5


def is_punc(uchar):
    if uchar in punc:
        return True


def is_chinese_punc(uchar):
    if uchar in punc:
        return True

    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    else:
        return False


def is_number(uchar):
    if u'\u0030' <= uchar <= u'\u0039':
        return True
    else:
        return False


def is_alpha(uchar):
    if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
        return True
    else:
        return False


def is_legal(uchar):
    if not (is_chinese_punc(uchar) or is_number(uchar) or is_alpha(uchar)):
        return False
    else:
        return True


def is_windows_legal(windows):
    for w in windows:
        if w in dat:
            return True
    return False


def word_process():
    file_read = open("articles.txt", "r")
    file_write = open("../data/articles-out.txt", "w")
    while True:
        line = file_read.readline()
        # check end file
        if len(line) == 0:
            break
        article = ""
        punc_flag = 0
        first_word_flag = 1
        for i, oneWord in enumerate(line):
            windows = line[i:i + windows_length]
            if is_chinese_punc(oneWord) or is_number(oneWord):
                if is_number(oneWord) and (not is_windows_legal(windows)):
                    continue
                if is_punc(oneWord):
                    if first_word_flag == 1 or punc_flag == 1:
                        continue
                    punc_flag = 1
                else:
                    punc_flag = 0
                article += oneWord
                first_word_flag = 0
        match = re.search(r'方方|汪芳|武汉', article, re.M | re.I)
        if match and len(article) > 10:
            file_write.write(article)
            file_write.write('\n')
    file_read.close()
    file_write.close()


def remove_duplicate_lines():
    file_read = open("../data/articles-out.txt", "r")
    file_write = open("../data/articles-rst.txt", "w")
    lines = set()
    line = file_read.readline()
    while line:
        if line not in lines:
            file_write.write(line)
            lines.add(line)
        line = file_read.readline()
    file_read.close()
    file_write.close()


params = {".", "。", "?", "？", "!", "！"}
end_flag = set(params)


def article_line():
    file_read = open("../data/articles-rst.txt", "r")
    file_write = open("../data/articles-line.txt", "w")
    line = file_read.readline()
    while line:
        for word in line:
            sent_end = 0
            if word in end_flag:
                file_write.write(word)
                file_write.write("\n")
                sent_end = 1
            else:
                file_write.write(word)
        if sent_end == 0:
            file_write.write("\n")
        line = file_read.readline()
    file_read.close()
    file_write.close()


def article_BIO():
    file_read = open("../data/articles-line.txt", "r")
    file_write = open("../data/articles-bio.txt", "w")
    line = file_read.readline()
    while line:
        if len(line.strip()) < 10:
            line = file_read.readline()
            continue
        for word in line:
            if len(word.strip()) < 1:
                continue
            sent_end = 0
            if word in end_flag:
                file_write.write(word)
                file_write.write("\n\n")
                sent_end = 1
            else:
                if len(word.strip()) >= 1:
                    file_write.write(word)
                    file_write.write("\n")
        if sent_end == 0:
            file_write.write("\n")
        line = file_read.readline()
    file_read.close()
    file_write.close()


word_process()
remove_duplicate_lines()
article_line()
article_BIO()
