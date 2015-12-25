from tornado.httpclient import HTTPRequest, AsyncHTTPClient,HTTPError
import tornado.web
import tornado.gen

class SeuxkHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render("seuxk.js")
