#coding=utf-8
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.databases.tables import Article
from mod.Auth.SessionHelper import SessionHelper
import tornado.web
import tornado.gen
import urllib
import time

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
        sessionhelper = SessionHelper(self,self.db)
        correct_user = sessionhelper.checkSession()
        response = {}
        if correct_user!=None:
            try:
                article_content = self.get_argument("article_content")
                print article_content
                article_title = self.get_argument("article_title")
                username = correct_user.user_name
                posttime = time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
                article = Article(user_id = correct_user.user_id,
                    title = article_title,
                    content = article_content,
                    user = username,
                    time = posttime)
                self.db.add(article)
                self.db.commit()
                response["status"]=200
                response["data"]='success'
                self.write(response)
            except Exception, e:
                response["status"]=400
                response["data"]=str(e)
                self.write(response)
                raise e
        else:
            self.render("homepage/login.html",correct_user=None)
    	