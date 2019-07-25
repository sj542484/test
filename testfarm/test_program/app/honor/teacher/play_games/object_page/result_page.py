#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import re
import time
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from conf.base_config import GetVariable as gv
from utils.get_attribute import GetAttribute
from utils.wait_element import WaitElement


class ResultPage(BasePage):
    """结果页"""
    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_result_page(self, var=20):
        """以“准确率 ”的ID为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "correct_rate")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def correct_rate(self):
        """准确率"""
        rate = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "correct_rate").text
        return rate

    @teststep
    def result_score(self):
        """积分"""
        score = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "score").text
        return score

    @teststep
    def result_star(self):
        """星星"""
        star = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "star").text
        return star

    @teststep
    def result_time(self):
        """时间"""
        ele = self.driver.find_element_by_id(gv.PACKAGE_ID + "time")
        value = re.sub("\D", "", ele.text)
        return value

    @teststep
    def rank(self):
        """title: 排行榜"""
        rank = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "rank").text
        return rank

    @teststep
    def rank_menu(self):
        """排行榜下拉按钮"""
        self.driver\
            .find_element_by_id("android:id/text1").click()
        time.sleep(1)

    @teststep
    def rank_menu_item(self):
        """排行榜下拉菜单"""
        item = self.driver.find_elements_by_id("android:id/text1")
        time.sleep(1)
        return item

    # 以下为排行榜list内容
    @teststep
    def rank_index(self):
        """排名"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "index")
        return item

    @teststep
    def rank_name(self):
        """学生昵称"""
        time.sleep(1)
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "name")
        return item

    @teststep
    def rank_accuracy_rate(self):
        """准确率最高的那次的正确率"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "rate")
        return item

    @teststep
    def rank_spend_time(self):
        """准确率最高的那次 完成所用时间"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "time")
        return item

    @teststep
    def check_result_button(self):
        """查看答案按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "detail") \
            .click()

    # 以下为查看答案页面元素
    @teststeps
    def wait_check_detail_page(self, var=10):
        """title:查看答案"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'查看答案')]")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def mine_result(self):
        """查看答案 页面每个小题后面 对错标识"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "iv_mine")
        value = GetAttribute().selected(item)
        return value

    @teststep
    def again_button(self):
        """错题再练/再练一遍按钮"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "again")
        print(ele.text)
        return ele,ele.text

    @teststep
    def back_up_button(self):
        """以“返回按钮”的class name为依据"""
        time.sleep(1)
        self.driver \
            .find_element_by_class_name("android.widget.ImageButton").click()

    @teststeps
    def back_up(self):
        """返回到作业list"""
        time.sleep(1)
        j = 0
        while j < 2:
            self.back_up_button()  # 结果页 返回按钮
            j += 1

    @teststeps
    def result_page_correct_rate(self, questions, rate):
        """结果页结果统计 -- 准确率"""
        print('结果页 -- 准确率：共%s题'% rate)
        if self.wait_check_result_page():  # 结果页检查点
            if len(questions) != 0:  # 答对的题数
                correct_rate = re.findall(r"\d+", self.correct_rate())[0]  # 本次结果统计——准确率

                accuracy_rate = 100
                num = len(questions) * 100 / int(rate)

                if num < 100:
                    var = 0
                    if num - int(num) >= 0.5:
                        var += 1

                    accuracy_rate = int(num) + var  # 根据答题情况 计算准确率

                print('统计结果:', accuracy_rate)
                if int(correct_rate) == accuracy_rate:
                    print("准确率逻辑无误 - 答对%s题 准确率:%s" % (len(questions), correct_rate + '%'))
                else:
                    print("★★★ Error 准确率逻辑有误 - 答对%s题 但准确率为:%s" % (len(questions), correct_rate + '%'))
                    # MyError(self.driver).my_error(int(correct_rate) != accuracy_rate)
            else:
                print("答对0题 准确率为:0%")
            print('==================================================')

    @teststeps
    def result_page_score(self, questions):
        """结果页结果统计 -- 积分"""
        print('结果页 -- 积分：')
        if self.wait_check_result_page():  # 结果页检查点
            score = re.sub("\D", "", self.result_score())  # 本次结果统计——积分

            if int(score) == 0:
                print("积分逻辑无误 - 答对%s题 积分:%s" % (questions, score))
            else:
                print("★★★ 积分逻辑有误 - 答对%s题 但积分为:%s" % (questions, score))
                # MyError(self.driver).my_error(int(score) != len(questions))

            print('==================================================')
        return questions

    @teststeps
    def result_page_star(self, questions):
        """结果页结果统计 -- 星星"""
        print('结果页 -- 星星：')
        if self.wait_check_result_page():  # 结果页检查点
            star_count = re.sub("\D", "", self.result_star())  # 本次结果统计——星星

            if int(star_count) == 0:
                print("星星逻辑无误 - 做了%s题 星星数:%s" % (questions, star_count))
            else:
                print("★★★ 星星逻辑有误 - 做了%s题 但星星数为:%s" % (questions, star_count))
                # MyError(self.driver).my_error(int(rate) != int(star_count))

            print('==================================================')
            return star_count

    @teststeps
    def result_page_time(self, now, button=''):
        """结果页结果统计 -- 所用时间"""
        print('结果页 -- 所用时间:')
        if self.wait_check_result_page():  # 结果页检查点
            result_time = self.get_time(self.result_time())  # 本次结果统计——所用时间
            print('result_time:', result_time, now)
            if button != '错题再练按钮':
                if now == result_time:
                    print("本次答题所用时间:", result_time)
                elif now < result_time:
                    print("本次答题所用时间:%s秒, 时间差为：%s秒" % (result_time, result_time - now))
                else:
                    print("★★★ 时间逻辑有误 - 做题页面时间为 %s 结果页统计时间为:%s" % (now, result_time))
                    # MyError(self.driver).my_error(now > result_time)
            else:  # 错题再练
                if now == result_time:
                    print("本次答题所用时间：", result_time)
                elif result_time - now <= 2:
                    print("本次答题所用时间：%s秒 时间差为:%s秒 " % (result_time, result_time - now))
                else:
                    print("★★★ 时间逻辑有误 - 做题页面时间为: %s 结果页统计时间为:%s" % (now, result_time))
                    # MyError(self.driver).my_error(now > result_time)
            print('==================================================')
            return result_time

    def get_time(self, time_str):
        """将带有格式的时间（xx:xx）转换为int类型"""
        now = []
        var = re.sub("\D", "", time_str)
        # 小时
        if int(var[0]) != 0:
            now.append(60 * int(var[0]) * 10 + 60 * int(var[1]))
        else:
            now.append(60 * int(var[1]))

        # 分钟
        if int(var[2]) != 0:
            now.append(int(var[2])*10 + int(var[3]))
        else:
            now.append(int(var[3]))

        for i in range(len(now)):
            if i + 1 < len(now):
                now[0] += now[i + 1]

        return int(now[0])
