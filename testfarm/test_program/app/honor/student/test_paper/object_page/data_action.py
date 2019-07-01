import json

from app.student.login.object_page.home_page import HomePage
from app.student.word_book.object_page.sql_data.mysql_data import MysqlData
from conf.base_page import BasePage
from conf.decorator import teststep
from conf.base_config import GetVariable as gv


class DataPage(BasePage):
    """数据操作类"""
    def __init__(self):
        self.mysql = MysqlData()
        self.home = HomePage()

    @teststep
    def delete_student_exam_record(self):
        self.mysql.delete_all_exam_record(gv.STU_ID)
        self.mysql.delete_all_exam_wrong(gv.STU_ID)
        self.mysql.delete_student_all_exams(gv.STU_ID)

    @teststep
    def get_section_id(self, exam_name):
        """根据试卷名称 获取试卷题型的id"""
        db_id = self.mysql.find_stu_exam(gv.STU_ID)
        exam_id = 0

        for i in range(len(db_id)):
            name = self.mysql.find_exam_name_by_id(db_id[i][0])
            if name[0][0] == exam_name:
                exam_id = db_id[i][0]
                break

        section_ids = self.mysql.find_exam_detail_by_id(exam_id)
        return section_ids

    @teststep
    def get_ques_answer(self, section_ids, ques_title):
        """根据题目名称获取当前题目和答案"""
        ques_id = 0
        for i in range(len(section_ids)):
            ques_name = self.mysql.find_ques_name_by_id(section_ids[i][0])
            if ques_name[0][0] in ques_title:
                ques_id = section_ids[i][0]
        ques_answers = self.mysql.find_wrong_right_ids_by_id(gv.STU_ID, ques_id)
        return ques_answers, ques_id

    @teststep
    def get_word(self, bank_id):
        word_info = self.mysql.find_tip_word_by_id(bank_id)
        word = json.loads(word_info[0][0])
        return word

    @teststep
    def get_wrong_answer(self, ques_id):
        answer = self.mysql.find_answer_by_id(gv.STU_ID, ques_id)
        return answer

    @teststep
    def write_json_to_file(self, json_data):
        with open('app/student/test_paper/test_data/data', 'w') as f:
            json.dump(json_data, f, ensure_ascii=False)

    @teststep
    def get_data_json_from_file(self):
        with open('app/student/test_paper/test_data/data', 'r') as f:
            try:
                data_json = json.load(f)
                return data_json
            except:
                return {}





