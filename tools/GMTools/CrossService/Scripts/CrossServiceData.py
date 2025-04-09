# -*- coding: utf-8 -*-

from django.http import HttpResponse

import time
import traceback

from CrossService.Common import Define
from CrossService.Common.Results import  DATABASEACTIONRESULT, DBActionResult, CROSSSERVICECODE
from CrossService.Scripts.DBConnectInterface import g_dbInterfaceInst
from CrossService.Scripts.CrossFieldsInfo import g_CSFieldInfoInst

class DataBaseActionInfo:
	def __init__(self, sql = "", data = []):
		self._sql = sql
		self._data = data
	
	def setSql(self, sql):
		self._sql = sql
	
	def setData(self, data):
		self._data = data
	
	def getSql(self):
		return self._sql
		
	def getData(self):
		return self._data


class CrossServiceData:
	"""
	跨服数据
	"""
	_instance = None
	def __init__(self):
		pass
		
	@staticmethod
	def instance():
		"""
		"""
		if CrossServiceData._instance == None:
			CrossServiceData._instance = CrossServiceData()
		return CrossServiceData._instance
		
	def isCrossServicePlayer(self, serverkey, roleName):
		"""
		判断是否是跨服的账号
		"""
		sql = self.getQuerySqlInfo(Define.TABLE_NAME_ROLE, [Define.CROSS_LOGON_FIELD_KEY_NAME_ROLE], "sm_playerName", roleName)
		queryResult = self.query(serverkey, sql)
		if queryResult.getResult() == DATABASEACTIONRESULT.FAIL:
			return False
		data = queryResult.getData()
		if len(data) < 0 or (len(data) > 0 and int(data[0][0]) == 0):
			return False
			
		return True
		
	def getQuerySqlInfo(self, tableName, fieldList, fieldkey, fieldkeyValue):
		fieldStr = ""
		for field in fieldList:
			fieldStr += "`%s`, " % field
		sql = ""
		if len(fieldStr) > 0:
			sql = "select %s from %s where `%s` = '%s'" % (fieldStr[0:-2], tableName, fieldkey, fieldkeyValue)
		return sql
		
	def getUpdateSql(self, tableName, fieldList, fieldkey, fieldkeyValue, data):
		updateFields = ""
		for field in fieldList:
			updateFields += "`%s` = " % field
			updateFields += "%s, "
		sql = "update %s set " % tableName + updateFields[0:-2] + " where `%s` = '%s'" % (fieldkey, fieldkeyValue)
		
		DBActionInfo = DataBaseActionInfo(sql, data)
		return DBActionInfo
		
	def getInsertSql(self, tableName, generalFields, specialFields, fieldkeyTypeInfo, data):
		tempData = data.copy()
		fieldsStr = ("`%s`, " * len(generalFields)) % tuple(generalFields)
		for specialField in specialFields:
			fieldsStr += "`%s`, " % specialField["name"]
			tempData.append(fieldkeyTypeInfo[int(specialField["type"])])
		dataStr = ("%s, " * (len(generalFields) + len(specialFields)))[0:-2]
		sql = "insert into %s(%s) values(" % (tableName, fieldsStr[0:-2]) + dataStr + ")"
		DBActionInfo = DataBaseActionInfo(sql, tempData)
		return DBActionInfo
		
	def getDeleteSql(self, tableName,fieldkey, fieldkeyValue):
		sql = "Delete from %s where `%s` = '%s'" % (tableName, fieldkey, fieldkeyValue)
		return sql
		
	def getDeleteSqlForMultTables(self, tableInfos, parentTableName, parentID):
		sql = "select "
		tableStr = ""
		conditionStr = ""
		for info in tableInfos:
			tableName = info["tablename"]
			tableStr += "%s, " % tableName
			conditionStr += "%s.parentID = %s.id, " % (tableName, parentTableName)
			parentTableName = tableName
		
	def getPlayerInfo(self, serverkey, account, role):
		"""
		获取玩家信息
		return: {0: account name, 1: account dbid, 2: role name, 3: role dbid}
		"""
		#暂时不考虑重名的问题
		queryResult = DataBaseActionInfo()
		playerInfo = {}
		playerInfo[Define.DB_FIELD_KEY_TYPE_ACCOUNT_NAME] = account
		playerInfo[Define.DB_FIELD_KEY_TYPE_ACCOUNT_DBID] = Define.PLAYER_DEFAULT_VALUE
		playerInfo[Define.DB_FIELD_KEY_TYPE_ROLE_NAME] = role
		playerInfo[Define.DB_FIELD_KEY_TYPE_ROLE_DBID] = Define.PLAYER_DEFAULT_VALUE
		
		#账号
		queryResult = self.queryAccount(serverkey, account)
		if queryResult.getResult() == DATABASEACTIONRESULT.FAIL:
			Define.logger.error("CrossServiceData.getPlayerInfo: query account info error: serverkey(%s), account(%s)" % (serverkey, account))
			queryResult.setResult(DATABASEACTIONRESULT.FAIL)
			return queryResult
		accountInfo = queryResult.getData()
		if len(accountInfo) > 0 and len(accountInfo[0]) > 0:
			playerInfo[Define.DB_FIELD_KEY_TYPE_ACCOUNT_DBID] = int(accountInfo[0][0])
		else:
			#账号不存在，不需要再查下角色，直接返回
			queryResult.setResult(DATABASEACTIONRESULT.SUCCESS)
			queryResult.setData(playerInfo)
			return queryResult
		
		#角色
		queryResult = self.queryRole(serverkey, account, role)
		if queryResult.getResult() == DATABASEACTIONRESULT.FAIL:
			Define.logger.error("CrossServiceData.getPlayerInfo: query role info error: serverkey(%s), account(%s), role(%s)" % (serverkey, account, role))
			queryResult.setResult(DATABASEACTIONRESULT.FAIL)
			return queryResult
			
		roleInfo = queryResult.getData()
		if len(roleInfo) > 0 and len(roleInfo[0]) > 0:
			playerInfo[Define.DB_FIELD_KEY_TYPE_ROLE_DBID] = int(roleInfo[0][0])
		
		queryResult.setResult(DATABASEACTIONRESULT.SUCCESS)
		queryResult.setData(playerInfo)
		return queryResult
		
	def checkRecord(self, serverkey, tableName, fieldkey, fieldkeyValue):
		sql = "select %s from %s where %s = '%s'" % (fieldkey, tableName, fieldkey, fieldkeyValue)
		return self.query(serverkey, sql)
		
	def insertAccount(self, serverkey, account):
		sql = "insert into %s(sm_playerName) values('%s')" % (Define.TABLE_NAME_ACCOUNT, account)
		return self.execute(serverkey, sql)
		
	def insertRole(self, serverkey, role, accountDBID):
		sql = "insert into %s(sm_playerName, sm_parentDBID) values('%s', %s)" % (Define.TABLE_NAME_ROLE, role, accountDBID)
		return self.execute(serverkey, sql)
		
	def execute(self, serverkey, sql, data = []):
		executeResult = g_dbInterfaceInst.updateRecord(serverkey, sql, data)
		return executeResult
		
	def query(self, serverkey, sql):
		queryResult = g_dbInterfaceInst.queryRecord(serverkey, sql)
		return queryResult
		
	def queryAccount(self, serverkey, account):
		"""
		查询账号信息
		"""
		sql = "select id from %s where sm_playerName = '%s'" % (Define.TABLE_NAME_ACCOUNT, account)
		return g_dbInterfaceInst.queryRecord(serverkey, sql)
		
	def queryRole(self, serverkey, account, role):
		"""
		查询玩家信息
		"""
		sql = "select %s.id from %s, %s where %s.sm_playerName = '%s' and %s.sm_playerName = '%s' and %s.id = %s.sm_parentDBID" \
			% (Define.TABLE_NAME_ROLE, Define.TABLE_NAME_ACCOUNT, Define.TABLE_NAME_ROLE, Define.TABLE_NAME_ACCOUNT, account, 
			Define.TABLE_NAME_ROLE, role, Define.TABLE_NAME_ACCOUNT, Define.TABLE_NAME_ROLE)
		
		return g_dbInterfaceInst.queryRecord(serverkey, sql)
		
	def queryData(self, serverkey, tableName, fieldList, fieldkey, fieldkeyValue):
		"""
		"""
		queryResult = DBActionResult()
		sql = self.getQuerySqlInfo(tableName, fieldList, fieldkey, fieldkeyValue)
		if len(sql) > 0:
			queryResult = self.query(serverkey, sql)
			if queryResult.getResult() == DATABASEACTIONRESULT.FAIL:
				return queryResult
		else:
			queryResult.setResult(DATABASEACTIONRESULT.SUCCESS)
		return queryResult
		
	def deleteData(self, serverkey, tableName, fieldkey, fieldkeyValue):
		sql = self.getDeleteSql(tableName,fieldkey, fieldkeyValue)
		return self.execute(serverkey, sql)
		
	def updateChildTableData(self, prevServerkey, followedServerkey, childTables, prevServerParentDBID, followedServerParentDBID, prevServerSpecialInfo, followedServerSpecialInfo):
		"""
		"""
		executeResult = DBActionResult()
		for table in childTables:
			fieldList = table["fields"]["general"].copy()
			fieldList.insert(0, Define.CHILD_TABLE_DBID_FIELD_NAME) #需要把当前服务器的数据的dbid也查询出来
			queryResult = self.queryData(prevServerkey, table["tablename"], fieldList, Define.PARENT_TABLE_DBID_FIELD_NAME, prevServerParentDBID)
			if queryResult.getResult() == DATABASEACTIONRESULT.FAIL:
				return queryResult
			srcServerData = queryResult.getData()
			if len(srcServerData) > 0:
				#如果当前服务器存在数据，则更新
				tempFields = [Define.CHILD_TABLE_DBID_FIELD_NAME]
				queryResult = self.queryData(followedServerkey, table["tablename"], tempFields, Define.PARENT_TABLE_DBID_FIELD_NAME, followedServerParentDBID)
				if queryResult.getResult() == DATABASEACTIONRESULT.FAIL:
					return queryResult
				dstServerData = queryResult.getData()
				srcDataLen = len(srcServerData)
				dstDataLen = len(dstServerData)
				updateLen = min(srcDataLen, dstDataLen)
				tempIDList = []
				for i in range(updateLen):
					DBActionInfo = self.getUpdateSql(table["tablename"], table["fields"]["general"], Define.CHILD_TABLE_DBID_FIELD_NAME, int(dstServerData[i][0]), srcServerData[i][1:])
					executeResult = self.execute(followedServerkey, DBActionInfo.getSql(), DBActionInfo.getData())
					if executeResult.getResult() == DATABASEACTIONRESULT.FAIL:
						return executeResult
					executeResult = self.updateChildTableData(prevServerkey, followedServerkey, table["childtables"], int(srcServerData[i][0]), int(dstServerData[i][0]), prevServerSpecialInfo, followedServerSpecialInfo)
					if executeResult.getResult() == DATABASEACTIONRESULT.FAIL:
						return executeResult
					tempIDList.append(int(dstServerData[i][0]))
					
				if srcDataLen > dstDataLen:#当前服务器的数据比目标服务器的数据行数多，更新目标服务器现有数据，再插入新数据
					for i in range(srcDataLen - dstDataLen):
						specialFields = [{"name": Define.PARENT_TABLE_DBID_FIELD_NAME, "type": Define.DB_FIELD_KEY_TYPE_PARENT_DBID}]
						specialFields.extend(table["fields"]["special"])
						fieldkeyTypeInfo = {Define.DB_FIELD_KEY_TYPE_PARENT_DBID: followedServerParentDBID}
						fieldkeyTypeInfo.update(followedServerSpecialInfo)
						
						DBActionInfo = self.getInsertSql(table["tablename"], table["fields"]["general"], specialFields, fieldkeyTypeInfo, srcServerData[dstDataLen + i][1:])
						executeResult = self.execute(followedServerkey, DBActionInfo.getSql(), DBActionInfo.getData())
						if executeResult.getResult() == DATABASEACTIONRESULT.FAIL:
							return executeResult
						#执行完成后，再查找该数据的dbid
						queryResult = self.queryData(followedServerkey, table["tablename"], tempFields, Define.PARENT_TABLE_DBID_FIELD_NAME, followedServerParentDBID)
						if queryResult.getResult() == DATABASEACTIONRESULT.FAIL:
							return queryResult
						tempList = [int(data[0]) for data in queryResult.getData()]
						newID = max(tempList)
						if newID in tempIDList:
							Define.logger.error("CrossServiceData.updateChildTableData: check new data dbid error")
							queryResult.setResult(DATABASEACTIONRESULT.FAIL)
							return queryResult
						executeResult = self.updateChildTableData(prevServerkey, followedServerkey, table["childtables"], srcServerData[dstDataLen + i][0], newID, prevServerSpecialInfo, followedServerSpecialInfo)
						if executeResult.getResult() == DATABASEACTIONRESULT.FAIL:
							return executeResult
						tempIDList.append(newID)
				else:#当前服务器的数据比目标服务器的数据行数少，则需要删除多余的行数
					for data in dstServerData:
						if int(data[0]) not in tempIDList:
							sql = self.getDeleteSql(table["tablename"], Define.CHILD_TABLE_DBID_FIELD_NAME, int(data[0]))
							executeResult = self.execute(followedServerkey, sql, [])
							if executeResult.getResult() == DATABASEACTIONRESULT.FAIL:
								return executeResult
			else:
				#如果当前服务器不存在数据，则删除目标服务器的数据
				sql = self.getDeleteSql(table["tablename"], Define.PARENT_TABLE_DBID_FIELD_NAME, followedServerParentDBID)
				self.execute(followedServerkey, sql, [])
		executeResult.setResult(DATABASEACTIONRESULT.SUCCESS)
		return executeResult
		
	def syncData(self, srcServerkey, dstServerkey, srcServerPlayerInfo, dstServerPlayerInfo, fieldsInfo):
		"""
		"""
		executeResult = DBActionResult()
		
		#仅支持父表是tbl_Role或tbl_Account
		if fieldsInfo["keytype"] == Define.DB_FIELD_KEY_TYPE_ACCOUNT_DBID or fieldsInfo["keytype"] == Define.DB_FIELD_KEY_TYPE_ACCOUNT_NAME:
			srcServerParentDBID = srcServerPlayerInfo[Define.DB_FIELD_KEY_TYPE_ACCOUNT_DBID]
			dstServerParentDBID = dstServerPlayerInfo[Define.DB_FIELD_KEY_TYPE_ACCOUNT_DBID]
		elif fieldsInfo["keytype"] == Define.DB_FIELD_KEY_TYPE_ROLE_DBID or fieldsInfo["keytype"] == Define.DB_FIELD_KEY_TYPE_ROLE_NAME:
			srcServerParentDBID = srcServerPlayerInfo[Define.DB_FIELD_KEY_TYPE_ROLE_DBID]
			dstServerParentDBID = dstServerPlayerInfo[Define.DB_FIELD_KEY_TYPE_ROLE_DBID]
		else:
			Define.logger.error("CrossServiceData.syncData: table(%s) keytype(%s) config is error" % (fieldsInfo["tablename"], fieldsInfo["keytype"]))
			executeResult.setResult(DATABASEACTIONRESULT.FAIL)
			return executeResult
			
		queryResult = self.queryData(srcServerkey, fieldsInfo["tablename"], fieldsInfo["fields"]["general"], fieldsInfo["fieldkey"], srcServerPlayerInfo[fieldsInfo["keytype"]])
		if queryResult.getResult() == DATABASEACTIONRESULT.FAIL:
			return queryResult
		data = queryResult.getData()
		
		if len(data) >0:
			checkResult = self.checkRecord(dstServerkey, fieldsInfo["tablename"], fieldsInfo["fieldkey"], dstServerPlayerInfo[fieldsInfo["keytype"]])
			if checkResult.getResult() == DATABASEACTIONRESULT.FAIL:
				return checkResult
			if len(checkResult.getData()) > 0:
				DBActionInfo = self.getUpdateSql(fieldsInfo["tablename"], fieldsInfo["fields"]["general"], fieldsInfo["fieldkey"], dstServerPlayerInfo[fieldsInfo["keytype"]], data[0])
			else:
				DBActionInfo = self.getInsertSql(fieldsInfo["tablename"], fieldsInfo["fields"]["general"], fieldsInfo["fields"]["special"], dstServerPlayerInfo, data[0])
			executeResult = self.execute(dstServerkey, DBActionInfo.getSql(), DBActionInfo.getData())
			if executeResult.getResult() == DATABASEACTIONRESULT.FAIL:
				return executeResult
				
			return self.updateChildTableData(srcServerkey, dstServerkey, fieldsInfo["childtables"], srcServerParentDBID, dstServerParentDBID, srcServerPlayerInfo, dstServerPlayerInfo)
		else:
			Define.logger.warning("CrossServiceData.syncData: serverkey(%s) table(%s) account(%s) role(%s) data is empty" % (srcServerkey, fieldsInfo["tablename"], 
				srcServerPlayerInfo[Define.DB_FIELD_KEY_TYPE_ACCOUNT_NAME], srcServerPlayerInfo[Define.DB_FIELD_KEY_TYPE_ROLE_NAME]))
			return queryResult
			
	def deleteChildTableRecord(self, serverkey, tableInfos, parentID):
		"""
		"""
		executeResult = DBActionResult()
		for info in tableInfos:
			tableName = info["tablename"]
			if len(info["childtables"]) > 0:
				queryResult = self.queryData(serverkey, tableName, [Define.CHILD_TABLE_DBID_FIELD_NAME], Define.PARENT_TABLE_DBID_FIELD_NAME, parentID)
				if queryResult.getResult() == DATABASEACTIONRESULT.FAIL:
					return queryResult
				for data in queryResult.getData():
					id = int(data[0])
					self.deleteChildTableRecord(serverkey, info["childtables"], id)
			executeResult = self.deleteData(serverkey, tableName, Define.PARENT_TABLE_DBID_FIELD_NAME, parentID)
			if executeResult.getResult() == DATABASEACTIONRESULT.FAIL:
				return executeResult
					
		executeResult.setResult(DATABASEACTIONRESULT.SUCCESS)
		return executeResult
		
	def deleteServerRecord(self, serverkey, tableInfos, playerInfo):
		"""
		删除服务器的指定数据
		"""
		executeResult = DBActionResult()
		for info in tableInfos:
			if info["keytype"] == Define.DB_FIELD_KEY_TYPE_ACCOUNT_DBID or info["keytype"] == Define.DB_FIELD_KEY_TYPE_ACCOUNT_NAME:
				parentID = playerInfo[Define.DB_FIELD_KEY_TYPE_ACCOUNT_DBID]
			elif info["keytype"] == Define.DB_FIELD_KEY_TYPE_ROLE_DBID or info["keytype"] == Define.DB_FIELD_KEY_TYPE_ROLE_NAME:
				parentID = playerInfo[Define.DB_FIELD_KEY_TYPE_ROLE_DBID]
			else:
				Define.logger.error("CrossServiceData.deleteServerRecord: table(%s) keytype(%s) config is error" % (info["tablename"], info["keytype"]))
				executeResult.setResult(DATABASEACTIONRESULT.FAIL)
				return executeResult
				
			executeResult = self.deleteChildTableRecord(serverkey, info["childtables"], parentID)
			if executeResult.getResult() == DATABASEACTIONRESULT.FAIL:
				return executeResult
				
			executeResult = self.deleteData(serverkey, info["tablename"], info["fieldkey"], playerInfo[info["keytype"]])
			if executeResult.getResult() == DATABASEACTIONRESULT.FAIL:
				return executeResult
				
		executeResult.setResult(DATABASEACTIONRESULT.SUCCESS)
		return executeResult
		
	def updateAccountLastLogonDBID(self, serverkey, account, value):
		"""
		更新Account表的lastLogonDBID字段，否则删除最后登录角色后，再次登录时角色选择界面不正常
		"""
		DBActionInfo = self.getUpdateSql(Define.TABLE_NAME_ACCOUNT, [Define.ACCOUNT_LAST_LOGON_DBID_NAME], Define.ACCOUNT_NAME_FIELD_NAME, 
			account, [value])
		return self.execute(serverkey, DBActionInfo.getSql(), DBActionInfo.getData())
		
	def updateAccountData(self, serverkey, playerInfo):
		"""
		更新账号信息
		"""
		accountName = playerInfo[Define.DB_FIELD_KEY_TYPE_ACCOUNT_NAME]
		
		executeResult = self.insertAccount(serverkey, accountName)
		if executeResult.getResult() == DATABASEACTIONRESULT.FAIL:
			return executeResult
		queryAccountResult = self.queryAccount(serverkey, accountName)
		if queryAccountResult.getResult() == DATABASEACTIONRESULT.FAIL:
			return queryAccountResult
		accountData = queryAccountResult.getData()
		if len(accountData) < 0 or len(accountData[0]) < 0:
			Define.logger.error("CrossServiceData.updateAccountData error: can not find account dbid for serverkey(%s), account(%s)" % (serverkey, accountName))
			executeResult.setResult(DATABASEACTIONRESULT.FAIL)
			return executeResult
			
		playerInfo[Define.DB_FIELD_KEY_TYPE_ACCOUNT_DBID] = int(accountData[0][0])
		
		executeResult.setResult(DATABASEACTIONRESULT.SUCCESS)
		return executeResult
		
	def updateRoleData(self, serverkey, playerInfo):
		"""
		更新角色信息
		"""
		accountName = playerInfo[Define.DB_FIELD_KEY_TYPE_ACCOUNT_NAME]
		accountDBID = playerInfo[Define.DB_FIELD_KEY_TYPE_ACCOUNT_DBID]
		roleName = playerInfo[Define.DB_FIELD_KEY_TYPE_ROLE_NAME]
		
		if accountDBID== Define.PLAYER_DEFAULT_VALUE:
			Define.logger.error("CrossServiceData.updateRoleData error: account dbid error for serverkey(%s), account(%s)" % (serverkey, accountName))
			executeResult = DATABASEACTIONRESULT()
			return executeResult
		
		executeResult = self.insertRole(serverkey, roleName, accountDBID)
		if executeResult.getResult() == DATABASEACTIONRESULT.FAIL:
			return executeResult
			
		queryRoleResult = self.queryRole(serverkey, accountName, roleName)
		if queryRoleResult.getResult() == DATABASEACTIONRESULT.FAIL:
			return queryRoleResult
		roleData = queryRoleResult.getData()
		if len(roleData) < 0 or len(roleData[0]) < 0:
			Define.logger.error("CrossServiceData.updateRoleData error: can not find role dbid for serverkey(%s), account(%s), role(%s)" % (serverkey, accountName, roleName))
			executeResult.setResult(DATABASEACTIONRESULT.FAIL)
			return executeResult
			
		playerInfo[Define.DB_FIELD_KEY_TYPE_ROLE_DBID] = int(roleData[0][0])
		
		executeResult.setResult(DATABASEACTIONRESULT.SUCCESS)
		return executeResult
		
	def updateDefaultData(self, serverkey, fieldkeyTypeInfo):
		"""
		更新指定默认数据的字段
		"""
		executeResult = DBActionResult()
		
		for data in g_CSFieldInfoInst.getDefaultDataConfig():
			DBActionInfo = self.getUpdateSql(data["tablename"], data["fields"], data["fieldkey"], fieldkeyTypeInfo[data["keytype"]], data["data"])
			executeResult = self.execute(serverkey, DBActionInfo.getSql(), DBActionInfo.getData())
			if executeResult.getResult() == DATABASEACTIONRESULT.FAIL:
				return executeResult
		
		executeResult.setResult(DATABASEACTIONRESULT.SUCCESS)
		return executeResult
		
	def updateCrossServiceData(self, prevServerkey, followedServerkey, account, role):
		"""
		更新跨服需要同步的数据信息到数据库
		@param prevServerkey: 跨服前的服务器key
		@param followedServerkey: 跨服后的服务器key
		"""
		executeResult = DBActionResult()
		
		queryResult =self.getPlayerInfo(followedServerkey, account, role)
		if queryResult.getResult() == DATABASEACTIONRESULT.FAIL:
			return queryResult
		followedServerPlayerInfo =queryResult.getData()
		#如果账号不存在，需要先写入账号和角色信息
		if followedServerPlayerInfo[Define.DB_FIELD_KEY_TYPE_ACCOUNT_DBID] == Define.PLAYER_DEFAULT_VALUE:
			executeResult = self.updateAccountData(followedServerkey, followedServerPlayerInfo)
			if executeResult.getResult() == DATABASEACTIONRESULT.FAIL:
				return executeResult
			executeResult = self.updateRoleData(followedServerkey, followedServerPlayerInfo)
			if executeResult.getResult() == DATABASEACTIONRESULT.FAIL:
				return executeResult
		elif followedServerPlayerInfo[Define.DB_FIELD_KEY_TYPE_ROLE_DBID] == Define.PLAYER_DEFAULT_VALUE:
			#账号已存在，角色不存在的情况
			executeResult = self.updateRoleData(followedServerkey, followedServerPlayerInfo)
			if executeResult.getResult() == DATABASEACTIONRESULT.FAIL:
				return executeResult
				
		queryResult =self.getPlayerInfo(prevServerkey, account, role)
		if queryResult.getResult() == DATABASEACTIONRESULT.FAIL:
			return queryResult
		prevServerPlayerInfo =queryResult.getData()
		
		for info in g_CSFieldInfoInst.getSyncFieldsInfo():
			executeResult = self.syncData(prevServerkey, followedServerkey, prevServerPlayerInfo, followedServerPlayerInfo, info)
			if executeResult.getResult() == DATABASEACTIONRESULT.FAIL:
				return executeResult
				
		executeResult = self.updateDefaultData(followedServerkey, followedServerPlayerInfo)
		if executeResult.getResult() == DATABASEACTIONRESULT.FAIL:
			return executeResult
			
		#将账号的最后登录角色dbid改成同步过去的玩家的dbid
		return self.updateAccountLastLogonDBID(followedServerkey, account, followedServerPlayerInfo[Define.DB_FIELD_KEY_TYPE_ROLE_DBID])
		
	def updateReturnServerData(self, prevServerkey, followedServerkey, account, role):
		"""
		更新跨服完成后返回原服务器的需要同步的数据信息到数据库
		@param prevServerkey: 跨服前的服务器key
		@param followedServerkey: 跨服后的服务器key
		"""
		executeResult = DBActionResult()
		
		queryResult =self.getPlayerInfo(followedServerkey, account, role)
		if queryResult.getResult() == DATABASEACTIONRESULT.FAIL:
			return queryResult
		followedServerPlayerInfo =queryResult.getData()
		
		#如果账号不存在则返回错误
		if followedServerPlayerInfo[Define.DB_FIELD_KEY_TYPE_ACCOUNT_DBID] == Define.PLAYER_DEFAULT_VALUE or followedServerPlayerInfo[Define.DB_FIELD_KEY_TYPE_ROLE_DBID] == Define.PLAYER_DEFAULT_VALUE:
			executeResult.setResult(DATABASEACTIONRESULT.FAIL)
			executeResult.setCode(CROSSSERVICECODE.CROSS_SERVICE_OLD_PLAYER_INFO_ERROR)
			return executeResult
		
		queryResult =self.getPlayerInfo(prevServerkey, account, role)
		if queryResult.getResult() == DATABASEACTIONRESULT.FAIL:
			return queryResult
		prevServerPlayerInfo =queryResult.getData()
		
		#同步数据到原服务器
		for info in g_CSFieldInfoInst.getSyncFieldsInfo():
			executeResult = self.syncData(followedServerkey, prevServerkey, followedServerPlayerInfo, prevServerPlayerInfo, info)
			if executeResult.getResult() == DATABASEACTIONRESULT.FAIL:
				return executeResult
		
		executeResult.setResult(DATABASEACTIONRESULT.SUCCESS)
		return executeResult
		
	def onReturnServerFinished(self, prevServerkey, followedServerkey, account, role):
		"""
		返回原服务器完成
		@param prevServerkey: 跨服前的服务器key
		@param followedServerkey: 跨服后的服务器key
		"""
		executeResult = DataBaseActionInfo()
		if not self.isCrossServicePlayer(followedServerkey, role):
			executeResult.setResult(DATABASEACTIONRESULT.FAIL)
			executeResult.setCode(CROSSSERVICECODE.CROSS_SERVICE_NOT_CROSS_SERVER_PLAY)
			return executeResult
			
		queryResult =self.getPlayerInfo(followedServerkey, account, role)
		if queryResult.getResult() == DATABASEACTIONRESULT.FAIL:
			return queryResult
		playerInfo =queryResult.getData()
		
		executeResult = self.deleteServerRecord(followedServerkey, g_CSFieldInfoInst.getDeleteTableInfos(), playerInfo)
		if executeResult.getResult == DATABASEACTIONRESULT.FAIL:
			return executeResult
		return self.updateAccountLastLogonDBID(followedServerkey, account, Define.ACCOUNT_LAST_LOGON_DBID_DEFAULE_VALUE)
		
g_CSDataInst = CrossServiceData.instance()