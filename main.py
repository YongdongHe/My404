# from mod.testapi.handler import testHandler
#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os.path
import random
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import time
# from mod.testapi.handler import testHandler
from sqlalchemy.orm import scoped_session, sessionmaker
from mod.databases.db import engine
from mod.databases.tables import Session
from mod.RootHandler.RootHandler import HomePageHandler
from mod.RootHandler.RootHandler import IndexHandler
from mod.RootHandler.RootHandler import IndexPageHandler
from mod.ArticleHandler.ArticleHandler import ArticleHandler
from mod.ArticleHandler.ArticleWriteHandler import ArticleWriteHandler
from mod.ArticleHandler.ArticleHandler import ArticleContentModule
from mod.BlogHandler.BlogHandler import BlogHandler
from mod.Auth.RegisterHandler import RegisterHandler
from mod.Auth.LoginHandler import LoginHandler
from mod.Auth.LogoutHandler import LogoutHandler
from mod.MessageHandler.MessageHandler import MessageBoxHandler
from mod.testapi.handler import TestHandler
from mod.testapi.handler import TestapiHandler
from mod.Api.BusHandler import BusHandler
from mod.Api.SeuxkHandler import SeuxkHandler
from mod.Api.SeuxkHandler import SeuxkKeyHandler
from mod.DownloadHandler.DownloadHandler import DownloadFileHandler
from tornado.options import define, options


define("port", default=3000, help="run on the given port", type=int)

# def main():
#     tornado.options.parse_command_line()
#     application = tornado.web.Application(
        
#         static_path=os.path.join(os.path.dirname(__file__),"static"),
#         template_path=os.path.join(os.path.dirname(__file__), "templates")
#         )
#     http_server = tornado.httpserver.HTTPServer(application)
#     http_server.listen(options.port)
#     tornado.ioloop.IOLoop.instance().start()
#     self.db = scoped_session(sessionmaker(bind=engine,
#                                               autocommit=False, autoflush=True,
#                                               expire_on_commit=False))


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
        (r"/", IndexHandler),
        (r"/404",IndexPageHandler),
        (r"/home/(\w+)",HomePageHandler),
        (r"/register",RegisterHandler),
        (r"/login",LoginHandler),
        (r"/logout",LogoutHandler),
        (r"/article",ArticleHandler),
        (r"/articlewrite",ArticleWriteHandler),
        (r"/blog",BlogHandler),
        (r"/msg",MessageBoxHandler),
        (r"/test",TestapiHandler),
        (r"/api/bus",BusHandler),
        (r"/api/seuxk",SeuxkHandler),
        (r"/api/seuxk/getkey",SeuxkKeyHandler),
        (r"/download",DownloadFileHandler),
        (r"/tieba",GetIpHandler)]
        modules={'ArticleContent': ArticleContentModule}
        settings = dict(
            debug=True,
            static_path=os.path.join(os.path.dirname(__file__),"static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            cookie_secret="365B3932BBBA6182B2D899B494468874",
            ui_modules=modules
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=engine,
                                              autocommit=False, autoflush=True,
                                              expire_on_commit=False))
        self.filepath=os.path.join(os.path.dirname(__file__),'files')


class GetIpHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    def get(self):
        try:
            create_time = time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
            real_ip = str(self.request.headers.get("x-real-ip", "default-ip"))
            data_session = Session(session_value = '007',user_id = '007',create_time=create_time,user_ip=real_ip)
            self.db.add(data_session)
            self.db.commit()
        except Exception as e:
            print str(e)
            self.db.rollback()
        self.redirect("http://tieba.baidu.com/home/main/?un=S%E9%97%AA%E9%97%AA%E6%83%B9%E4%BA%BA%E7%88%B1S&ie=utf-8&fr=frs")

if __name__ == '__main__':
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
