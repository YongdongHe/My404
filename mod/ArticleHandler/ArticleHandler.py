from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.databases.tables import Article
import tornado.web
import tornado.gen
import urllib

class ArticleHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
    	article_id = self.get_argument("article_id")
    	data = self.db.query(Article).filter(Article.article_id == article_id).first()
    	print data
        self.render("article.html",article_name = data.title , article_content = data.content ,arrs = ['s','ss'])
    def post(self):
    	pass