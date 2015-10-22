import os.path
import random
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('home.html')


class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
    	user_session = str(self.get_secure_cookie("session"))
        self.render('homepage/index.html',register=True,session=user_session)

class HomePageHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get(self,args):
        askurl = args[0::]
        print "In home handler:"+askurl
        user_session = str(self.get_secure_cookie("session"))
        if askurl == "login":
            ####login
            if user_session == None:
                self.render('homepage/login.html',register=True,session=user_session)
            else:
                self.render('homepage/login.html',register=True,session=user_session)
        elif askurl == "index":
            self.render('homepage/index.html',register=True,session=user_session)
        else:
            self.render('homepage/%s.html'%(askurl),register=True,session=user_session)




