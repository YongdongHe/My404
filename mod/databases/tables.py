#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, VARCHAR,ForeignKey, Float 
from sqlalchemy.orm import relationship,backref
from db import engine,Base

class Article(Base):
	__tablename__ = 'articles'
	article_id = Column(Integer,primary_key = True)
	user_id = Column(Integer)
	user_name = Column(VARCHAR(20))
	title = Column(VARCHAR(40))
	time = Column(VARCHAR(20))
	content = Column(VARCHAR(2000))

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

		
class Comment(Base):
	__tablename__ = 'comments'
	comment_id = Column(Integer,primary_key=True)
	article_id = Column(Integer)
	comment_content = Column(String)
	commenter_id = Column(Integer)
	commenter_name = Column(String)
	comment_time = Column(VARCHAR)
	

	


