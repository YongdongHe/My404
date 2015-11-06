import os.path
import random
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from mod.databases.tables import Session
from mod.databases.tables import User
from mod.Auth.SessionHelper import SessionHelper
from mod.BlogHandler.BlogHandler import GravatarHelper

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db     
    
    def getCurrentUser(self):
        try:
            session = str(self.get_secure_cookie("session"))
            user_id = int(self.get_secure_cookie("userid"))
            if session == None or user_id == None:
                print 'Error'
                return None
            correct_session = self.db.query(Session).filter(Session.session_value == session).first()
            self.db.commit()
            if (correct_session != None) and (correct_session.user_id == user_id):
                correct_user = self.db.query(User).filter(User.user_id == user_id).first()
                # print correct_user.user_id
                return correct_user
            else:
                return None
        except Exception, e:
            self.db.rollback()
            print 'Exception e in mod.Auth.SessionHelper.checkSession:%s'%(str(e))
            return None

