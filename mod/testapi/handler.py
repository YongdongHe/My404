from tornado.httpclient import HTTPRequest, AsyncHTTPClient
import tornado.web
import tornado.gen
import urllib

class DbHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("this is a db test")


