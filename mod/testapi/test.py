#coding=utf8
import requests
from sgmllib import SGMLParser

class RunningParser(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
    
    def getRunningTable(self, text):
        self.table = []
        self.row = []
        self.flag = 0
        self.form = 0
        # _cookies = cookies
        # _url = 'http://zccx.seu.edu.cn/SportWeb/gym/gymExercise/gymExercise_query_result_2.jsp?xh=%s'%(card_id)
        self.feed(text)

    def start_form(self, attrs):
        self.form += 1

    def end_form(self):
        self.form -= 1
        msg = {}
        msg['sign_date'] = self.row[3]
        msg['sign_time'] = self.row[4]
        msg['sign_effect'] = self.row[6]
        self.table.append(msg)
        self.row = []


    def start_td(self, attrs):
        self.flag += 1

    def end_td(self):
        self.flag -= 1

    def handle_data(self, text):
        if self.flag == 3 and self.form == 1:
            self.row.append(text)



#spider = RunningParser()
#spider.getRunningTable('213151933')
#for item in spider.table:
#    print item
