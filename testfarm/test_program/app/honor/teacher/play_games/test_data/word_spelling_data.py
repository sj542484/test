#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

word_spelling_dict = {'到': 'get','大': 'big','图书馆': 'library','音乐': 'music','午餐': 'lunch',
                      '阴天的；多云的': 'cloudy','外衣；大一': 'sweater','衣服；服装': 'clothes','马': 'horse',
                      '雨伞': 'umbrella','奋斗，斗争，辩论': 'content','不安定，不稳定，基础薄弱': 'instability',

                      # '你好（首字母大写，自定义去除最后一个字母）': 'Hello', '结束（自定义去除最后一个字母）': 'over',
                      # '苹果（首字母大写，自定义去除最后一个字母）': 'Apple', '喜欢（自定义去除最后一个字母）': 'like',
                      # '但是（自定义去除最后一个字母）': 'but', '一样的单词': 'aa',
                      #
                      # '喷泉': 'fountain', '见面': 'meet', '杂志': 'magazine', '台阶': 'stair', '在......旁边': 'beside ',
                      # '观光': 'sightseeing', '围巾': 'scarf', '加拿大': 'Canada', '鲸鱼': 'whale', '旅行': 'cruise',
                      #
                      # '嗨': 'hi', '你好': 'hello ', '猪': 'pig ', '是': 'am', '猫': 'cat', '你(们)': 'you', '是的': 'yes',
                      # '先生': 'Mr', '不': 'no', '小姐': 'Miss ', '狐狸': 'fox ', '狗': 'dog', '鸭子': 'duck',
                      # '小鸟': 'bird', '小鸡': 'chick'
}


def word_spelling_operation(key):
    """根据word找解释"""
    print('key:', key)
    if key in word_spelling_dict.keys():
        value = word_spelling_dict[key]
        print('value:', value)
        return value
    else:   # 不在数据字典中的数据
        print('不在数据字典中的数据!!')
        return 'abc'
