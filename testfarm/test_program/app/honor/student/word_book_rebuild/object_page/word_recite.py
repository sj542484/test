from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.word_book_rebuild.object_page.clear_user_data import CleanDataPage
from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from app.honor.student.word_book_rebuild.object_page.data_handle import WordDataHandlePage
from conf.decorator import teststeps


class ReciteProgress(BasePage):

    def __init__(self):
        self.common = WordDataHandlePage()
        self.clean = CleanDataPage()
        self.word = WordBook()
        self.home = HomePage()

    @teststeps
    def recite_progress(self, i,level):
        """复习单词过程"""
        self.get_every_recite_count()
        recite_b = self.common.get_different_level_words(1)
        recite_a = self.common.get_different_level_words(0)

        if recite_a == 0:  # 若没有新词出现，则会复习F<=4 的所有单词 提前复习
            recite_count = self.common.get_need_recite_count(4)
        else:              # 若新词存在，则只复习到F<= level 的单词
            recite_count = self.common.get_need_recite_count(level)

        word_result = self.word.play_word_book()  # 单词本 具体过程

        vocab_recite = word_result[2]  # 词汇选择组
        vocab_apply = word_result[3]
        if len(word_result[4]) != 0:  # 游戏名称数组
            if word_result[4][0] != '闪卡练习(新词)':
                self.vocab_group(vocab_recite, recite_b)
                self.no_vocab_group(vocab_apply, recite_count)
                if word_result[1] >= 28:
                    if word_result[0] > 0:
                        print('★★★ Error-复习词大于28时，有新词出现！！！')
                else:
                    if i == 0:
                        if word_result[0] <= 10:
                            print('新词个数小于等于10，正确！')
                        else:
                            print('★★★ Error-新词个数大于10!')
                    else:
                        if 10 > word_result[0] >= 3:
                            print('新词个数大于3 小于10,正确！')
                        else:
                            if word_result[0] != 0:
                                print('★★★ Error-新词个数小于3！\n')

                print('----------------------------------')

    @teststeps
    def vocab_group(self, vocab_recite, recite_b):
        """判断B轮单词是否根据其个数分组"""
        if recite_b != 0:   # B轮单词不为0
            if recite_b <= 10:
                if vocab_recite != 1:
                    print('★★★ Error-B轮单词小于10，词汇选择组数为%d，应为1组!\n' % vocab_recite)
                else:
                    print('B轮单词为%d,已分为%d组' %(recite_b, vocab_recite))
            elif 21 > recite_b > 10:
                if vocab_recite != 2:
                    print('★★★ Error-B轮单词小于21大于10，词汇选择组数为%d，应为2组!\n' % vocab_recite)
                else:
                    print('B轮单词为%d,已分为%d组' %(recite_b, vocab_recite))
            elif 31 > recite_b > 20:
                if vocab_recite != 3:
                    print('★★★ Error-B轮单词小于31大于20，词汇选择组数为%d，应为3组!\n' % vocab_recite)
                else:
                    print('B轮单词为%d,已分为%d组' %(recite_b, vocab_recite))
        else:
            if vocab_recite != 0:
                print('★★★ Error-无B轮复习却出现词汇选择\n')

    @teststeps
    def no_vocab_group(self, vocab_apply, recite_count):
        """判断C、D、E轮是否根据其复习个数进行分组
        当没有新词和进阶词汇会进行提前复习（复习词为0<F<5的词）
        """
        if recite_count != 0:
            if recite_count <= 10:
                if vocab_apply != 1:
                    print('★★★ Error-本组需复习词数为%d小于10，词汇运用及单词拼写已分为%d组，应为1组!\n' %(recite_count,vocab_apply))
                else:
                    print('本组需复习词数为%d，词汇运用及单词拼写已分为%d组' %(recite_count, vocab_apply))
            elif 21 > recite_count > 10:
                if vocab_apply != 2:
                    print('★★★ Error-本组需复习词数为%d小于21大于10，词汇运用及单词拼写已分为%d组，应为2组!\n' %(recite_count,vocab_apply))
                else:
                    print('本组需复习词数为%d，词汇运用及单词拼写已分为%d组' %(recite_count, vocab_apply))

            elif 31 > recite_count > 20:
                if vocab_apply != 3:
                    print('★★★ Error-本组需复习词数为%d小于31大于20，词汇运用及单词拼写已分为%d组，应为3组!\n' %(recite_count,vocab_apply))
                else:
                    print('本组需复习词数为%d，词汇运用及单词拼写已分为%d组' %(recite_count, vocab_apply))

    @teststeps
    def get_every_recite_count(self):
        """打印每个"""
        print('\n目前数据库数据如下：')
        for i in range(0, 6):
            count = self.common.get_different_level_words(i)
            if i == 0:
                print('熟练度为0的个数(新词)：', count)
            elif i == 1:
                print('熟练度为1的个数(b轮)：', count)
            elif i == 2:
                print('熟练度为2的个数(c轮)：', count)
            elif i == 3:
                print('熟练度为3的个数(d轮)：', count)
            elif i == 4:
                print('熟练度为4的个数(e轮)：', count)
            else:
                print('熟练度为5的个数：', count)

        print('----------------------------------')

    @teststeps
    def limit_page_handle(self):
        """出现次数限制页面处理过程"""
        self.common.change_play_times(1)  # 重置今日练习次
        self.word.limit_confirm_button()  # 确定
        if self.word.wait_check_start_page():
            self.word.word_start_button()  # 点击 Go按钮

    @teststeps
    def set_recite_date(self, level):
        gv.LEVEL = level
        if level == 1:
            gv.TIME_COUNT = 1
            print('\n#### 本轮为B轮复习 ####\n')
        elif level == 2:
            gv.TIME_COUNT = 10
            print('\n#### 本轮为C轮复习 ####\n')
        elif level == 3:
            gv.TIME_COUNT = 30
            print('\n#### 本轮为D轮复习 ####\n')
        elif level == 4:
            gv.TIME_COUNT = 60
            print('\n#### 本轮为E轮复习 ####\n')

        self.common.change_word_date()
        self.home.click_back_up_button()
        self.clean.clean_cache()
        new_word = self.common.get_different_level_words(0)
        if new_word == 0:
            total = self.common.get_need_recite_count(5)
            print("已无生词, 单词会提前复习, 复习单词数为：", total)
        else:
            total = self.common.get_need_recite_count(level)  # 需要复习的个数
            print('本轮不加提前复习的词数为：', total)







