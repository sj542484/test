#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI

guess_word_dict = {'你好': 'hello', '小姐': 'Miss', '球棒，蝙蝠': 'bat', '公交车': 'bus',
                   '床': 'bed', '垃圾桶': 'bin', '盒子': 'box',
                   '六': 'six', '狐狸': 'fox', '斧头': 'ax',

                   '你好（首字母大写，自定义去除最后一个字母）': 'Hello', '结束（自定义去除最后一个字母）': 'over',
                   '苹果（首字母大写，自定义去除最后一个字母）': 'Apple', '喜欢（自定义去除最后一个字母）': 'like',
                   '但是（自定义去除最后一个字母）': 'but',

                   '享受，喜爱，欣赏': 'enjoy', '周末': 'weekend',
                   '属于（某人或者某物）；关于（某人或某物）': 'of', '下一个（的）；接下来（的）': 'next',
                   '照片；图画': 'picture', '女孩': 'girl', '狗': 'dog',
                   '后院': 'backyard', '整齐的，整洁的': 'tidy', '装饰，装潢': 'decorate'
                   }


def guess_word_operation(key):
    """根据word找解释"""
    print('key:', key)
    if key in guess_word_dict.keys():
        value = guess_word_dict[key]
        print('value:', value)
        return value.lower()
    else:  # 不在数据字典中的数据
        print('不在数据字典中的数据!!!')
        return None
