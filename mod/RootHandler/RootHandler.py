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
    def get(self,args):
        print "In home handler:"+args[0::]
        user_session = str(self.get_secure_cookie("session"))
        self.render('homepage/%s.html'%(args[0::]),register=True,session=user_session)