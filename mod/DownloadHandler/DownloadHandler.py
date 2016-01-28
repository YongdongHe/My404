from mod.BaseHandler import BaseHandler
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.httpserver
import tornado.options
import os

class DownloadFileHandler(BaseHandler):
    def get(self):
        download_path=self.application.filepath 
        filename = "404helper.apk"
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
        self.write("s")
