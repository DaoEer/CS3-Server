# -*- coding: utf-8 -*-

from common import DBConnector,SQLConfig
from common import csstatus
from common import csdefine
from collections import OrderedDict

CS3DBConfigPath = "config/CS3DBConfig.ini"
CS3DBGameName = "GameDatabase"
CS3DBLogName = "LogDataBase"

class DBConnectManager(object):
	"""
	数据库连接管理器
	"""
	def __init__(self, config):
		"""
		"""
		self.config = config
		self.gameDBConnector = DBConnector.DBConnector(**config["gameDatabaseInfo"])
		self.logDBConnector = DBConnector.DBConnector(**config["logDatabaseInfo"])
		
	def getGameDBConnector(self):
		"""
		获取游戏数据库连接器实例
		"""
		if not self.gameDBConnector:
			self.gameDBConnector = DBConnector.DBConnector(**self.config["gameDatabaseInfo"])
		return self.gameDBConnector
		
	def getLogDBConnector(self):
		"""
		获取日志数据库连接器实例
		"""
		if not self.logDBConnector:
			self.logDBConnector = DBConnector.DBConnector(**self.config["logDataBaseInfo"])
		return self.logDBConnector


class DBConnectInterface:
	"""
	数据库操作接口
	"""
	_instance = None
	def __init__(self):
		"""
		"""
		self.configs = OrderedDict()
		self.dbConnectorMgrs = {}
	
	@staticmethod
	def instance():
		if not DBConnectInterface._instance:
			DBConnectInterface._instance = DBConnectInterface()
		return DBConnectInterface._instance
		
	def initConfig(self, configs):
		self.configs = configs
		
	def onServerChange(self, key):
		"""
		服务器改变，修改数据库连接
		"""
		if self.getDBConnectorMgr(key):
			return True
		else:
			return False
		
	def getDBConnectorMgr(self, key):
		"""
		获取对应的DBConnectorMgr
		"""
		if key in self.dbConnectorMgrs:
			return self.dbConnectorMgrs[key]
		else:
			dbConnectorMgr = DBConnectManager(self.configs[key])
			self.dbConnectorMgrs[key] = dbConnectorMgr
			return dbConnectorMgr
		
	def getGameInfoBySql(self, key, sql):
		"""
		根据SQL语句获取游戏数据库的信息
		"""
		connector = self.getDBConnectorMgr(key).getGameDBConnector()
		results = connector.select(sql)
		return results
		
	def getLogInfoBySql(self, key, sql):
		"""
		根据SQL语句获取日志数据库的信息
		"""
		connector = self.getDBConnectorMgr(key).getLogDBConnector()
		results = connector.select(sql)
		return results

	def executeSqlInGameDB(self, key, sql, param):
		"""
		根据SQL语句对游戏数据库进行操作
		"""
		connector = self.getDBConnectorMgr(key).getGameDBConnector()
		connector.execute(sql,param)

	#-----------------------------------------check-------------------------------------------
	def checkAccount(self, key, accountName):
		"""
		检查账号是否存在
		"""
		sql = """select accountName from kbe_accountinfos where accountName = '%s'"""
		results = self.getGameInfoBySql(key, sql % accountName)
		return len(results) > 0
		
	def checkRole(self, key, roleName):
		"""
		检查角色是否存在
		"""
		sql = """select sm_playerName from tbl_Role where sm_playerName = '%s'"""
		results = self.getGameInfoBySql(key, sql % roleName)
		return len(results) > 0
		
	#-----------------------------------------query-------------------------------------------
	def queryAccountInfo(self, key, queryType, queryText):
		"""
		获取账号信息
		"""
		connector = self.getDBConnectorMgr(key).getGameDBConnector()
		sql = "select entityDBID, accountName, regtime, lasttime, numlogin from kbe_accountinfos where " + "%s = '%s'" % (queryType, queryText)
		results = connector.select(sql)
		message = {}
		if len(results) == 0:
			message["empty_data"] = True
			message["datas"] = {}
			return message
		else:
			message["empty_data"] = False
		datas = []
		for data in results:
			tempData = []
			for d in data:
				tempData.append(d)
			datas.append(tempData)
		message["datas"] = datas
		return message

	def exportAllRoleInfo(self, key):
		"""
		获取以便导出所有角色信息
		"""
		rechargeInfo_sql = "select accountName, value from %s" % (SQLConfig.LOG_TYPE_RECHARGE)
		log_connector = self.getDBConnectorMgr(key).getLogDBConnector()
		rechargeInfo_result=log_connector.select(rechargeInfo_sql)
		rechargeInfo=[]
		for data in rechargeInfo_result:
			rechargeInfo.append(list([d for d in data]))
		connector = self.getDBConnectorMgr(key).getGameDBConnector()
		sql = "SELECT kbe_accountinfos.accountName, tbl_Role.sm_playerName, tbl_Role.sm_gender, tbl_Role.sm_level, tbl_Role.sm_camp, tbl_Role.sm_profession, tbl_Role.sm_xiuwei, \
			tbl_Role.sm_killingValue, tbl_Role.sm_potential, tbl_Role.sm_money, tbl_Role.sm_lingshi, tbl_Account.sm_xianshi, tbl_Account.sm_xuanshi, tbl_Role.sm_createTime, \
			tbl_Role.sm_offlineTime, tbl_Role.sm_lifetime FROM tbl_Role, kbe_accountinfos, tbl_Account where tbl_Role.sm_parentDBID = kbe_accountinfos.entityDBID \
			AND tbl_Role.sm_parentDBID = tbl_Account.id"
		results = connector.select(sql)
		datas = []
		for data in results:
			datas.append(list([d for d in data]))
		for data in datas:
			recharge_value=0
			data.append(recharge_value)
			for value in rechargeInfo:
				if data[0]==value[0]:
					data[16]+=value[1]
		message = {"datas": datas}
		return message


g_dbInterfaceInst = DBConnectInterface.instance()