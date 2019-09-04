#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 15:16
# -----------------------------------------
import re
from testfarm.test_program.app.honor.student.games.game_public_element import PublicPage
from testfarm.test_program.conf.decorator import teststep


class HomeWorkPublicElePage(PublicPage):


    @teststep
    def bank_count(self):
        """题目个数"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_title")
        return int(ele.get_attribute('contentDescription'))

    @teststep
    def rest_bank_num(self):
        """待完成题数"""
        ele = self.driver.find_element_by_id('{}rate'.format(self.id_type()))
        return int(ele.text)

    @teststep
    def bank_time(self):
        """题目时间"""
        ele = self.driver.find_element_by_id('{}time'.format(self.id_type()))
        time_str = re.findall(r'\d', ele.text)
        return int(time_str[0]) * 3600 + int(time_str[1]) * 60 + int(time_str[2]) * 10 + int(time_str[3])

    @teststep
    def rate_judge(self, total, i):
        """待完成数校验"""
        print(total, i)
        current_rate = self.rest_bank_num()
        if int(current_rate) != total - i:
            print('★★★ 待完成数不正确', current_rate, '应为：', total - i)

    @teststep
    def judge_timer(self, timer):
        if len(timer) > 1:
            if any(timer[i + 1] > timer[i] for i in range(0, len(timer) - 1)):
                print('计时功能无误:', timer, '\n')
                return True
            else:
                print('★★★ Error - 计时错误:', timer, '\n')
        else:  # 只有一道题
            print('只有一道题，时间为:', timer[0], '\n')
            return True
