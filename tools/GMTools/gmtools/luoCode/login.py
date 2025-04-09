# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from common import csdefine
from common import tooldefine
from common import Functions
from common.baseConnector import g_baseappConnector
from common.DBConnectInterface import g_dbInterfaceInst
from common.ServerConfigMgr import g_srvCfgMgrInstance
from cs3_web_services import settings
from ..models import GMUser
from collections import OrderedDict

import functools, hashlib


GMUserQuerySet = GMUser.objects.using(tooldefine.tool_default_db_key)

# Create your views here.

class LoginManager():
	"""
	登录器
	"""
	_instance = None
	def __init__(self):
		self.configs = OrderedDict()
	
	@staticmethod
	def instance():
		if not LoginManager._instance:
			LoginManager._instance = LoginManager()
		return LoginManager._instance
	
	def initServerConfig(self, request):
		self.configs = g_srvCfgMgrInstance.getConfig()
		g_baseappConnector.initConfig(self.configs)
		g_dbInterfaceInst.initConfig(self.configs)
	
	def setRequestDefaultInfo(self, request):
		"""
		设置request默认信息以及填充ServerInfos
		"""
		self.setRequestServerInfo(request)
		if not request.session.get(tooldefine.CURR_SERVER, None):
			self.setDefaultServer(request)
	
	def setDefaultServer(self, request):
		defaultServer = Functions.getDefaultServer()
		if defaultServer in request.serverInfos:
			request.session[tooldefine.CURR_SERVER] = defaultServer
		else:
			request.session[tooldefine.CURR_SERVER] = list(request.serverInfos.keys())[0]
		
	def login_check(self, func):
		"""
		检查是否已登录
		"""
		@functools.wraps( func )
		def wrapper(classObj, request, *arg, **kws ):
			#把服务器配置放到request中，以保证在各个页面使用
			if len(self.configs) == 0 or self.configs != g_srvCfgMgrInstance.getConfig():
				self.initServerConfig(request)
			self.setRequestServerInfo(request)
			if not request.session.get("logined", False):
				return HttpResponseRedirect("/gmtools/login")
			return func(classObj, request, *arg, **kws )
		return wrapper
		
	def login(self, request):
		"""
		gm账号登录页面
		"""
		#print("request.session is",request.session)
		if request.session.get( "logined", False ):
			return HttpResponseRedirect( "/gmtools/index" )

		if len(self.configs) == 0 or self.configs != g_srvCfgMgrInstance.getConfig():
			self.initServerConfig(request)
		#session可能由于客户端浏览器清空记录，导致curr_server不存在，所以登陆的地方不存在这个就设置一次
		self.setRequestDefaultInfo(request)
		
		name = request.POST.get("name", None)
		password = request.POST.get("password", None)
		curr_server = request.POST.get("server_select", None)
		context = { "next_uri" : "", "error":"" }
		
		if name is None or password is None:
			return render(request, "gmtools/login.html", context)
		
		if not name or not password:
			context["error"] = "错误：缺少用户名或密码参数"
			return render(request, "gmtools/login.html", context)
		
		m = hashlib.md5( password.encode("utf-8") )
		pwd = m.hexdigest()
		
		if not GMUserQuerySet.filter( userID = name, password = pwd ).exists():
			context["error"] = "错误：用户名不存在或密码不正确"
			return render(request, "gmtools/login.html", context)
		
		if curr_server:
			if request.session[tooldefine.CURR_SERVER] != curr_server:
				request.session[tooldefine.CURR_SERVER] = curr_server
			try:
				if not g_baseappConnector.onServerChange(curr_server):
					context["error"] = "错误：%s服务器连接不上，请检查服务器启动情况以及数据库连接情况"%request.serverInfos[curr_server]
					return render(request, "gmtools/login.html", context)
			except Exception as error:
				#print("login server error: %s" %error)
				context["error"] = "错误：%s服务器连接不上，请检查服务器启动情况以及数据库连接情况"%request.serverInfos[curr_server]
				return render(request, "gmtools/login.html", context)
		
		user = GMUser.objects.get( userID = name )
		
		request.session["logined"] = True
		request.session["gm_id"] = user.id
		request.session["gm_userid"] = user.userID
		request.session["gm_username"] = user.userName
		request.session["gm_level"] = user.level
		
		#self.setDefaultServer(request)
		return render(request,"gmtools/index.html",context)
		#return HttpResponseRedirect( "/gmtools/index" )

	def logout(self, request):
		"""
		登出
		"""
		request.session["logined"] = False
		request.session["gm_userid"] = ""
		request.session["gm_username"] = ""
		request.session["gm_level"] = 0
		request.session[tooldefine.CURR_SERVER] = ""

		return HttpResponseRedirect("/gmtools/index")
		
	def setRequestServerInfo(self, request):
		"""
		设置request的serverInfos
		"""
		if hasattr(request, "serverInfos"):
			return
		request.serverInfos = OrderedDict()
		for key, value in self.configs.items():
			request.serverInfos[key] =  value["name"]
		
g_loginInstance = LoginManager.instance()