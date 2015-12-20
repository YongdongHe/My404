#coding=utf8
from tornado.httpclient import HTTPRequest, AsyncHTTPClient,HTTPError
import requests
from sgmllib import SGMLParser
import tornado.web
import tornado.gen
import urllib
import json

class BusParser(SGMLParser):
    def __init__(self, verbose = 0):
        SGMLParser.__init__(self)
    def getBusTime(self,url):
        self.table = []
        self.flag = 0
        r = requests.get(url)
        self.feed(r.text)
        if len(self.table) > 1:
            return self.table[1]
        else:
            return 'NoBus'
    def start_span(self,attrs):
        for k,v in attrs:
            if k == 'class' and v == 'red':
                self.flag = 1
                break
    def end_span(self):
        self.flag = 0
    def handle_data(self, data):
        if self.flag == 1:
            self.table.append(data)

class BusHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        urlToCompany = 'http://112.2.33.3:5902/wap/line.do?command=toDiss2&stationNo=2&stationName=%E5%87%BA%E5%8F%A3%E5%8A%A0%E5%B7%A5%E5%8C%BA&lineId=461&inDown=1&lineName=711&strInfo=%E5%87%BA%E5%8F%A3%E5%8A%A0%E5%B7%A5%E5%8C%BA%E5%AE%A2%E8%BF%90%E7%AB%99%E2%86%92%E5%AE%89%E5%BE%B7%E9%97%A8'
        urlToSchool = 'http://112.2.33.3:5902/wap/line.do?command=toDiss2&stationNo=19&stationName=%E5%B0%86%E5%86%9B%E5%A4%A7%E9%81%93%E8%BF%8E%E7%BF%A0%E8%B7%AF&lineId=461&inDown=2&lineName=711&strInfo=%E5%AE%89%E5%BE%B7%E9%97%A8%E2%86%92%E5%87%BA%E5%8F%A3%E5%8A%A0%E5%B7%A5%E5%8C%BA%E5%AE%A2%E8%BF%90%E7%AB%99'
        spider = BusParser()
        s1 = spider.getBusTime(urlToCompany)
        s2 = spider.getBusTime(urlToSchool)

        s = {'ToCompany':s1, 'ToSchool':s2}
        self.write(json.dumps(s,ensure_ascii=False))