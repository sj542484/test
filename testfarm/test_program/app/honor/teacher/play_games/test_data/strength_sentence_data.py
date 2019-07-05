#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

strength_sentence_dict = {'我可以说': 'i can say.','快点': 'hurry up',
                          '我有一个梦想。': 'I have a dream.', '我爱英语。': ' I love English.',
                          "我回来了。（自定义i'm）": "i'm home.", "有什么事吗?（自定义what's）": "what's up?",
                          "别担心。（自定义don't）": "don't worry."}


def strength_sentence_operation(key):
    """根据句子找word"""
    print('key:', key)
    if key in strength_sentence_dict.keys():
        value = strength_sentence_dict[key]
        print('value:', value)
        return value
    else:   # 不在数据字典中的数据
        print('!!!不在数据字典中的数据')
        return 'abc'
