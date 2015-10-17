from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.databases.tables import User
from mod.databases.tables import Article
import tornado.web
import tornado.gen
import urllib

class UserhomeHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    def get(self):
    	user_id = self.get_argument("user_id")
        print user_id
    	user = self.db.query(User).filter(User.user_id == user_id).first()
        articles = self.db.query(Article).filter(Article.user == user.user_name).all()
        self.write(user.user_name)
        print articles
        self.render("userhome.html", user = user , articles = articles )
    def post(self):
    	pass