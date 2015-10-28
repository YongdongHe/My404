from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.databases.tables import Article
from mod.Auth.SessionHelper import SessionHelper
import tornado.web
import tornado.gen
import urllib

class ArticleHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        pass

    def post(self):
    	pass