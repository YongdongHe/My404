from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.databases.tables import User
from mod.databases.tables import Article
from mod.Auth.SessionHelper import SessionHelper
import tornado.web
import tornado.gen
import urllib
import hashlib

class BlogHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    def get(self):
        sessionhelper = SessionHelper(self,self.db)
        correct_user = sessionhelper.checkSession()
        blog_user_id = self.get_argument("id")
        blog_user = self.db.query(User).filter(User.user_id == blog_user_id).first()
        if blog_user == None:
            self.render("homepage/404error.html",
                correct_user=correct_user)
        else:
            articles = self.db.query(Article).filter(Article.user_id == blog_user_id).all()
            email = blog_user.user_email
            default = "http://www.example.com/default.jpg"
            size = 40
            gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
            gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
            self.render("blog.html",
                correct_user=correct_user,
                articles=articles,
                blog_user=blog_user,
                gravatar_url=gravatar_url)
    def post(self):
    	pass