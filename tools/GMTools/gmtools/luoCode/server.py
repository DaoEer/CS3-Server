# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist

from . import login
from ..models import GMUser
from common import csstatus
from common import csdefine
from common import tooldefine
from common.baseConnector import g_baseappConnector

loginInstannce = login.g_loginInstance

class ServerManager:
	"""
	服务器管理
	"""
	_instance = None
	def __init__(self):
		pass
	
	@staticmethod
	def instance():
		if ServerManager._instance == None:
			ServerManager._instance = ServerManager()
		return ServerManager._instance
		
	@loginInstannce.login_check
	def server_change(self, request):
		"""
		修改base服务器
		"""
		context = {"error":""}
		html_template = "gmtools/index.html"
		try:
			changeServer = request.GET.get(tooldefine.CURR_SERVER)
			if not g_baseappConnector.onServerChange(changeServer):
				context["error"] = csstatus.CHANGE_SERVER_FAILED %request.serverInfos[changeServer]
				return render(request, html_template, context)
			request.session[tooldefine.CURR_SERVER] = changeServer
		except Exception as err:
			#print("change server error: %s" % err)
			context["error"] = csstatus.CHANGE_SERVER_FAILED %request.serverInfos[changeServer]
		#return HttpResponseRedirect("/gmtools/index")
		return render(request, html_template, context)

g_serverInstance = ServerManager.instance()