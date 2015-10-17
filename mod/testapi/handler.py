from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.databases.tables import Article
import tornado.web
import tornado.gen
import urllib

class DbHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        data = self.db.query(Article).all()
        for item in data:
        	print item.content




