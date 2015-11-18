# -*- coding: utf-8 -*-
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.databases.tables import Article,Comment,User,Message
from mod.Auth.SessionHelper import SessionHelper
from mod.BlogHandler.BlogHandler import GravatarHelper
from mod.BaseHandler import BaseHandler
import tornado.web
import tornado.gen
import urllib
import time

class MessageBoxHandler(BaseHandler):
    def get(self):
        response = {}
        current_user = self.current_user()
        self.write("s")
        # if current_user == None:
        #     response["code"]=304
        #     response["data"]="Please log in."
        #     self.write(response)
        # elif:
        #     response["data"]={}
        #     response["data"]["read"]=[]
        #     response["data"]["unread"]=[]
        #     unreads = self.db.query(Message).filter(
        #         Message.user_id == current_user.user_id,
        #         Message.read == 0)
        #     reads = self.db.query(Message).filter(
        #         Message.user_id == current_user.user_id,
        #         Message.read == 1)
        #     for msg in unreads:
                


    def post(self):
        #new comment
        sessionhelper = SessionHelper(self,self.db)
        correct_user = self.getCurrentUser()
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
