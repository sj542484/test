#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI

form_sentence_dict = {'我可以说': 'I can say.', '快点': 'hurry up',
                      '我有一个梦想。(自定义HAVE)': 'I HAVE a dream.', '我爱英语。（自定义English）': 'I love English.',
                      "我回来了。（自定义i'm）": "i'm home.", "有什么事吗?（自定义what's）": "what's up?",
                      "别担心。（自定义don't）": "don't worry.",

                      "我可以带些面包来": "I can bring some bread.", "鸡蛋怎么样？": "What about eggs?",
                      "星期五你打算做什么？": "What are you going to do on Friday?",
                      "我们需要什么？": "What do we need?",
                      "我要去看我的祖父母。": 'I am going to see my grandparents.',
                      }


def form_sentence_operation(key):
    """根据句子找word"""
    print('key:', key)
    if key in form_sentence_dict.keys():
        value = form_sentence_dict[key]
        print('value:', value)
        return value.lower()
    else:  # 不在数据字典中的数据
        print('不在数据字典中的数据 ! !')
        return None
