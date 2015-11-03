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
            session = str(self.get_secure_cookie("session"))
            if session!= None:
                layout_user = self.db.query(Session).filter(Session.session_value == session).first()
                self.db.delete(layout_user)
                self.db.commit()
                pass
            self.clear_cookie("session")
            self.clear_cookie("userid")
            self.render("homepage/index.html",correct_user = None)
        except Exception, e:
            self.db.rollback()
            print 'Exception e in mod.LogoutHandler.get:%s'%(str(e))
            self.render("homepage/index.html",correct_user = None)
        
