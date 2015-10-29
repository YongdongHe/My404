from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.databases.tables import User
from mod.databases.tables import Session
import uuid
import time
# from mod.Debug.Col import Color
import re
import tornado.web
import tornado.gen
import urllib

class LoginHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def post(self):
        # debugPrint = Color()
        # debugPrint.print_green_text("DebugMsgIn%s"%('RegisterHandler'))
        email = self.get_argument("email")
        psd = self.get_argument("psd")
        # debugPrint.print_green_text("DebugMsgIn%s:%s"%('RegisterHandler',email))
        # debugPrint.print_green_text("DebugMsgIn%s:%s"%('RegisterHandler',name))
        # debugPrint.print_green_text("DebugMsgIn%s:%s"%('RegisterHandler',psd))
        # debugPrint.print_green_text("DebugMsgIn%s:%s"%('RegisterHandler',confpsd))
        data={}
        try:
            helper = LoginHelper(self.db,email,psd)
            correct_user = helper.Check()
            if  correct_user != None:
            	data["status"] = 200
                data["data"] = "Login Success"
                uuid_session = str(uuid.uuid4())
                create_time = time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
                data_session = Session(session_value = uuid_session,user_id = correct_user.user_id,create_time=create_time)
                self.db.add(data_session)
                self.db.commit()
                self.set_secure_cookie("session",uuid_session)
                print str(correct_user.user_id)
                self.set_secure_cookie("userid",str(correct_user.user_id))
                self.write(data)
        except LoginError, e:            
            data["status"] = e.getErrorCode()
            data["data"] = e.getErrorMsg()
            # debugPrint.print_green_text("DebugMsgIn%s:%s%s"%('RegisterHandler',"Register failed",e.getErrorMsg()))
            self.write(data)

#Check register msg
class LoginHelper(object):
    """docstring for LoginHelper"""
    def __init__(self,db,email,psd):
        super(LoginHelper, self).__init__()
        self.db = db
        self.email = str(email)
        self.psd = str(psd)

    def Check(self):
        if len(self.email) < 7:
            raise LoginError("Length of email must be greater than or equal to 7",400);
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", self.email) == None:
            raise LoginError("Invalid Email Address",400)
        user = self.db.query(User).filter(User.user_email == self.email).first()
        if user==None:
            raise LoginError("Unexisted Email Address",404)
        elif user.user_psd == self.psd: 
            return user
        else:
        	raise LoginError("Wrong password for this email",403)
        return None



    def CheckSafe(self,str):
        safaChars = ["\'","+",">","=","\""]
        for it in safaChars:
            if(str.find(it)!=-1):
                return False
        return True


#possibly error      
class LoginError(RuntimeError):
    def __init__(self, msg,code):
        self.msg = str(msg)
        self.code = int(code)
    def getErrorCode(self):
        return self.code
    def getErrorMsg(self):
        return self.msg