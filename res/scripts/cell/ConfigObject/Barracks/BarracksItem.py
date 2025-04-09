# -*- coding: utf-8 -*-

import KBEngine
#common
import KBEDebug
import csdefine
import ConfigObject.Barracks.BarracksObjectCondition as BarracksObjectCondition

class BarracksItem:
	def __init__( self ):
		self.id = 0							# 兵ID
		self.scriptID = ""					# 兵的scriptID
		self.soldierName = ""				# 兵的名字
		self.soldierType = csdefine.BARRACKS_SOLDIER_COMMON_TYPE				# 兵类型
		self.maxHaveAmount = 0				# 兵拥有最大数量
		self.armyMaxAmount = 0 				# 部队拥有的最大数量
		self.maxUpLevel = 0					# 兵的最高等级
		self.costMoney = 0					# 花费的金钱
		self.unLockConditions =None			# 解锁的条件
		self.unLockLevelConditions ={}		# 解锁等级的条件
		self.commonSkillIDs = []			# 普通技能
		self.commandSkillID = 0				# 指挥技能	

	def init( self, data ):
		"""
		"""
		self.id = int(data["Name"])
		self.scriptID = data["ScriptID"]
		self.soldierName = data["SoldierName"]
		self.soldierType = getattr( csdefine, data["SoldierType"], csdefine.BARRACKS_SOLDIER_COMMON_TYPE )
		self.maxUpLevel = data["MaxUpLevel"]
		self.maxHaveAmount = data["MaxHaveAmount"]
		self.armyMaxAmount = data["ArmyMaxAmount"]		
		self.costMoney = data["CostMoney"]
		self.commonSkillIDs = data.get("CommonSkillIDs",[])
		self.commandSkillID = data["CommandSkillID"]
		if self.unLockConditions == None:
			self.unLockConditions = BarracksObjectCondition.BarracksObjectCondition()

		self.unLockConditions.init( data["UnLockConditions"] )

		for unLockLevelData in data["UnLockLevelConditions"]:
			self.unLockLevelConditions[unLockLevelData["TargetLevel"]] = BarracksObjectCondition.BarracksObjectCondition()
			self.unLockLevelConditions[unLockLevelData["TargetLevel"]].init( unLockLevelData["Conditions"] )

	def getBarracksItemDict( self ):
		"""
		获得兵种的数据
		"""
		data = { 
			"id":self.id,
			"scriptID":self.scriptID,
			"soldierType":self.soldierType,
			"maxHaveAmount":self.maxHaveAmount,
			"armyMaxAmount":self.armyMaxAmount,
			"maxUpLevel":self.maxUpLevel,
			"costMoney":self.costMoney
		}
		return data

	def checkBarracksItemIsUnLock( self, role ):
		"""
		检查兵是否已解锁
		"""
		return self.unLockConditions.valid( role )

	def checkBarracksItemLevelIsUnLock( self, role, level ):
		"""
		检查兵等级是否已解锁
		"""
		if level in self.unLockLevelConditions:
			return self.unLockLevelConditions[level].valid( role )
		return True

	def getMaxHaveAmount( self ):
		"""
		获得最大拥有数量
		"""
		return self.maxHaveAmount

	def getCostMoney( self ):
		"""
		获得消耗的金钱
		"""
		return self.costMoney

	def getArmyMaxAmount( self ):
		"""
		获得部队拥有的最大数量
		"""
		return self.armyMaxAmount

	def getMaxUpLevel( self ):
		"""
		获得兵升的最大等级
		"""
		return self.maxUpLevel
