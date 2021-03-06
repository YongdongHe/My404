from tornado.httpclient import HTTPRequest, AsyncHTTPClient,HTTPError
from mod.databases.tables import Article
from test import RunningParser
import json
import tornado.web
import tornado.gen
import urllib

class TestHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        loginurl1 = "http://ids2.seu.edu.cn/amserver/UI/Login?goto=http%3A%2F%2Fzccx.seu.edu.cn%2F"

        runurl = "http://zccx.seu.edu.cn"
        testurl = "http://zccx.seu.edu.cn/student/queryCheckInfo.jsp"

        username = '213151933'
        password = 'vme2744394782'
        client = AsyncHTTPClient()


        data = {
            "Login.Token1" : username,
            "Login.Token2" : password,
            'goto' : "http://mynew.seu.edu.cn/loginSuccess.portal",
            'gotoOnFail' : "http://mynew.seu.edu.cn/loginFailure.portal"
            }

        data1 = {
            'IDToken0':   '',
            'IDToken1':username,
            'IDToken2':password,
            'IDButton':'Submit',
            'goto':'http://zccx.seu.edu.cn/',
            'gx_charset':'gb2312'
            }

        cookie1 = ''
        request = HTTPRequest(
            loginurl1,
            method='POST',
            body = urllib.urlencode(data1),
            follow_redirects=False
            )
        initcookie = ''
        try:
            response = yield client.fetch(request)
        except HTTPError as e:
            print e.response.code
            self.write(e.response.headers)
            initcookie = e.response.headers['Set-Cookie']
       
        print initcookie
        init_cookie1 = initcookie.split(';')[4].split(',')[1]#+initcookie.split(';')[0]
        


        print init_cookie1
        
        header = {
            'Host':'zccx.seu.edu.cn',
            'Accept': 'textml,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Referer':'http://zccx.seu.edu.cn/',
            'Connection':'Keep-alive',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cookie':init_cookie1+';'+cookie1+';'+';amblcookie=02'
            }

        request = HTTPRequest(
            runurl,
            method='GET',
            headers = header
            )
        try:
            response = yield client.fetch(request)
            print response.headers['Set-Cookie']

            cookie1 = response.headers['Set-Cookie']
            header['Cookie'] = init_cookie1+';'+cookie1+';'+';amblcookie=02'


            request = HTTPRequest(
                testurl,
                headers = header,
                request_timeout=8
                )
            
            response = yield client.fetch(request)
            self.write(response.body)
        except HTTPError as e:
            print(str(e))
            self.write("Time Out")
        # except HTTPError as e:
        #     # self.write(e.response)
        #     print e.response.code
        #     self.write(e.response.headers)
        #     init_cookie1 = e.response.headers['Set-Cookie'].split(';')[0]


        # header['Cookie'] = init_cookie1+';'+cookie1+';'+';amblcookie=02'
        # request = HTTPRequest(
        #     testurl,
        #     headers = header,
        #     request_timeout=8,
        #     )
        # try:
        #     response = yield client.fetch(request)
        #     self.write(response.body)
        # except HTTPError as e:
        #     # self.write(e.response)
        #     print e.response.code
        #     self.write(e.response.headers)
            # init_cookie1 = e.response.headers['Set-Cookie'].split(';')[0]
        # self.write(response.body)
        self.finish()





class TestapiHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
    	loginurl1 = "http://ids2.seu.edu.cn/amserver/UI/Login?goto=http%3A%2F%2Fzccx.seu.edu.cn%2F"

        runurl = "http://zccx.seu.edu.cn"
        testurl = "http://zccx.seu.edu.cn/student/queryCheckInfo.jsp"

        username = '213130956'
        password = 'xiawucha0107'
        card_id = self.get_argument('card')
        client = AsyncHTTPClient()


        data = {
            "Login.Token1" : username,
            "Login.Token2" : password,
            'goto' : "http://mynew.seu.edu.cn/loginSuccess.portal",
            'gotoOnFail' : "http://mynew.seu.edu.cn/loginFailure.portal"
            }

        data1 = {
            'IDToken0':   '',
            'IDToken1':username,
            'IDToken2':password,
            'IDButton':'Submit',
            'goto':'http://zccx.seu.edu.cn/',
            'gx_charset':'gb2312'
            }

        cookie1 = ''
        request = HTTPRequest(
            loginurl1,
            method='POST',
            body = urllib.urlencode(data1),
            follow_redirects=False
            )
        initcookie = ''
        try:
            response = yield client.fetch(request)
        except HTTPError as e:
            print e.response.code
            # self.write(e.response.headers)
            initcookie = e.response.headers['Set-Cookie']
       
        print initcookie
        init_cookie1 = initcookie.split(';')[4].split(',')[1]#+initcookie.split(';')[0]
        


        print init_cookie1
        
        header = {
            'Host':'zccx.seu.edu.cn',
            'Accept': 'textml,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Referer':'http://zccx.seu.edu.cn/',
            'Connection':'Keep-alive',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cookie':init_cookie1+';'+cookie1+';'+';amblcookie=02'
            }

        request = HTTPRequest(
            runurl,
            method='GET',
            headers = header
            )

        
        try:
            response = yield client.fetch(request)
            print response.headers['Set-Cookie']

            cookie1 = response.headers['Set-Cookie']
            header['Cookie'] = init_cookie1+';'+cookie1+';'+';amblcookie=02'  
            getpeurl = "http://zccx.seu.edu.cn/SportWeb/gym/gymExercise/gymExercise_query_result_2.jsp?xh=%s"%(card_id)
            request = HTTPRequest(
                getpeurl,
                headers = header,
                request_timeout=8
                )
            response = yield client.fetch(request)
            spider = RunningParser()
            spider.getRunningTable(response.body)
            # self.write(response.body)
            s = json.dumps(spider.table,ensure_ascii=False)
            self.write(s)
        except HTTPError as e:
            print(str(e))
            self.write("Time Out")
        self.finish()