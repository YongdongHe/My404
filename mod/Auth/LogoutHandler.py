from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.databases.tables import User
from mod.databases.tables import Session
# from mod.Debug.Col import Color
import re
import tornado.web
import tornado.gen
import urllib

class LogoutHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        try:
            self.clear_cookie("session")
            self.clear_cookie("userid")
            self.render("homepage/index.html",correct_user = None)
        except Exception, e:
            print 'Exception e in mod.LogoutHandler.get:%s'%(str(e))
            self.render("homepage/index.html",correct_user = None)
        