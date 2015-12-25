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
        try:
            key = str(self.get_cookie("seuxkkey"))
            enble = self.db.query(Xkkey).filter(Xkkey.key == key).first()
            if enble != None:
                enble.time = enble.time + 1
                self.db.commit()
                self.render("seuxk.js")
            else:
                self.render("seuxk.js")
        except Exception, e:
            print str(e)
            self.db.rollback()
            self.write("unknow error")

class SeuxkKeyHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    @tornado.gen.coroutine
    def get(self):
        key  = self.get_argument("key")
        self.clear_cookie("seuxkkey")
        self.set_cookie("seuxkkey",key)
        self.write("Set key as %s succcessfully."%(key))
