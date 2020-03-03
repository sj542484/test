#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI

match_dict = {'sheep': '羊', 'horse': '马', 'chicken': '鸡', 'dog': '狗',
              'dragon': '龙', 'cow': '牛', 'tiger': '老虎', 'mouse': '老鼠',
              'rabbit': '兔子', 'snake': '蛇', 'pig': '猪', 'monkey': '猴子',
              'one': '一', 'two': '二',

              'Hello': '你好（首字母大写，自定义去除最后一个字母）', 'over': '结束（自定义去除最后一个字母）',
              'Apple': '苹果（首字母大写，自定义去除最后一个字母）', 'like': '喜欢（自定义去除最后一个字母）',
              'but': '但是（自定义去除最后一个字母）',

              'bag': '书包', 'Alice': '（人名）爱丽丝', 'apple': '苹果'
              }


def match_operation(key):
    """根据word找解释"""
    if key in match_dict.keys():
        value = match_dict[key]
        return value
    else:
        print('!!!不在数据字典中的数据')
        return None
