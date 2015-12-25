from tornado.httpclient import HTTPRequest, AsyncHTTPClient,HTTPError
import tornado.web
import tornado.gen
from mod.databases.tables import Xkkey


class SeuxkHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    @tornado.gen.coroutine
    def get(self):
        key = str(self.get_secure_cookie("seuxkkey"))
        enble = self.db.query(Xkkey).filter(Xkkey.key == key).first()
        if enble != None:
            self.render("seuxk.js")
        else:
            self.render("seuxkerror.js")

class SeuxkKeyHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    @tornado.gen.coroutine
    def get(self):
        key  = self.get_argument("key")
        self.set_secure_cookie("seuxkkey",key)
        self.write("Set key as %s succcessfully."%(key))
