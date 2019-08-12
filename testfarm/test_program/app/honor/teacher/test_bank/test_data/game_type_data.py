#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

game_dict = {"听后选择": "1",
             '单项选择': '2',
             '强化炼句': '3',
             "听音连句": "4",
             "句型转换": "5",
             "阅读理解": "6",
             "完形填空": "7",
             "补全文章": "8",
             "选词填空": "9",

             "单词听写": "10",
             "单词拼写": "11",
             "猜词游戏": "12",
             "词汇选择": "13",
             "闪卡练习": "14",
             "听音选图": "15",
             "连连看": "16",
             "连词成句": "17",
             "还原单词": "18",

             "句子学习": "19",
             "单词抄写": "20",
             "单词学习": "21",

             "微课": "22",
             "磨耳朵": "23"
             }

def game_type_operation(key):
    """根据"""
    if key in game_dict.keys():
        value = game_dict[key]
        return int(value)
    else:
        print('!!!数据中不包含该游戏类型:', key)
        return None