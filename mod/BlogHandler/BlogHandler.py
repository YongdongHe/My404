from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.databases.tables import User
from mod.databases.tables import Article
import tornado.web
import tornado.gen
import urllib

class BlogHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    def get(self):
    	self.render("blog.html",correct_user=None)
    def post(self):
    	pass