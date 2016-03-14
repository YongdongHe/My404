#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, VARCHAR,ForeignKey, Float 
from sqlalchemy.orm import relationship,backref
from db import engine,Base

class Article(Base):
	__tablename__ = 'articles'
	article_id = Column(Integer,primary_key = True)
	user_id = Column(Integer)
	user_name = Column(String)
	title = Column(String)
	time = Column(String)
	content = Column(String)

class User(Base):
	__tablename__ = 'users'
	user_id = Column(Integer,primary_key = True)
	user_email = Column(String)
	user_name = Column(String)
	user_psd = Column(String)
	register_time = Column(VARCHAR)

class Session(Base):
	__tablename__ = 'sessions'
	session_id = Column(Integer,primary_key=True)
	session_value = Column(String)
	create_time = Column(VARCHAR)
	user_id = Column(Integer)
	user_ip = Column(String)

		
class Comment(Base):
	__tablename__ = 'comments'
	comment_id = Column(Integer,primary_key=True)
	article_id = Column(Integer)
	comment_content = Column(String)
	commenter_id = Column(Integer)
	commenter_name = Column(String)
	comment_time = Column(VARCHAR)

class Message(Base):
	__tablename__ = 'messages'
	message_id = Column(Integer,primary_key=True)
	message_type = Column(String)
	message_content = Column(String)
	user_id = Column(Integer)
	read = Column(Integer)
	
class Xkkey(Base):
	__tablename__ = 'xkkeys'
	key_id = Column(Integer,primary_key=True)
	key = Column(String)
	time = Column(Integer)

class Oauthkey(Base):
	__tablename__ = 'oauthkeys'
	key_id = Column(Integer,primary_key=True)
	app_key = Column(String)
	app_name = Column(String)

class Oauthtoken(Base):
	__tablename__ = 'oauthtokens'
	token_id = Column(Integer,primary_key=True)
	access_token = Column(String)
	refresh_token = Column(String)
	auth_code = Column(String)
	app_key = Column(String)
	user_id = Column(Integer)

class SlideView(Base):
	__tablename__ = 'slideviews'
	id = Column(Integer,primary_key=True)
	title = Column(String)
	imageurl = Column(String)
	url = Column(String)

class PushMessage(Base):
	__tablename__ = 'pushmessages'
	id = Column(Integer,primary_key=True)
	content = Column(String)
	url = Column(String)
		
class Version(Base):
	__tablename__ = 'versions'
	id = Column(Integer,primary_key=True)
	code= Column(Integer)
	des = Column(String)
	name = Column(String)
	date = Column(String)

