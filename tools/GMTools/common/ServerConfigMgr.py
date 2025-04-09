# -*- coding: utf-8 -*-

from collections import OrderedDict

from common import Functions

class ServerConfigMgr:
	_instance = None
	def __init__(self):
		self._config = Functions.loadServerConfig()
	
	@staticmethod
	def instance():
		if ServerConfigMgr._instance == None:
			ServerConfigMgr._instance = ServerConfigMgr()
		return ServerConfigMgr._instance
	
	def getConfig(self):
		self._config = Functions.loadServerConfig()
		return self._config
		

g_srvCfgMgrInstance = ServerConfigMgr.instance()