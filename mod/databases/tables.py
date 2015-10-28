#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, VARCHAR,ForeignKey, Float 
from sqlalchemy.orm import relationship,backref
from db import engine,Base

class Article(Base):
	__tablename__ = 'articles'
	article_id = Column(Integer,primary_key = True)
	user_id = Column(Integer)
	user = Column(VARCHAR(20))
	title = Column(VARCHAR(40))
	time = Column(VARCHAR(20))
	content = Column(VARCHAR(2000))

class User(Base):
	__tablename__ = 'users'
	user_id = Column(Integer,primary_key = True)
	user_email = Column(String)
	user_name = Column(String)
	user_psd = Column(String)

class Session(Base):
	__tablename__ = 'sessions'
	session_id = Column(Integer,primary_key=True)
	session_value = Column(String)
	user_id = Column(Integer)

		

	

	


