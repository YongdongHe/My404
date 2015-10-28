from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.databases.tables import Article
from mod.Auth.SessionHelper import SessionHelper
import tornado.web
import tornado.gen
import urllib
import time

class ArticleWriteHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        sessionhelper = SessionHelper(self,self.db)
        correct_user = sessionhelper.checkSession()
        if correct_user==None:
            self.render("homepage/login.html",correct_user=correct_user)
        else:
            self.render("articlewrite.html",correct_user=correct_user)
