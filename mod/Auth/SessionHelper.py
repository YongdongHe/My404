# -*- coding: utf-8 -*-
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.databases.tables import Session
from mod.databases.tables import User
import re
import tornado.web
import tornado.gen
import urllib

class SessionHelper(object):
    """docstring for SessionHelper"""
    def __init__(self, app,db):
        super(SessionHelper, self).__init__()
        self.app = app
        self.db = db


    def checkSession(self):
        try:
            session = str(self.app.get_secure_cookie("session"))
            user_id = int(self.app.get_secure_cookie("userid"))
            # print session
            # print user_id
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
