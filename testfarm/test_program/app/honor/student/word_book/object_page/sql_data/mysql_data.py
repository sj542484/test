import sys
import traceback
import pymysql

from conf.decorator import teststeps
from conf.base_config import GetVariable as gv


class MysqlData:
    @classmethod
    def start_db(cls):
        """启动数据库"""
        cls.db = pymysql.connect(gv.HOST, gv.USER_NAME, gv.PASSWORD, gv.DB)
        cls.cursor = cls.db.cursor()
        print('启动数据库')

    def close_db(self):
        print('关闭数据库')
        self.db.close()

    def execute_sql_return_result(self, sql):
        result = 0
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.db.commit()
        except:
            print(sys.exc_info()[0], sys.exc_info()[1])
            self.db.rollback()
        return result

    def execute_sql_only(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print(sys.exc_info()[0], sys.exc_info()[1])
            self.db.rollback()

    def find_word_by_explain(self, prop, exp):
        """根据翻译查找单词"""
        sql = "SELECT wb.vocabulary FROM wordbank AS wb,wordbank_translation AS wt " \
              "WHERE wb.id = wt.wordbank_id AND wt.part_of_speech = '{0}' " \
              "AND wt.translation = '{1}'".format(prop, exp)
        return self.execute_sql_return_result(sql)

    def find_word_by_explain_no_prop(self, exp):
        """根据翻译查找单词"""
        sql = "SELECT wb.vocabulary FROM wordbank AS wb,wordbank_translation AS wt " \
              "WHERE wb.id = wt.wordbank_id AND wt.translation = '{}'".format(exp)
        return self.execute_sql_return_result(sql)

    def find_student_id(self, phone):  # 根据翻译查询指定单词
        """根据手机号查找自己的student id"""
        sql = "SELECT ua.id FROM user_account AS ua,`user` WHERE ua.user_id = `user`.id and `user`.phone = '{}' " \
              "AND ua.user_type_id =5" .format(phone)
        return self.execute_sql_return_result(sql)

    def find_all_fluency_id(self, stu_id):
        """获取所有Id"""
        sql = "SELECT wordbank_id FROM word_student_fluency WHERE student_id = '%s'" % stu_id
        return self.execute_sql_return_result(sql)

    def find_fluency_equal_zero(self, stu_id):
        """获取所有Id"""
        sql = "SELECT id FROM word_student_fluency WHERE student_id = '%s' AND fluency_level = '0' " % stu_id
        return self.execute_sql_return_result(sql)

    def find_range_fluency(self, stu_id, level):
        """根据student id 查找对应等级的单词的id"""
        sql = "SELECT id FROM word_student_fluency WHERE student_id = '%s' and fluency_level BETWEEN 1 " \
              "AND '%s'" % (stu_id, str(level))
        return self.execute_sql_return_result(sql)


    def find_word_by_sentence_exp(self, exp):
        """根据句子的解释查找单词"""
        sql = "SELECT wordbank.vocabulary FROM wordbank,wordbank_sentence AS ws WHERE wordbank.id =     " \
              "ws.wordbank_id AND ws.`explain` = '%s'" % exp
        return self.execute_sql_return_result(sql)

    def find_word_by_id(self, word_id):
        """根据id查找单词"""
        sql = "SELECT vocabulary FROM wordbank where id = '%s'" % word_id
        return self.execute_sql_return_result(sql)

    def find_id_by_word(self, word):
        """根据单词查询单词id"""
        sql = "SELECT id FROM wordbank where vocabulary= '%s'" % word
        return self.execute_sql_return_result(sql)

    def find_student_not_set_word_in_ids(self, stu_id, word_ids):
        """查询学生下不去重的单词"""
        sql = "SELECT wordbank_id, translation_id FROM word_student_fluency WHERE student_id = '{0}'" \
              " AND wordbank_id in {1}".format(stu_id, word_ids)
        return self.execute_sql_return_result(sql)

    def find_student_not_set_word_eql_id(self, stu_id, word_id):
        sql = "SELECT wordbank_id, translation_id FROM word_student_fluency WHERE student_id = '{0}'" \
              " AND wordbank_id = '{1}'".format(stu_id, word_id)
        return self.execute_sql_return_result(sql)

    def find_student_word_and_explain(self, word_info):
        """查询单词与翻译"""
        sql = "SELECT CONCAT(wordbank_translation.part_of_speech,wordbank_translation.translation)," \
              "wordbank.vocabulary FROM wordbank, wordbank_translation " \
              "WHERE wordbank.id= wordbank_translation.wordbank_id AND wordbank.id='{0}'" \
              " AND wordbank_translation.id = '{1}'".format(word_info[0], word_info[1])
        return self.execute_sql_return_result(sql)

    def find_word_different_level(self, stu_id, level):
        """查找所有新词"""
        sql = "SELECT wordbank_id FROM word_student_fluency WHERE student_id = '%s' AND  fluency_level " \
              "='%s'" % (stu_id, level)
        return self.execute_sql_return_result(sql)


    def find_word_level(self, stu_id, word):
        """查找单词的熟练度"""
        sql = "SELECT fluency_level from wordbank,word_student_fluency as wsf where" \
              " wordbank.id = wsf.wordbank_id AND wsf.student_id = '%s' AND wordbank.vocabulary = '%s'" \
              % (stu_id, word)
        return self.execute_sql_return_result(sql)

    def find_book_label(self, stu_id):
        """查询标签id"""
        sql = "SELECT word_homework_id FROM word_student_fluency WHERE student_id = '{}' " \
              "GROUP BY word_homework_id" .format(stu_id)
        return self.execute_sql_return_result(sql)

    def find_word_homework_name(self, word_homework_id):
        """根据标签id 查询标签名称"""
        sql = "SELECT name FROM word_homework WHERE id = '{}'" .format(word_homework_id)
        return self.execute_sql_return_result(sql)

    def find_homework_id_by_name(self, homework_name):
        sql = "SELECT id FROM word_homework WHERE name = '{}'".format(homework_name)
        return self.execute_sql_return_result(sql)

    def find_label_id_by_homework_id(self, student_id, homework_id):
        sql = 'SELECT label_ids FROM word_student_fluency WHERE student_id= "{0}" ' \
              ' and word_homework_id= "{1}" GROUP BY label_ids'.format(student_id, homework_id)
        return self.execute_sql_return_result(sql)

    def find_wordbank_by_label_id(self, label_id):
        sql = 'SELECT content FROM wordbank_label_overview WHERE label_id = "{}"'.format(label_id)
        return self.execute_sql_return_result(sql)

    def find_word_by_label(self, stu_id, word_homework_id):
        """查询指定用户下，对应标签的"""
        sql = "SELECT wordbank_id,fluency_level FROM word_student_fluency WHERE student_id = '{0}' AND " \
              "word_homework_id = '{1}'" .format(stu_id, word_homework_id)
        return self.execute_sql_return_result(sql)

    def find_star_word_id(self, stu_id):
        """查询标星单词"""
        sql = "SELECT wordbank_id FROM word_student_fluency_flag WHERE student_id ='%s' AND flag = " \
              "'star_word'" % stu_id
        return self.execute_sql_return_result(sql)

    def find_familiar_word_id(self, stu_id):
        """查询标熟单词"""
        sql = "SELECT wordbank_id FROM word_student_fluency_flag WHERE student_id ='%s' AND flag = " \
              "'familiar_word'" % stu_id
        return self.execute_sql_return_result(sql)

    def find_stu_exam(self, stu_id):
        """查找学生所有试卷"""
        sql = "SELECT quotation_id FROM exam_student WHERE student_id ='%s' and score is not NULL " % stu_id
        return self.execute_sql_return_result(sql)

    def find_exam_name_by_id(self, exam_id):
        """根据试卷名称查找"""
        sql = "SELECT `name` FROM test_quotation WHERE id = '{}'".format(exam_id,)
        return self.execute_sql_return_result(sql)

    def find_exam_detail_by_id(self, exam_id):
        """根据试卷id 查找试卷题型"""
        sql = "SELECT section_id FROM exam_student_record WHERE quotation_id = '%d'" % exam_id
        return self.execute_sql_return_result(sql)

    def find_ques_name_by_id(self, ques_id):
        """根据试卷id 查找试卷题型"""
        sql = "SELECT name FROM user_quoted_testbank WHERE id = '{}'".format(ques_id)
        return self.execute_sql_return_result(sql)

    def find_wrong_right_ids_by_id(self, stu_id, ques_id):
        """查找当前题目 错题与对题"""
        sql = "SELECT wrong_ids,right_ids FROM exam_student_record WHERE  student_id ='%s' " \
              "and section_id = '%d'" % (stu_id, ques_id)
        return self.execute_sql_return_result(sql)

    def find_answer_by_id(self, stu_id, ques_id):
        """根据题目id 查找错题"""
        sql = 'SELECT answer FROM exam_student_wrong WHERE  student_id ="%s" ' \
              'and section_id = "%s"' % (stu_id, ques_id)
        return self.execute_sql_return_result(sql)

    def find_tip_word_by_id(self, bank_id):
        """根据id 查找正确的题"""
        sql = "SELECT testbank_item_value FROM user_quoted_testbank_entity WHERE id = '%s'" % (bank_id,)
        return self.execute_sql_return_result(sql)

    def find_teacher_word_label_id(self, stu_id):
        sql = "SELECT whlm.label_id FROM  word_homework_student as whs, word_homework_label_map as whlm " \
              "WHERE whs.word_homework_id = whlm.word_homework_id AND whs.auth_type =2 " \
              "AND whlm.student_id = '%s' GROUP BY whlm.created_at DESC" % stu_id
        return self.execute_sql_return_result(sql)

    def find_system_word_label_id(self, stu_id):
        sql = "SELECT whlm.label_id FROM  word_homework_student as whs, word_homework_label_map as whlm " \
              "WHERE whs.word_homework_id = whlm.word_homework_id AND whs.auth_type =1 " \
              "AND whlm.student_id = '%s' GROUP BY whlm.created_at DESC" % stu_id
        return self.execute_sql_return_result(sql)

    def find_word_by_label_id(self, homework_id):
        sql = "SELECT content FROM `wordbook_rebuild`.`wordbank_label_overview` WHERE `label_id` = '%s' " % homework_id
        return self.execute_sql_return_result(sql)



    def update_play_times(self, stu_id, times):
        """更改练习次数"""
        sql = "UPDATE user_student_data SET `value` = '%s' WHERE user_account_id = '%s' AND `key` = " \
              "'word_play_times'" % (times, stu_id)
        self.execute_sql_only(sql)

    def update_today_word_count(self, stu_id, count):
        """更改今日练习个数"""
        sql = "UPDATE user_student_data SET `value` = '%s' WHERE user_account_id = '%s' AND `key` = " \
              "'today_word_count'" % (count, stu_id)
        self.execute_sql_only(sql)

    def update_today_new_count(self, stu_id, count):
        """更改今日新词个数"""
        sql = "UPDATE user_student_data SET `value` = '%s' WHERE user_account_id = '%s' AND `key` = " \
              "'today_new_count'" % (count, stu_id)
        self.execute_sql_only(sql)


    def update_level_zero(self, stu_id, before, after):
        """变更单词的熟练度"""
        sql = "UPDATE word_student_fluency SET fluency_level = '%s' WHERE student_id= '%s' and " \
              "fluency_level aq1= '%s'" % (after, stu_id, before)
        self.execute_sql_only(sql)

    def update_word_record(self, date, stu_id):
        """根据student_id 对已学单词去重"""
        sql = "UPDATE `word_homework_student_record` SET `created_at` = '%s' WHERE `student_id` = %s" % (
            str(date), stu_id)
        self.execute_sql_only(sql)

    def update_word_date(self, date, student_id, level):
        """根据单词熟练度表的id 更改单词的时间，以让单词处于指定轮次的复习"""
        sql = "UPDATE word_student_fluency SET last_finish_at = '%s' WHERE student_id= '%s' and " \
              "fluency_level BETWEEN 1 AND '%s'" % (str(date), student_id, level)
        self.execute_sql_only(sql)




    def delete_all_star(self, stu_id):
        """删除所有星星"""
        sql = "DELETE FROM user_student_data where user_account_id = '%s'AND `key` = 'star' " % stu_id
        self.execute_sql_only(sql)

    def delete_all_score(self, stu_id):
        """删除所有分数"""
        sql = "DELETE FROM user_student_data where user_account_id = '%s'AND `key` = 'score'" % stu_id
        self.execute_sql_only(sql)

        # 试卷
    def delete_all_record(self, student_id):
        """删除用户去重记录"""
        sql = "DELETE FROM word_homework_student_record WHERE student_id = '%s'" % student_id
        self.execute_sql_only(sql)

    def delete_fluency_flag(self, student_id):
        """删除标星标熟数据"""
        sql = "DELETE FROM word_student_fluency_flag where student_id = '%s'" % student_id
        self.execute_sql_only(sql)


    def delete_all_word(self, student_id):
        """删除所有单词"""
        sql = "DELETE FROM word_student_fluency WHERE student_id = '%s'" % student_id
        self.execute_sql_only(sql)

    def delete_all_exam_wrong(self, stu_id):
        """删除试卷所有错题记录"""
        sql = "DELETE FROM exam_student_wrong WHERE  student_id ='%s'" % stu_id
        self.execute_sql_only(sql)

    def delete_all_exam_record(self, stu_id):
        """删除试卷所有记录"""
        sql = "DELETE FROM exam_student_record WHERE  student_id ='%s'" % stu_id
        self.execute_sql_only(sql)

    def delete_student_all_exams(self, stu_id):
        sql = "DELETE FROM exam_student  student_id ='%s'" % stu_id
        self.execute_sql_only(sql)

    # def delete_vanclass_homework(self, vanclass_id):
    #     sql = 'DELETE FROM `wordbook_rebuild`.`word_homework` WHERE `public_vanclass_ids` = %s' % vanclass_id
    #     self.execute_sql_only(sql)

    def delete_student_word_homework(self, stu_id):
        sql = 'DELETE FROM word_homework_student WHERE student_id = "%s" ' % stu_id
        self.execute_sql_only(sql)

    def delete_student_homework_record(self, stu_id):
        sql = 'DELETE FROM word_homework_student_record WHERE student_id = "%s" ' % stu_id
        self.execute_sql_only(sql)

    def delete_student_homework_wrong(self, stu_id):
        sql = 'DELETE FROM word_homework_student_wrong WHERE student_id = "%s" ' % stu_id
        self.execute_sql_only(sql)

    def delete_homework_label_map_info(self, stu_id):
        sql = 'DELETE FROM word_homework_label_map WHERE student_id = "%s" ' % stu_id
        self.execute_sql_only(sql)