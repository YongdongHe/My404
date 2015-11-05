# -*- coding: utf-8 -*-
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

class MessageHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        #get article by id
        sessionhelper = SessionHelper(self,self.db)
        #message box page load

    def post(self):
        #new comment
        sessionhelper = SessionHelper(self,self.db)
        correct_user = sessionhelper.checkSession()
        response = {}
        if correct_user!=None:
            try:
                article_id = self.get_argument("article_id")
                comment_content = self.get_argument("comment_content")
                posttime = time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
                comment = Comment(
                    article_id=article_id, 
                    comment_content=comment_content,
                    commenter_id=correct_user.user_id,
                    commenter_name=correct_user.user_name,
                    comment_time=posttime
                    )
                self.db.add(comment)
                self.db.commit()
                response["status"]=200
                response["data"]='comment success'
                self.write(response)
                self.redirect("/article?article_id=%s"%(article_id))
            except Exception, e:
                response["status"]=400
                response["data"]=str(e)
                self.db.rollback()
                self.write(response)
        else:
            self.render("homepage/login.html",correct_user=None)



# class CommentItemModule(tornado.web.UIModule):
#     def render(self):
#         return 's'