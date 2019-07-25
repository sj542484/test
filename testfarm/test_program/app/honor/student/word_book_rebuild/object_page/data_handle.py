#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/27 14:38
# -----------------------------------------
import datetime

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.word_rebuild_sql import WordRebuildSql
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep


class DataActionPage(BasePage):
    def __init__(self):
        self.mysql = WordRebuildSql()
        self.home = HomePage()

    @teststep
    def get_sys_words_trans_id(self, stu_id):
        """获取系统翻译ID列表"""
        sys_trans_ids = self.mysql.find_sys_words_trans_id(stu_id)
        return [x[0] for x in sys_trans_ids]

    @teststep
    def get_teacher_words_trans_id(self, stu_id):
        """获取老师布置单词"""
        sys_trans_ids = self.mysql.find_teacher_words_trans_id(stu_id)
        return [x[0] for x in sys_trans_ids]

    @teststep
    def get_explain_level(self, explain_id_list, stu_id, fvalue=0):
        """根据解释的id获取对应的F值"""
        level_list = [self.mysql.find_explain_level_by_id(x, stu_id)[0][0] for x in explain_id_list]
        result = [x for x in level_list if x >= fvalue]
        return len(result)

    @teststep
    def clear_student_word_data(self, stu_id):
        """清除学生单词记录"""
        self.mysql.update_student_word_fluency_data(stu_id)
        self.mysql.update_student_word_data(stu_id)
        self.mysql.delete_student_word_wrong_data(stu_id)


    @teststep
    def update_word_date(self, time_interval, stu_id, fluency_level):
        """更改单词最后完成时间"""
        now = datetime.datetime.now()
        word_date = (now + datetime.timedelta(days=-time_interval)).strftime("%Y-%m-%d %H:%M:%S")
        self.mysql.update_has_studied_word_date(word_date, stu_id, fluency_level)
        self.mysql.update_word_record_date(word_date, stu_id)
