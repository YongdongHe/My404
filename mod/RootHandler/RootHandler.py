import os.path
import random
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from mod.databases.tables import Session
from mod.databases.tables import User
from mod.Auth.SessionHelper import SessionHelper

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('home.html')


class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
    	user_session = str(self.get_secure_cookie("session"))
        self.render('homepage/index.html',correct_user=None)

class HomePageHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get(self,args):
        askurl = args[0::]
        print "In home handler:"+askurl
        session_helper = SessionHelper(self,self.db)
        correct_user = session_helper.checkSession()
        # correct_user = self.checkSession()
        if askurl == "login":
            ####login
            if correct_user == None:
                self.render('homepage/login.html',
                    correct_user=correct_user)
            else:
                print correct_user.user_id
                self.render('homepage/index.html',
                    correct_user=correct_user)
        elif askurl == "index":
            self.render('homepage/index.html',
                correct_user=correct_user)
        else:
            self.render('homepage/%s.html'%(askurl),
                correct_user=correct_user)
    
    def checkSession(self):
        try:
            session = str(self.get_secure_cookie("session"))
            user_id = int(self.get_secure_cookie("userid"))
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
            print 'Exception e in mod.RootHandler.checkSession:%s'%(str(e))
            return None
