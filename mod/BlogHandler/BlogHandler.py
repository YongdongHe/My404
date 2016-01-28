from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.BaseHandler import BaseHandler
from mod.databases.tables import User
from mod.databases.tables import Article
from mod.Auth.SessionHelper import SessionHelper
import tornado.web
import tornado.gen
import urllib
import hashlib
class BlogHandler(BaseHandler):
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
            gravatar_url =GravatarHelper(blog_user.user_email,240).getUrl()
            self.render("blog.html",
                correct_user=correct_user,
                articles=articles,
                blog_user=blog_user,
                gravatar_url=gravatar_url)
    def post(self):
    	pass

class GravatarHelper(object):
    """docstring for GravatarHelper"""
    def __init__(self, email,size):
        super(GravatarHelper, self).__init__()
        self.email = email
        self.size = size

    def getUrl(self):
        default = "http://www.example.com/default.jpg"
        size = self.size
        gravatar_url = "http://secure.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':"retro", 's':str(size)})
        return gravatar_url
        