#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI

# data base of word dictation
# we can add a or multiple expalin_word in it, like this '{'explain': 'xxxxxxxxxxx', 'word': 'yyyyyyyy'},'
dictation_dict = (
                    {'explain': '谢谢', 'word': 'thanks'},
                    {'explain': '拜访', 'word': 'visit'},

                    {'explain': '雨', 'word': 'rain'},
                    {'explain': '雪', 'word': 'snow'},
                    {'explain': '河', 'word': 'river'},
                    {'explain': '树', 'word': 'tree'},

                    {'explain': '你好（首字母大写，自定义去除最后一个字母）', 'word': 'Hello'},
                    {'explain': '结束（自定义去除最后一个字母）', 'word': 'over'},
                    {'explain': '苹果（首字母大写，自定义去除最后一个字母）', 'word': 'Apple'},
                    {'explain': '喜欢（自定义去除最后一个字母）', 'word': 'like'},
                    {'explain': '但是（自定义去除最后一个字母）', 'word': 'but'},
                    {'explain': '一样的单词', 'word': 'aabbcd'},
                )


def dictation_operation(i):
    """根据句子找word"""
    value = dictation_dict[i]['word']
    return value
