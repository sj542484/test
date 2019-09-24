#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

sentence_transform_dict = {'This is a desk.(变一般疑问句)': 'Is this a desk?',
                            'That is a chair.（变成否定句）': "That isn't a chair.",
                            'Is this a book?（给出肯定回答）': 'Yes,it is .',
                            'Is it a duck？（给出否定回答）': "No，it isn't.",

                            'I have a dream.（将原句改为否定句）': 'I have not a dream.',
                           'I have not a dream.（将原句改为肯定句）': 'I have a dream.'}


def sentence_transform_operation(key):
    """根据word找解释"""
    print('key:', key)
    if key in sentence_transform_dict.keys():
        value = sentence_transform_dict[key]
        print('value:', value)
        return value
    else:   # 不在数据字典中的数据
        print('不在数据字典中的数据 ! !')
        return None
