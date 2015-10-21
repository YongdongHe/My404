from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.databases.tables import User
from mod.Debug.Col import Color
import re
import tornado.web
import tornado.gen
import urllib


class RegisterHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def post(self):
        debugPrint = Color()
        debugPrint.print_green_text("DebugMsgIn%s"%('RegisterHandler'))
        try:
            helper = RegisterHelper(self.db,
                self.get_argument("email"),
                self.get_argument("name"),
                self.get_argument("psd"),
                self.get_argument("confpsd"))
            if helper.CheckEmail():
                print "valid email"
        except RegisterError, e:
            print e.getErrorMsg()


#Check register msg
class RegisterHelper(object):
    """docstring for RegisterHelper"""
    def __init__(self,db,email,name,psd,confpsd):
        super(RegisterHelper, self).__init__()
        self.db = db
        self.email = str(email)
        self.name = str(name)
        self.psd = str(psd)
        self.confpsd = str(psd)

    def CheckEmail(self):
        if len(self.email) < 7:
            raise RegisterError("Length of email must be greater than or equal to 7",304);
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", self.email) == None:
            raise RegisterError("Invalid email address",304)
        user = self.db.query(User).filter(User.user_email == self.email).first()
        print user.user_name
        return True


#possibly error      
class RegisterError(RuntimeError):
    def __init__(self, msg,code):
        self.msg = str(msg)
        self.code = int(code)
    def getErrorCode(self):
        return self.code
    def getErrorMsg(self):
        return self.msg

        