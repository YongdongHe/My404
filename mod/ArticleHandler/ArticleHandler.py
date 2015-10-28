from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.databases.tables import Article
from mod.Auth.SessionHelper import SessionHelper
import tornado.web
import tornado.gen
import urllib

class ArticleHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        sessionhelper = SessionHelper(self,self.db)
        article_id = self.get_argument("article_id")
        article = self.db.query(Article).filter(Article.article_id == article_id).first()
        self.render("article.html",
            article_title=article.content,
            user_name=article.user,
            article_content=article.content,
            correct_user=sessionhelper.checkSession())
        pass

    def post(self):
    	pass