#coding=utf-8
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.databases.tables import Article
from mod.databases.tables import Comment
from mod.databases.tables import User
from mod.Auth.SessionHelper import SessionHelper
from mod.BlogHandler.BlogHandler import GravatarHelper
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
        comments = self.db.query(Comment).filter(Comment.article_id == article_id).order_by(Comment.comment_id).all()
        urls={}
        for comment in comments:
            commenter = self.db.query(User).filter(User.user_id == comment.commenter_id).first()
            urls[commenter.user_id]=GravatarHelper(commenter.user_email,240).getUrl()
        self.render("article.html",
            user_id=article.user_id,    
            user_name=article.user,
            article_title=article.title,
            article_content=article.content,
            comments=comments,
            urls=urls,
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



class ArticleContentModule(tornado.web.UIModule):
    def render(self,article_content):
        return article_content

class CommentItemModule(tornado.web.UIModule):
    def render(self):
        return 's'