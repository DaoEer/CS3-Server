# -*- coding: utf-8 -*-

import KBEDebug
from Singleton import Singleton

class SpaceCopyYXLMMonsterDataLoader( Singleton ):
	"""
	副本-—— 英雄联盟怪数据加载类
	"""
	def __init__( self ):
		Singleton.__init__( self )
		self.monsterDatas = {}   #{ scriptID:{level:{"maxExp":100,"expRewardToKiller":100}} }

	def init( self, monsterConfigDatas ):
		"""
		读取配置
		"""
		self.monsterDatas.clear()
		for scriptID, monsterConfigData in monsterConfigDatas.items():
			self.monsterDatas[scriptID] = {}
			for level, monsterData in monsterConfigData.items():
				self.monsterDatas[scriptID][int(level)] = monsterData

	def getMonsterLevelData( self, monsterScriptID, level ):
		"""
		获得配置数据
		"""
		monsterDatas = self.monsterDatas.get( monsterScriptID,None )
		if not monsterDatas:
			KBEDebug.ERROR_MSG("SpaceCopyYXLMMonsterData.json has not this monster(%s)"%monsterScriptID)
			return None
		monsterLevelData = monsterDatas.get(level,None)
		if not monsterLevelData:
			KBEDebug.ERROR_MSG("SpaceCopyYXLMMonsterData.json has not this level(%i)"%level)
			return None
		return monsterLevelData

	def getMonsterMaxExpByLevel( self, monsterScriptID, level ):
		"""
		通过等级获得最大经验
		"""
		monsterLevelData = self.getMonsterLevelData( monsterScriptID, level )
		if not monsterLevelData:
			return None
		return monsterLevelData["maxExp"]

	def getMonsterRewardJadeToKillerPlayer( self, monsterScriptID, level ):
		"""
		直接击杀怪物 获得奖励魂玉
		"""
		monsterLevelData = self.getMonsterLevelData( monsterScriptID, level )
		if not monsterLevelData:
			return 0
		return monsterLevelData.get("rewardJadeToKillerPlayer",0)

	def getMonsterRewardJadeToAssistPlayer( self, monsterScriptID, level ):
		"""
		获得助攻奖励的魂玉
		"""
		monsterLevelData = self.getMonsterLevelData( monsterScriptID, level )
		if not monsterLevelData:
			return 0
		return monsterLevelData.get("rewardJadeToAssistPlayer",0)

	def getMonsterExpRewardToKillerPlayer( self, monsterScriptID, level ):
		"""
		怪物被玩家直接击杀 获得经验奖励
		"""
		monsterLevelData = self.getMonsterLevelData( monsterScriptID, level )
		if not monsterLevelData:
			return 0
		return monsterLevelData.get("expRewardToKillerPlayer",0)

	def getMonsterExpRewardToKillerMonster( self, monsterScriptID, level ):
		"""
		怪物被怪物直接击杀 获得经验奖励
		"""
		monsterLevelData = self.getMonsterLevelData( monsterScriptID, level )
		if not monsterLevelData:
			return 0
		return monsterLevelData.get("expRewardToKillerMonster",0)

	def getMonsterExpRewardToAssistPlayer( self, monsterScriptID, level ):
		"""
		周围玩家获得经验奖励
		"""
		monsterLevelData = self.getMonsterLevelData( monsterScriptID, level )
		if not monsterLevelData:
			return 0
		return monsterLevelData.get("expRewardToAssistPlayer",0)

	def getMonsterExpRewardToAssistMonster( self, monsterScriptID, level ):
		"""
		周围怪物获得经验奖励
		"""
		monsterLevelData = self.getMonsterLevelData( monsterScriptID, level )
		if not monsterLevelData:
			return 0
		return monsterLevelData.get("expRewardToAssistMonster",0)

	
g_spaceCopyYXLMMonsterDataLoader = SpaceCopyYXLMMonsterDataLoader()