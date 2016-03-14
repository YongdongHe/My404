#coding=utf8
from tornado.httpclient import HTTPRequest, AsyncHTTPClient,HTTPError
import tornado.web
import tornado.gen
import os
from mod.BaseHandler import BaseHandler
from mod.databases.tables import User,Oauthkey,Oauthtoken,Session
class OauthHandler(tornado):
	@property
	def db(self):
		return self.application.db

	@tornado.gen.coroutine
	def get(self,url):
		if url == 'authorize_page':
			#发送client_id和redirect_url
			self.doAuthorize()

		@tornado.gen.coroutine
	def post(self,url):
		if url == 'get_code':
			#获取auth_code
			self.doGetCode()
		elif url == 'get_token':
			self.doGetToken()
		elif url == 'refresh_accesstoken':
			self.doRefreshToken()



	def doAuthorize(self):
		#返回授权页面

		

	def doGetCode(self):
		response = {code : '',content : ''}
		#检查是否由授权页面发送
		#获取用户名密码进行验证
		app_key = self.get_argument("app_key")
		redirect_url = self.get_argument("redirect_url",default="")
		account = self.get_argument("account")
		psd = self.get_argument("password")
		try:
			#检查app_key
			oauthkey = self.db.query(Oauthkey).fitler(Oauthkey.app_key == app_key).first()
			if oauthkey == None:
				response['code'] = 403
				respense['content'] = 'Wrong APP KEY.'
				self.write(response)
				return
			#检查用户名密码是否正确
			user = self.db.query(User).filter(User.user_email == account,User.user_psd == psd).first()
			if user == None:
				response['code'] = 403
				respense['content'] = 'Please check whether the usernames and passwords match.'
				self.write(response)
				return
			elif:
				#如果正确则附加code参数重定向到用户指定的url
				#查找该appkey下用户对应的token
				oauthtoken = self.db.query(Oauthtoken).filter(Oauthtoken.user_id == user.user_id).first()
				if oauthtoken == None:
					#如果没有则新建一个
					oauthtoken = Oauthtoken(
						access_token = self.getRandomToken(),
						refresh_token = self.getRandomToken(),
						auth_code = self.getRandomToken(),
						app_key = app_key,
						user_id = user.user_id
						)
					self.db.add(new_oauthtoken)
					self.db.commit()
				#如果有的话则更新code并且返回
				oauthtoken.code = self.getRandomToken()
				self.db.commit()
				self.redirect("http://"+redirect_url+"?code=%s"%(oauthtoken.code))
		except Exception as e:
			print str(e)
			self.db.rollback()

	def doGetToken(self):
		response = {code : '',content : ''}
		app_key = self.get_argument('app_key')
		auth_code = self.get_argument('code')
		try:
			#检查app_key和auth_code是否对应正确
			oauthtoken = self.db.query(Oauthtoken).filter(
				Oauthtoken.app_key == app_key,
				Oauthtoken.auth_code == auth_code
				).first()
			if oauthtoken == None:
				#如果没有则说明错误
				response['code'] = 403
				respense['content'] = 'Invalid auth code.'
				self.write(response)
				return
			#如果有的话则返回accesstoken和refreshtoken
			response['code'] = 200
			response['content'] = {}
			response['content']['access_token'] = oauthtoken.access_token
			response['content']['refresh_token'] = oauthtoken.refresh_token 
			self.write(response)
		except Exception as e:
			print str(e)
			self.db.rollback()

	def doRefreshToken(self):
		#刷新access_token
		response = {code : '',content : ''}
		app_key = self.get_argument('app_key')
		refresh_token = self.get_argument('refresh_token')
		try:
			#检查app_key和auth_code是否对应正确
			oauthtoken = self.db.query(Oauthtoken).filter(
				Oauthtoken.app_key == app_key,
				Oauthtoken.refresh_token == refresh_token
				).first()
			if oauthtoken == None:
				#如果没有则说明错误
				response['code'] = 403
				respense['content'] = 'Invalid refresh_token.'
				self.write(response)
				return
			#如果有的话则返回刷新后的accesstoken
			#刷新
			oauthtoken.access_token = self.getRandomToken()
			self.db.commit()
			response['code'] = 200
			response['content'] = {}
			response['content']['access_token'] = oauthtoken.access_token
			self.write(response)
		except Exception as e:
			print str(e)
			self.db.rollback()

	def getRandomToken(self):
		return ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(16)))