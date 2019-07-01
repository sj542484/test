import datetime

from app.student.login.object_page.home_page import HomePage
from app.student.user_center.object_page.buy_card_page import PurchasePage
from app.student.user_center.object_page.user_Info_page import UserInfoPage
from app.student.user_center.object_page.user_center_page import UserCenterPage
from app.student.word_book.object_page.sql_data.mysql_data import MysqlData
from conf.base_page import BasePage
from conf.decorator import teststep
from conf.base_config import GetVariable as gv


class DataActionPage(BasePage):
    """数据操作类"""
    def __init__(self):
        self.mysql = MysqlData()
        self.home = HomePage()
        self.user_center = UserCenterPage()
        self.user_info = UserInfoPage()

    @teststep
    def get_student_id(self):
        """获取学生id"""
        """获取用户手机号"""
        self.home.click_tab_profile()
        if self.user_center.wait_check_page():
            self.user_center.click_buy()
            if PurchasePage().wait_check_buy_page():
                phone = self.user_info.phone()
                name = self.user_info.nickname()
                stu_id = self.mysql.find_student_id(phone)
                # print(stu_id)
                gv.STU_ID = stu_id[0][0]
                print("学生id:", gv.STU_ID)
                return name

    @teststep
    def get_id_nick_back_home(self):
        """返回主页面"""
        nick_name = self.get_student_id()
        self.home.click_back_up_button()
        if self.user_center.wait_check_page():
            self.home.click_tab_hw()
        return nick_name

    @teststep
    def get_word_by_explain(self, explain):
        """根据翻译从数据库中获取单词
           若获取的单词可能为多个,则与数据库中的单词作比较
        """
        if ';' in explain:  # 解释拆分 对于有多个解释的单词，采用;前第一个解释
            explain = explain.split(';')[0]
        if '.' in explain:
            exp_list = explain.split('.')
            prop = exp_list[0] + '.'
            exp = exp_list[1].strip()
            english = self.mysql.find_word_by_explain(prop, exp)
        else:
            english = self.mysql.find_word_by_explain_no_prop(explain)
        word = [english[0][0]] if len(english) == 1 else [x[0] for x in english]
        return word

    @teststep
    def get_change_date(self, num):
        """为数据库提供修改日期"""
        now = datetime.datetime.now()
        word_date = (now + datetime.timedelta(days=-num)).strftime("%Y-%m-%d %H:%M:%S")
        record_date = (now + datetime.timedelta(days=-2)).strftime("%Y-%m-%d %H:%M:%S")
        print('单词时间：', word_date)
        print('去重时间：', record_date)
        return word_date, record_date

    @teststep
    def change_word_date(self):
        self.get_student_id()
        print("LEVEL：", gv.LEVEL)
        date = self.get_change_date(gv.TIME_COUNT)  # 获取修改的时间
        self.mysql.update_word_date(str(date[0]), gv.STU_ID, gv.LEVEL)
        self.mysql.update_word_record(str(date[1]), gv.STU_ID)  # 单词去重，更改record的create时间

    @teststep
    def get_all_word_homework_ids(self):
        """获取标签id"""
        word_homework_list = self.mysql.find_book_label(gv.STU_ID)
        word_homework = [x[0] for x in word_homework_list]
        return word_homework

    @teststep
    def get_word_homework_name(self, word_homework_id):
        """获取标签名称"""
        name = self.mysql.find_word_homework_name(word_homework_id)
        return name[0][0]

    @teststep
    def get_word_homework_id_by_name(self, word_homework_name):
        homework_id = self.mysql.find_homework_id_by_name(word_homework_name)
        return homework_id[0][0]

    @teststep
    def get_student_label_id_by_homework_id(self, homework_id):
        label_id = self.mysql.find_label_id_by_homework_id(gv.STU_ID, homework_id)
        return label_id[0][0]

    @teststep
    def get_wordbank_by_label_id(self, label_id):
        words = self.mysql.find_wordbank_by_label_id(label_id)
        word_list = words[0][0].split(',')
        return word_list

    @teststep
    def get_words_count(self, word_homework_id):
        """获取单词总数 与一轮 三轮单词数"""
        result = self.mysql.find_word_by_label(gv.STU_ID, word_homework_id)
        first_count = []
        third_count = []
        for i in range(len(result)):
            if result[i][1] >= 1:
                first_count.append(i)
            if result[i][1] >= 3:
                third_count.append(i)
        return len(first_count), len(third_count)

    @teststep
    def get_word_by_sentence(self, sentence_exp):
        word = self.mysql.find_word_by_sentence_exp(sentence_exp)
        return [x[0] for x in word]

    @teststep
    def get_star_words(self):
        """获取标星单词"""
        star_ids = self.mysql.find_star_word_id(gv.STU_ID)
        star_list = [self.mysql.find_word_by_id(s_id)[0][0] for s_id in star_ids]
        return star_list

    @teststep
    def get_familiar_words(self):
        """获取标熟单词"""
        familiar_ids = self.mysql.find_familiar_word_id(gv.STU_ID)
        familiar_list = [self.mysql.find_word_by_id(f_id)[0][0] for f_id in familiar_ids]
        return familiar_list

    @teststep
    def get_word_level(self,word):
        """获取单词的熟练度"""
        level = self.mysql.find_word_level(gv.STU_ID, word)
        return int(level)

    @teststep
    def change_play_times(self, time):
        """更改练习次数"""
        self.mysql.update_play_times(gv.STU_ID, time)

    @teststep
    def change_today_word_count(self, count):
        """更改今日练习词数"""
        self.mysql.update_today_word_count(gv.STU_ID, count)

    @teststep
    def change_today_new_count(self, count):
        """更改今日新词数"""
        self.mysql.update_today_new_count(gv.STU_ID, count)

    @teststep
    def delete_all_star(self):
        """删除所有star数据"""
        self.mysql.delete_all_star(gv.STU_ID)

    @teststep
    def delete_all_score(self):
        """删除所有score数据"""
        self.mysql.delete_all_score(gv.STU_ID)

    @teststep
    def delete_all_word(self):
        """删除用户所有单词数据"""
        self.mysql.delete_all_word(gv.STU_ID)

    @teststep
    def delete_all_record(self):
        """删除所有去重记录"""
        self.mysql.delete_all_record(gv.STU_ID)

    def delete_all_fluency_flag(self):
        """删除所有标星标熟记录"""
        self.mysql.delete_fluency_flag(gv.STU_ID)

    @teststep
    def get_need_recite_count(self,level):
        """获取需要复习的单词数"""
        words = self.mysql.find_range_fluency(gv.STU_ID, level)
        return len(words)

    @teststep
    def change_new_word_level(self, before, after):
        """更改熟练度"""
        self.mysql.update_level_zero(gv.STU_ID, before, after)

    @teststep
    def get_different_level_words(self, level):
        """获取新词个数"""
        words = self.mysql.find_word_different_level(gv.STU_ID, level)
        return len(words)
