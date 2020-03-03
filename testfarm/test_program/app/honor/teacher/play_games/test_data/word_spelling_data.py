#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI

word_spelling_dict = {'到': 'get', '大': 'big', '图书馆': 'library', '音乐': 'music', '午餐': 'lunch',
                      '阴天的；多云的': 'cloudy', '外衣；大一': 'sweater', '衣服；服装': 'clothes',
                      '马': 'horse', '雨伞': 'umbrella', '奋斗，斗争，辩论': 'content',
                      '不安定，不稳定，基础薄弱': 'instability', '最重的': 'heaviest',
                      '丑陋的': 'ugliest', '最慢的': 'slowest', '最快的': 'fastest', '友善的': 'friendliest',

                      '模型': 'model', '艺术家': 'artist', '技术': 'technology',

                      '书包': 'bag', ' （人名）爱丽丝': 'Alice', '苹果': 'apple',
                      '你好（首字母大写，自定义去除最后一个字母）': 'Hello', '结束（自定义去除最后一个字母）': 'over',
                      '苹果（首字母大写，自定义去除最后一个字母）': 'Apple', '喜欢（自定义去除最后一个字母）': 'like',
                      '但是（自定义去除最后一个字母）': 'but', '一样的单词': 'aa',
                      }


def word_spelling_operation(key):
    """根据word找解释"""
    print('key:', key)
    if key in word_spelling_dict.keys():
        value = word_spelling_dict[key]
        print('value:', value)
        return value
    else:  # 不在数据字典中的数据
        print('不在数据字典中的数据!!')
        return 'abc'
