# -*- coding: utf-8 -*-
from mod.BaseHandler import BaseHandler
from mod.databases.tables import PushMessage,SlideView,Version,AppUser
import time
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.httpserver
import tornado.options
import os

class DownloadAndroidHandler(BaseHandler):
    def get(self):
        download_path=self.application.filepath 
        filename = "heraldstudioxiaohou.apk"
        filepath=os.path.join(download_path,filename)
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename='+filename)
        buf_size = 4096
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                self.write(data)
        self.finish()

class VersionHandler(BaseHandler):
    def post(self):
        schoolnum = self.get_argument("schoolnum")
        versioncode = self.get_argument("versioncode")
        uuid = self.get_argument("uuid")
        response = {'content':'',"code":''}
        response['content'] = {}
        try:
            appuser = self.db.query(AppUser).filter(AppUser.schoolnum == schoolnum).first()
            now_time = time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
            if appuser != None :
                appuser.last_time = now_time
                appuser.login_count += 1
                self.db.commit()
            else:
                newuser = AppUser(
                    schoolnum = schoolnum,
                    uuid = uuid,
                    register_time = now_time,
                    last_time = now_time,
                    login_count = 0
                    )
                self.db.add(newuser)
                self.db.commit()
        except Exception as e:
            print str(e)
            self.db.rollback()
        #返回版本相关信息
        try:
            #版本信息返回
            last_version = self.db.query(Version).first()
            response['content']['version'] = {}
            response['content']['version']['code'] = last_version.code
            response['content']['version']['name'] = last_version.name
            response['content']['version']['des'] = last_version.des
            push_message = self.db.query(PushMessage).first()
            
            #推送消息
            response['content']['message'] = {}
            response['content']['message']['content'] = push_message.content
            response['content']['message']['url'] = push_message.url

            #图片轮播信息
            sliderviews = self.db.query(SlideView).all()
            imageurls = []
            for item in sliderviews:
                imageurls.append({
                        "title" : item.title,
                        "imageurl" : item.imageurl,
                        "url" : item.url
                    })
            response['content']['sliderviews'] = imageurls
            #code
            response['code'] = 200
            self.write(response)
        except Exception as e:
            print str(e)
            self.db.rollback()