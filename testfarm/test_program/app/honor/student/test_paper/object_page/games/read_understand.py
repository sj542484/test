import time
from app.honor.student.games.article_read_understand import ReadUnderstandGame
from app.honor.student.test_paper.object_page.games.listen_select import ListenSelect
from conf.decorator import teststeps


class ReadUnderstand(ReadUnderstandGame):

    @teststeps
    def play_read_understand_game(self, num, exam_json):
        exam_json['阅读理解'] = bank_json = {}
        text = self.rich_text()
        print(text)
        self.drag_operate()
        time.sleep(5)
        ListenSelect().select_operate(num, '阅读理解', bank_json)

    @teststeps
    def read_understand_detail(self, bank_info):
        self.drag_operate()
        ListenSelect().check_result_detail_operate(bank_info, quote_type=2)