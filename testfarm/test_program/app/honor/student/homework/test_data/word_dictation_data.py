import random


# data base of word dictation
# we can add a or multiple expalin_word in it, like this '{'explain': 'xxxxxxxxxxx', 'word': 'yyyyyyyy'},'
dictation_dict = (
    {'explain': '你好（首字母大写，自定义去除最后一个字母）', 'word': 'Hello'},
    {'explain': '结束（自定义去除最后一个字母）', 'word': 'over'},
    {'explain': '苹果（首字母大写，自定义去除最后一个字母）', 'word': 'Apple'},
    {'explain': '喜欢（自定义去除最后一个字母）', 'word': 'like'},
    {'explain': '但是（自定义去除最后一个字母）', 'word': 'but'},
    {'explain': '一样的单词', 'word': 'aabbcd'},

)


def dictation_operate(i):
    """根据句子找word"""
    value = dictation_dict[i]['word']
    return value
