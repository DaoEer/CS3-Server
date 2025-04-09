# -*- coding:utf-8 -*-

import KBEngine
from KBEDebug import *
import LoadModule
import csdefine
import imp
from EquipPropertyParse import g_EquipPropertyLoadInst

class TitleLoader:
	"""
	称号配置加载器
	"""
	_instance = None
	
	def __init__( self ):
		assert TitleLoader._instance is None
		self._datas = {}
		path = "TitleData/titleData.json"
		self.loadData(path)
	
	@staticmethod
	def instance():
		if TitleLoader._instance is None:
			TitleLoader._instance = TitleLoader()
		return TitleLoader._instance


	def loadData( self, pathUrl ):
		jsFileObj = LoadModule.openJsonCfg( pathUrl )
		for data in jsFileObj:
			self._datas[ data["TitleID"] ] = data
			#-1.0 表示 永久 不限时
			data["LimitTime"] = float(data["LimitTime"].strip())*24*60*60         #天数转换成秒数
			if data["LimitTime"]  == 0:
				self._datas[data["TitleID"]]["LimitTime"] = -1.0


	def getAllData(self):
		"""
		"""
		return self._datas
		

	def getData( self, titleID ):
		"""
		根据titleID获得数据
		
		@param titleID:  称号ID
		@return: [( id, prestige ), ...]
		"""
		try:
			return self._datas[ titleID ]
		except KeyError:
			ERROR_MSG( "Title %s has no data." % ( titleID ) )
			return None		


	def isTimeLimit( self, titleID ):
		"""
		称号是否有时间限制
		
		rtype : BOOL
		"""
		try:
			time = self._datas[ titleID ][ "LimitTime" ]
			return time > 0
		except KeyError:
			ERROR_MSG( "title %s is not exist." % ( titleID ) )
			return False


	def getHoldEffectIDs( self, titleID ):
		"""
		获取持有效果列表
		"""
		if titleID == csdefine.TITLE_NONE:
			return []
		titleData = self.getData(titleID)
		if not titleData:
			return []
		holdEffectIDs =[]
		param1 = titleData.get("HoldEffectID","").strip()
		if param1 == "":
			return []
		holdEffectIDs = [int(ID) for ID in param1.split("|")]
		return holdEffectIDs


	def getAttackPropertiesStr(self,titleID):
		"""
		获取基础属性
		"""
		if titleID == csdefine.TITLE_NONE:
			return {}
		titleData = self.getData(titleID)
		if not titleData:
			return {}
		param2 = titleData.get("PropertyID",None)
		if param2 != "":
			param2 = int(param2)
		attackProperties = g_EquipPropertyLoadInst.getDataByID(param2)
		return attackProperties

	def reloadConfig(self):
		for id,e in KBEngine.entities.items():					#热更新前，取消掉持续效果
			if e.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				e.oldCombatPower = e.combatPower
				e.removeTitleHoldEffects()

		self._datas = {}
		path = "TitleData/titleData.json"
		self.loadData(path)

		for id,e in KBEngine.entities.items():					#热更新前，取消掉持续效果
			if e.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				e.addTitleHoldEffects()
				e.calcAttachProperties(csdefine.CALC_COMBAT_POWER_REASON_TITLE)
				e.onCombatPowerChange(e.oldCombatPower, csdefine.CALC_COMBAT_POWER_REASON_TITLE)

g_titleLoader = TitleLoader.instance()


from TitleData import titleRewardData

class TitleRewardLoader:
	"""
	称号奖励配置加载器
	"""
	_instance = None
	
	def __init__( self ):
		assert TitleRewardLoader._instance is None
		self._datas = titleRewardData.datas
	
	@staticmethod
	def instance():
		if TitleRewardLoader._instance is None:
			TitleRewardLoader._instance = TitleRewardLoader()
		return TitleRewardLoader._instance

	def getAllData(self):
		"""
		"""
		return self._datas

	def reloadConfig(self):
		imp.reload(titleRewardData)
		self._datas = titleRewardData.datas


g_titleRewardLoader = TitleRewardLoader.instance()


