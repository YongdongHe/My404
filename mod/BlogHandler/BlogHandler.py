from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.databases.tables import User
from mod.databases.tables import Article
from mod.Auth.SessionHelper import SessionHelper
import tornado.web
import tornado.gen
import urllib

class BlogHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    def get(self):
    	sessionhelper = SessionHelper(self,self.db)
    	correct_user = sessionhelper.checkSession()
        blog_user_id = self.get_argument("id")
        articles = self.db.query(Article).filter(Article.user_id == blog_user_id).all()
        for i in articles:
            print i.content
    	self.render("blog.html",correct_user=correct_user,articles=articles)
    def post(self):
    	pass