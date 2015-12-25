#coding=utf8
from tornado.httpclient import HTTPRequest, AsyncHTTPClient,HTTPError
from bs4 import BeautifulSoup
import requests
from sgmllib import SGMLParser
import tornado.web
import tornado.gen
import urllib
import json

class BusParser(SGMLParser):
    def __init__(self, verbose = 0):
        SGMLParser.__init__(self)
    def getBusTime(self,res):
        self.table = []
        self.flag = 0
        self.feed(res)
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
        try:
            client = AsyncHTTPClient()
            urlGetLineID = 'http://112.2.33.3:5902/wap/line.do?command=toLn'
            reqLine = HTTPRequest(urlGetLineID,request_timeout=8)
            resLineId = yield client.fetch(reqLine)
            soup = BeautifulSoup(resLineId.body)
            lineID = ''
            for option in soup.findAll('option'):
                if option.string == '711':
                    lineID = option['value'][:-4]
                    break
            print lineID
            urlToCompany = 'http://112.2.33.3:5902/wap/line.do?command=toDiss2&stationNo=15&stationName=%E5%B0%86%E5%86%9B%E5%A4%A7%E9%81%93%E8%BF%8E%E7%BF%A0%E8%B7%AF&lineId='+lineID+'&inDown=1&lineName=711&strInfo=%E5%87%BA%E5%8F%A3%E5%8A%A0%E5%B7%A5%E5%8C%BA%E5%AE%A2%E8%BF%90%E7%AB%99%E2%86%92%E5%AE%89%E5%BE%B7%E9%97%A8'
            print urlToCompany
            urlToSchool = 'http://112.2.33.3:5902/wap/line.do?command=toDiss2&stationNo=19&stationName=%E5%B0%86%E5%86%9B%E5%A4%A7%E9%81%93%E8%BF%8E%E7%BF%A0%E8%B7%AF&lineId='+lineID+'&inDown=2&lineName=711&strInfo=%E5%AE%89%E5%BE%B7%E9%97%A8%E2%86%92%E5%87%BA%E5%8F%A3%E5%8A%A0%E5%B7%A5%E5%8C%BA%E5%AE%A2%E8%BF%90%E7%AB%99'
            reqtoC = HTTPRequest(urlToCompany,request_timeout=8)
            reqtoS = HTTPRequest(urlToSchool,request_timeout=8)
            restoC = yield client.fetch(reqtoC)
            restoS = yield client.fetch(reqtoS)
            spider = BusParser()
            s1 = spider.getBusTime(restoC.body)
            s2 = spider.getBusTime(restoS.body)
            s = {'ToCompany':s1, 'ToSchool':s2,'status':200}
            self.write(json.dumps(s,ensure_ascii=False))
        except HTTPError as e:
            print str(e)
            s = {'ToCompany':'', 'ToSchool':'','status':443}
            self.write(json.dumps(s,ensure_ascii=False))
