# -*- coding: utf-8 -*-


from CrossService.Common import Define
from CrossService.Common.Define import logger
from CrossService.Common.Results import DATABASEACTIONRESULT, DBActionResult
from CrossService.Common import Utils
from CrossService.Scripts import DBConnector



class DBConnecterManager(object):
	"""
	数据库连接管理器
	"""
	_instance = None
	def __init__(self):
		self._dbConnecters = {}
	
	@staticmethod
	def instance():
		if not DBConnecterManager._instance:
			DBConnecterManager._instance = DBConnecterManager()
		return DBConnecterManager._instance
		
	def getDBConnector(self, serverkey, serverInfo):
		"""
		获取数据库连接器实例
		"""
		connector = None
		if serverkey in self._dbConnecters:
			connector = self._dbConnecters[serverkey]
		else:
			connector = DBConnector.DBConnector(**serverInfo)
			self._dbConnecters[serverkey] = connector
		return connector

class DBConnectInterface:
	"""
	数据库操作接口
	"""
	_instance = None
	def __init__(self):
		"""
		"""
		self._configs = {}
		self.initData(Define.SERVER_CONFIG_PATH)
	
	@staticmethod
	def instance():
		if not DBConnectInterface._instance:
			DBConnectInterface._instance = DBConnectInterface()
		return DBConnectInterface._instance
		
	def initData(self, configPath):
		self._configs = Utils.loadJsonDataByFile(configPath)
		
	def getDBConnector(self, serverkey):
		if serverkey not in self._configs:
			logger.error("DBConnectInterface error: serverkey('%s') not in config" % serverkey)
			return None
		return DBConnecterManager.instance().getDBConnector(serverkey, self._configs[serverkey]["dbInfo"])
		
	def queryRecord(self, serverkey, sql):
		"""
		根据SQL语句获取游戏数据库的信息
		"""
		executeResult = DBActionResult()
		connector = self.getDBConnector(serverkey)
		if not connector:
			executeResult.setResult(DATABASEACTIONRESULT.FAIL)
			return executeResult
		return connector.select(sql)
		
	def updateRecord(self, serverkey, sql, param = []):
		"""
		根据SQL语句对游戏数据库进行操作
		"""
		executeResult = DBActionResult()
		connector = self.getDBConnector(serverkey)
		if not connector:
			executeResult.setResult(DATABASEACTIONRESULT.FAIL)
			return executeResult
			
		return connector.execute(sql, param)

g_dbInterfaceInst = DBConnectInterface.instance()