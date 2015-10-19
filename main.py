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
# from mod.testapi.handler import testHandler
from sqlalchemy.orm import scoped_session, sessionmaker
from mod.databases.db import engine
from mod.testapi.handler import DbHandler
from mod.ArticleHandler.ArticleHandler import ArticleHandler
from mod.UserhomeHandler.UserhomeHandler import UserhomeHandler
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


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('home.html')


class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('homepage/index.html')

class HomePageHandler(tornado.web.RequestHandler):
    def get(self,args):
        print args[0::]
        self.render('homepage/%s.html'%(args[0::]))


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
        (r"/", IndexHandler),
        (r"/404",IndexPageHandler),
        (r"/home/(\w+)",HomePageHandler),
        (r"/db",DbHandler),
        (r"/article",ArticleHandler),
        (r"/userhome",UserhomeHandler)
        ]
        settings = dict(
            debug=True,
            static_path=os.path.join(os.path.dirname(__file__),"static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates")
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=engine,
                                              autocommit=False, autoflush=True,
                                              expire_on_commit=False))

if __name__ == '__main__':
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
