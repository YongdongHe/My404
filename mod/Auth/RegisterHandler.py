# -*- coding: utf-8 -*-
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.BaseHandler import BaseHandler
from mod.databases.tables import User
# from mod.Debug.Col import Color
import re
import tornado.web
import tornado.gen
import urllib
import time

class RegisterHandler(BaseHandler):
    def post(self):
        # debugPrint = Color()
        # debugPrint.print_green_text("DebugMsgIn%s"%('RegisterHandler'))
        email = self.get_argument("email")
        name = self.get_argument("name")
        psd = self.get_argument("psd")
        confpsd = self.get_argument("confpsd")
        # debugPrint.print_green_text("DebugMsgIn%s:%s"%('RegisterHandler',email))
        # debugPrint.print_green_text("DebugMsgIn%s:%s"%('RegisterHandler',name))
        # debugPrint.print_green_text("DebugMsgIn%s:%s"%('RegisterHandler',psd))
        # debugPrint.print_green_text("DebugMsgIn%s:%s"%('RegisterHandler',confpsd))
        data={}
        try:
            helper = RegisterHelper(self.db,email,name,psd,confpsd)
            if helper.CheckEmail() and helper.CheckName() and helper.CheckPsd():
                register_time = time.strftime("%Y-%m-%d %X",time.localtime(time.time()))
                new_user = User(
                    user_email = email,
                    user_name = name,
                    user_psd = psd,
                    register_time = register_time)
                self.db.add(new_user)
                self.db.commit()
                #check :success or not
                user = self.db.query(User).filter(User.user_name == name).first()
                if(user.user_email == email):
                    # debugPrint.print_green_text("DebugMsgIn%s:%s"%('RegisterHandler',"Register success"))
                    self.db.commit()
                    data["status"] = 200
                    data["data"] = "Register Success"
                    self.write(data)
        except RegisterError, e:
            self.db.rollback()        
            data["status"] = e.getErrorCode()
            data["data"] = e.getErrorMsg()
            # debugPrint.print_green_text("DebugMsgIn%s:%s%s"%('RegisterHandler',"Register failed",e.getErrorMsg()))
            self.write(data)
        except Exception ,e:
            self.db.rollback()
            print "RegisterHandler:"+str(e)


#Check register msg
class RegisterHelper(object):
    """docstring for RegisterHelper"""
    def __init__(self,db,email,name,psd,confpsd):
        super(RegisterHelper, self).__init__()
        self.db = db
        self.email = str(email)
        self.name = name
        self.psd = str(psd)
        self.confpsd = str(confpsd)

    def CheckSafe(self,str):
        safaChars = ["\'","+",">","=","\""]
        for it in safaChars:
            if(str.find(it)!=-1):
                return False
        return True

    def CheckEmail(self):
        if len(self.email) < 7:
            raise RegisterError("Length of email must be greater than or equal to 7",400);
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", self.email) == None:
            raise RegisterError("Invalid Email Address",400)
        user = self.db.query(User).filter(User.user_email == self.email).first()
        if user!=None:
            raise RegisterError("Existed Email Address",403)
        return True

    def CheckName(self):
        if(not self.CheckSafe(self.name)):
            raise RegisterError("Invalid Name(Your name can only contains a-z and 0-9) ",403)
        user = self.db.query(User).filter(User.user_name == self.name).first()
        if user!=None:
            raise RegisterError("Existed Name",403)
        return True

    def CheckPsd(self):
        if(not self.CheckSafe(self.psd)):
            raise RegisterError("Invalid Password(Your password can only contants a-z and 0-9)",403)
        if(self.psd!=self.confpsd):
            raise RegisterError("Two Input Password Is Not The Same.",400)
        if(len(self.psd)>32 or len(self.psd)<8):
            raise RegisterError("Length Of Password must between 8 to 32",400)
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

        