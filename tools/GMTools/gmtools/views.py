# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

from .luoCode import login
from . import models
from common import csdefine, tooldefine

import hashlib

loginInstannce = login.g_loginInstance

def createAdministrator():
	"""
	创建admin用户
	"""
	#为了预防开始没有账号登录，而导致无法进行其他操作，在创建admin账号
	#本来是想在__init__.py文件中创建的，但是在__init__.py文件中importmodels会报错，也不知道怎么解决，所以在这里添加了
	try:#在这里使用try,是因为在初始化数据库时（makemigrations、migrate）会加载本模块（views)，就会调用此方法，但是那时候数据库还不存在，所以会出错
		srvConf = tooldefine.tool_default_db_key
		users = models.GMUser.objects.using(srvConf)
		userIDList = [ user.userID.lower() for user in users ]

		userID = "admin"
		userName = "Administrator"
		password = "123456"

		if len(userIDList) == 0:
			r = models.GMUser.objects.using(srvConf).create(
				userID= userID,
				userName = userName,
				password= hashlib.md5(password.encode("utf-8")).hexdigest(),
				level = tooldefine.USER_LEVEL_ONE
			)
	except:
		pass

createAdministrator()

class Index:
	_instance = None
	def __init__(self):
		pass
		
	@staticmethod
	def instance():
		if Index._instance == None:
			Index._instance = Index()
		return Index._instance
			
	@loginInstannce.login_check
	def index( self, request ):
		context = {"error":""}
		html_template = "gmtools/index.html"
		return render( request, html_template, context)
		
g_IndexInstance = Index.instance()