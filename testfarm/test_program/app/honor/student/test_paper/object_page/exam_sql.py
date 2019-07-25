#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/27 15:41
# -----------------------------------------
from testfarm.test_program.app.honor.student.word_book.object_page.mysql_data import WordBookSql


class ExamSql(WordBookSql):

    # ========================= 删除试卷记录操作 ======================================
    def delete_all_exam_wrong(self, stu_id):
        """删除试卷所有错题记录"""
        sql = "DELETE FROM exam_student_wrong WHERE  student_id ='%s'" % stu_id
        self.execute_sql_only(sql)

    def delete_all_exam_record(self, stu_id):
        """删除试卷所有记录"""
        sql = "DELETE FROM exam_student_record WHERE  student_id ='%s'" % stu_id
        self.execute_sql_only(sql)

    def delete_student_all_exams(self, stu_id):
        """删除所有试卷"""
        sql = "DELETE FROM exam_student WHERE  student_id ='%s'" % stu_id
        self.execute_sql_only(sql)