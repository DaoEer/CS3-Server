# -*- coding: utf-8 -*-


from CrossService.Common import Define
from CrossService.Common import Utils


class CrossFieldsInfo:
	_instance = None
	def __init__(self):
		self._syncFieldsInfo = []
		self._defaultDataConfig = []
		self._deleteTableInfos = []
		self.initData(Define.CROSS_FIELDS_CONFIG_PATH)
		
	@staticmethod
	def instance():
		if CrossFieldsInfo._instance == None:
			CrossFieldsInfo._instance = CrossFieldsInfo()
			
		return CrossFieldsInfo._instance
		
	def checkPlayerTableConfig(self, tableName, fields):
		if tableName in Define.FIELDS_CONFIG_FORBID_DICT:
			#某些字段禁止同步，比如tbl_Role表的sm_parentDBID，该字段在目标服务器的数据库中可能不一样
			for field in Define.FIELDS_CONFIG_FORBID_DICT[tableName]:
				if field in fields:
					Define.logger.error("CrossFieldsInfo.checkPlayerTableConfig: config fields error for table(%s)" % tableName)
					return False
		return True
		
	def checkChildTableConfig(self, childTables):
		for table in childTables:
			if Define.PARENT_TABLE_DBID_FIELD_NAME in table["fields"]:
				Define.logger.error("CrossFieldsInfo.checkChildTableConfig: config fields error for childtable(%s) " % table["tablename"])
				return False
			result = self.checkChildTableConfig(table["childtables"])
			if not result:
				return False
		return True
		
	def initData(self, configPath):
		datas = Utils.loadJsonDataByFile(configPath)
		for data in datas.get("SyncFieldsInfo", []):
			if not self.checkPlayerTableConfig(data["tablename"], data["fields"]["general"]) or not self.checkChildTableConfig(data["childtables"]):
				self._syncFieldsInfo = []
				self._defaultDataConfig = []
				return
			fieldsData = {"tablename": data["tablename"], "fieldkey": data["fieldkey"], "keytype": int(data["keytype"]), "fields": data["fields"], "childtables": data["childtables"]}
			self._syncFieldsInfo.append(fieldsData)
			
		for data in datas.get("DefaultInfo", []):
			if not self.checkPlayerTableConfig(data["tablename"], data["fields"]):
				self._syncFieldsInfo = []
				self._defaultDataConfig = []
				return
			if len(data["data"]) != len(data["fields"]):
				Define.logger.error("CrossFieldsInfo.initData check DefaultInfo: config data and fields len error for childtable(%s) " % data["tablename"])
				self._syncFieldsInfo = []
				self._defaultDataConfig = []
				return
			tempdata = {"tablename": data["tablename"], "fieldkey": data["fieldkey"], "keytype": int(data["keytype"]), "fields": data["fields"], "data": data["data"]}
			self._defaultDataConfig.append(tempdata)
			
		for data in datas.get("DeleteTableInfos", []):
			data["keytype"] = int(data["keytype"])
			self._deleteTableInfos.append(data)
		
	def getSyncFieldsInfo(self):
		return self._syncFieldsInfo
		
	def getDefaultDataConfig(self):
		return self._defaultDataConfig
		
	def getDeleteTableInfos(self):
		return self._deleteTableInfos


g_CSFieldInfoInst = CrossFieldsInfo.instance()