#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

match_dict = {'sheep': '羊', 'horse': '马', 'chicken': '鸡', 'dog': '狗',
              'dragon': '龙', 'cow': '牛', 'tiger': '老虎', 'mouse': '老鼠',
              'rabbit': '兔子', 'snake': '蛇', 'pig': '猪', 'monkey': '猴子',
              'one': '一', 'two': '二',
              }


def match_operation(key):
    """根据word找解释"""
    if key in match_dict.keys():
        value = match_dict[key]
        return value
    else:
        print('!!!不在数据字典中的数据')
        return None
