#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/18 11:38
# -----------------------------------------
import unittest
from ddt import ddt, data, unpack

from testfarm.test_program.app.honor.student.homework_rebuild.object_pages.homework_data_handle import HomeworkDataHandle
from testfarm.test_program.app.honor.student.library.object_pages.game_page import LibraryGamePage
from testfarm.test_program.app.honor.student.library.object_pages.result_page import ResultPage
from testfarm.test_program.app.honor.student.library.object_pages.usercenter_page import UserCenterPage
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.homework_rebuild.test_data.homework_type_page import HomeworkTypePage as ht
from testfarm.test_program.conf.decorator import setup, teardown, testcase


@ddt
class FlashCard(unittest.TestCase):
    """闪卡练习"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.home = HomePage()
        cls.login_page = LoginPage()
        cls.library = LibraryGamePage()
        cls.result = ResultPage()
        cls.login_page.app_status()  # 判断APP当前状态

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @data(
        [ht.HW1, '闪卡练习'],
        [ht.HW1, '猜词游戏'],
        [ht.HW1, '还原单词'],
        [ht.HW1, '连连看'],
        [ht.HW2, '单项选择'],
        [ht.HW2, '单词听写'],
        [ht.HW2, '连词成句'],
        [ht.HW2, '单词拼写'],
        [ht.HW2, '选词填空'],
        [ht.HW3, '词汇选择'],
        [ht.HW3, '听音选图'],
        [ht.HW3, '句型转换'],
        [ht.HW3, '听后选择'],
        [ht.HW4, '强化炼句'],
        [ht.HW4, '听音连句'],
        [ht.HW4, '完形填空'],
        [ht.HW4, '阅读理解'],
        [ht.HW4, '补全文章'],
    )
    @unpack
    @testcase
    def test_all_game(self, hw_name, bank_type):
        if self.home.wait_check_home_page():
            user_info = UserCenterPage().get_user_info()                       # 获取个人信息
            stu_id = user_info[0]                                              # 学生id
            HomeworkDataHandle().delete_student_homework_data(stu_id)          # 删除作业记录
            if self.home.wait_check_home_page():
                self.home.click_hk_tab(2)  # 进入习题
                bank_info = self.library.enter_into_game(hw_name, bank_type)   # 获取大题元素与名称
                for i, ele in enumerate(bank_info[0]):                      # 遍历点击所有该题型的小题
                    if self.library.wait_check_bank_list_page():               # 题目列表页面检查点
                        bank_name = bank_info[1][i].text                            # 小题名称
                        print('大题名称：', bank_name)
                        bank_progress = self.library.bank_progress_by_name(bank_name)  # 大题进度
                        self.library.click_bank_by_name(bank_name)                                       # 点击进入游戏
                        if self.library.wait_check_game_page():                # 游戏页面检查点
                            # 首次做题(除闪卡外) 随机做题
                            first_result = self.library.play_book_games(fq=1, bank_name=bank_name,
                                                                        bank_progress=bank_progress)
                            if self.result.wait_check_result_page():  # 进入结果页，检验填写答案， 获取正确答案
                                self.result.again_btn().click()       # 错题再练
                                if self.library.wait_check_game_page():
                                    # 第二次做题， 全部做对
                                    self.library.play_book_games(fq=2, first_result=first_result, bank_name=bank_name)
                                self.library.click_back_up_button()

                if self.library.wait_check_bank_list_page():
                    self.library.click_back_up_button()
                    if self.library.wait_check_homework_list_page():
                        self.library.click_back_up_button()




