#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.databases.tables import Article
from mod.Auth.SessionHelper import SessionHelper
from mod.BaseHandler import BaseHandler
import tornado.web
import tornado.gen
import urllib
import time

reload(sys)   
sys.setdefaultencoding('utf8')

class ArticleWriteHandler(BaseHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        #page for write article
        sessionhelper = SessionHelper(self,self.db)
        correct_user = sessionhelper.checkSession()
        if correct_user==None:
            self.render("homepage/login.html",correct_user=correct_user)
        else:
            self.render("articlewrite.html",correct_user=correct_user)

    def post(self):
        # new article
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
                article = Article(
                    user_id = correct_user.user_id,
                    user_name = username,
                    title = article_title,
                    content = article_content,
                    time = posttime)
                self.db.add(article)
                self.db.commit()
                response["status"]=200
                response["data"]='success'
                self.write(response)
            except Exception, e:
                response["status"]=400
                response["data"]=str(e)
                self.db.rollback()
                self.write(response)
        else:
            self.render("homepage/login.html",correct_user=None)
