# -*- coding: utf-8 -*-

import KBEngine
#common
import Singleton
import KBEDebug
import csconst
import json
import csdefine
from LoadModule import openJsonCfg
from ConfigObject.Barracks.BarracksItem import BarracksItem
from Barracks.SoldierLevelUpCostExpCfg import Datas

def utf16ToJsonCfg( path ):
	allPath = csconst.CONFIG_PATCH + path
	fileObject = open( allPath, encoding="utf16" )
	jsFileObj = json.loads( fileObject.read() )
	fileObject.close()
	return jsFileObj

class BarracksMgr( Singleton.Singleton ):
	def __init__( self ):
		self.barracksTypeMappings  = {}
		self.soldierLevelMaxExpMap = {}
		self.gurdSoldierSkillData = {}
		self.soldierReviveCost = {}

	def init( self):
		"""
		配置更新
		"""
		barracksDatas = utf16ToJsonCfg("Barracks/BarracksData.json")
		gurdSoldierSkillDatas = utf16ToJsonCfg("Barracks/BarracksGuardSoldierSkillData.json")
		soldierReviveCost = openJsonCfg("Barracks/BarracksReviveCostDataTable.json")
		self.barracksTypeMappings.clear()
		self.gurdSoldierSkillData.clear()
		self.soldierLevelMaxExpMap = Datas
		for data in barracksDatas:
			soldierType = getattr( csdefine, data["SoldierType"], csdefine.BARRACKS_SOLDIER_COMMON_TYPE )	# 兵种类型
			if soldierType not in self.barracksTypeMappings:
				self.barracksTypeMappings[ soldierType ] = {}
			item = BarracksItem()
			item.init( data )
			self.barracksTypeMappings[soldierType][item.scriptID] = item
		for skillData in gurdSoldierSkillDatas:
			if skillData["ScriptID"] not in self.gurdSoldierSkillData:
				self.gurdSoldierSkillData[skillData["ScriptID"]] = {}
			if skillData["CurrentSkillID"] not in self.gurdSoldierSkillData[skillData["ScriptID"]]:
				self.gurdSoldierSkillData[skillData["ScriptID"]][skillData["CurrentSkillID"]] = {}
			self.gurdSoldierSkillData[skillData["ScriptID"]][skillData["CurrentSkillID"]] = skillData

		for data in soldierReviveCost:
			scriptID = data["scriptID"]
			self.soldierReviveCost[scriptID] = {}
			item = {}
			for i in data["item"]:
				level, money = i['level'], i['money']
				item[level] = money
				self.soldierReviveCost[scriptID].update(item)
		


	def getSoldierMaxExpByLevel( self, scriptID, level ):
		"""
		获得兵的最大经验
		"""
		if level in self.soldierLevelMaxExpMap and scriptID in self.soldierLevelMaxExpMap[level]:
			return self.soldierLevelMaxExpMap[level][scriptID]["maxExp"]
		return 0

	def getReviveCost(self, scriptID, level):
		"""
		获取兵种复活的费用
		"""
		if scriptID in self.soldierReviveCost and level in self.soldierReviveCost[scriptID]:
			return self.soldierReviveCost[scriptID][level]
		return -1


	def getBarracksItemByScriptID( self, soldierType, scriptID ):
		"""
		获得兵种Item
		"""
		if soldierType not in self.barracksTypeMappings:
			return None
		if scriptID not in self.barracksTypeMappings[soldierType]:
			return None
		return self.barracksTypeMappings[soldierType][scriptID]

	def getBarracksItemsBySoldierType( self, soldierType ):
		"""
		获得兵营某个类型的数据
		"""
		if soldierType in self.barracksTypeMappings:
			return list(self.barracksTypeMappings[soldierType].keys())

		return []

	def getSoldierSkillIDsByScriptID( self, scriptID):
		"""
		通过ScriptID 获得第1级的 技能ID
		"""
		if scriptID not in self.gurdSoldierSkillData:
			return []
		skillIDs = []
		skillDatas = self.gurdSoldierSkillData[scriptID]
		for skillData in skillDatas.values():
			if skillData["Level"] == 1:
				skillIDs.append( (skillData["CurrentSkillID"],skillData["ReqExp"]) )

		skillIDs = sorted(skillIDs,key = lambda i: i[0], reverse = False)

		return skillIDs

	def getSoldierNextSkillIDByScriptID( self, scriptID, skillID ):
		"""
		获得亲卫下一级的技能数据
		"""
		if scriptID not in self.gurdSoldierSkillData:
			return 0

		if skillID not in self.gurdSoldierSkillData[scriptID]:
			return 0

		return self.gurdSoldierSkillData[scriptID][skillID]["NextLevelSkillID"]

	def getSoldierSkillReqExpByScriptID( self, scriptID, skillID ):
		"""
		获得亲卫升级当前技能需要的经验值
		"""
		if scriptID not in self.gurdSoldierSkillData:
			return 0

		if skillID not in self.gurdSoldierSkillData[scriptID]:
			return 0

		return self.gurdSoldierSkillData[scriptID][skillID]["ReqExp"]


g_barracksMgr = BarracksMgr()

