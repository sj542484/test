#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI

strength_sentence_dict = {'我可以说': 'i can say.','快点': 'hurry up',
                          '我有一个梦想。': 'I have a dream.', '我爱英语。': ' I love English.',
                          "我回来了。（自定义i'm）": "i'm home.", "有什么事吗?（自定义what's）": "what's up?",
                          "别担心。（自定义don't）": "don't worry.",

                          '我有一个梦想。(自定义HAVE)':'I HAVE a dream.','我爱英语。（自定义English）':'I love English.',

                          '看！丹尼在天安门广场。': 'Look! Danny was at Tian\'anmen Square.',
                          '发生了什么事？我想放风筝。': 'What happened? I wanted to fly a kite.',
                          '我弄伤了我的胳膊，詹妮帮助了我。': 'I hurt my arm and Jenny helped me.',
                          '这张照片是给你的，丹尼。': ' This photo is for you, Danny.',
                          "那是我的熊猫！": "That's my panda!", "嗨，熊猫！我想念你！": "Hi, panda! I miss you!",
                          }


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
