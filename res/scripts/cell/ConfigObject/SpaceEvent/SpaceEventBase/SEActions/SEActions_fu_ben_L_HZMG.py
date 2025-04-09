# -*- coding: utf-8 -*-

# 副本事件行为
import random
import KBEMath
import KBEDebug
import KBEngine
import Const
import Functions
import csdefine
from ObjectScript.SpawnPoint.SpawnPointFactory import g_spawnPointFactory
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction152( SEActionBase ):
	"""
	幻阵迷宫完成全部阶段清理数据
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		KBEngine.globalData["MagicMazeSpaceManager"].deregister( spaceEntity.belongType, spaceEntity.spaceKey,spaceEntity.createArgs["mainScriptID"] )
		KBEngine.globalData["MagicMazeSpaceManager"].setSpaceExtraReward( spaceEntity.belongType, spaceEntity.spaceKey, -1, 0.0,spaceEntity.createArgs["mainScriptID"] )

class SEAction270( SEActionBase ):
	"""
	幻阵迷宫 通知显示进度界面
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for player in spaceEntity._spaceRoles:
			player.client.CLIENT_ProgressDisplayInterface()

class SEAction316( SEActionBase ):
	"""
	幻阵迷宫 进入传送门
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		belongType,spaceKey = spaceEntity.getScript().getPlayerBelongTypeAndSpaceKey(spaceEntity)
		for player in spaceEntity._spaceRoles:
			KBEngine.globalData["MagicMazeSpaceManager"].setNextLevelLoading(belongType, spaceKey, player.base, 0, 1,spaceEntity.createArgs["mainScriptID"])
			break
			
class SEAction433( SEActionBase ):
	"""
	增加循环次数,设置循环开始标记（只有从凤鸣城对话进入后的第一个地图增加次数）
	CST-11294
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		player = KBEngine.entities.get(triggerID)
		if not player or player.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		
		playerDBIDList = spaceEntity.queryTemp("playerDBID", [])
		if player.playerDBID in playerDBIDList:
			return
		
		playerDBIDList.append(player.playerDBID)
		spaceEntity.setTemp("playerDBID", playerDBIDList)
		
		if player.qianNengData.pop("Token", None):
			player.qianNengData["Loop"] = 0
		
		if player.qianNengData.get("LoopFlag", True):
			loop = player.qianNengData.get("Loop", 0)
			player.qianNengData["Loop"] = loop + 1
		
		player.qianNengData["Index"] = 0
		player.qianNengData["LoopFlag"] = False
		
		#本轮胜利通关的副本次数
		player.qianNengData["WinTimes"] = 0 
		
class SEAction434( SEActionBase ):
	"""
	完成一次循环，设置循环结束标记
	CST-11294
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		
		for player in spaceEntity._spaceRoles:
			player.qianNengData["LoopFlag"] = True
		
class SEAction435( SEActionBase ):
	"""
	增加副本序号，设置副本开始标记（事务截图中所谓的第一个玩法、第二个玩法……）
	CST-11294
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		
	def do( self, spaceEntity, triggerID, eventParams ):
		player = KBEngine.entities.get(triggerID)
		if not player or player.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
			
		if player.qianNengData.get("IndexFlag", True):
			index = player.qianNengData.get("Index", 0)
			player.qianNengData["Index"] = index + 1
		player.qianNengData["IndexFlag"] = False
		
class SEAction436( SEActionBase ):
	"""
	副本完成，主要用于标记某一副本序号的副本完成过了（失败/成功都算）
	CST-11294
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.flag = int(section["param1"])
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		
		for player in spaceEntity._spaceRoles:
			player.qianNengData["IndexFlag"] = True
			if self.flag: 
				winTimes = player.qianNengData.get("WinTimes", 0)
				player.qianNengData["WinTimes"] = winTimes + 1
				
class SEAction437( SEActionBase ):
	"""
	终点满足不同条件喊不同话
	CST-11294
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.winTimes = int(section["param1"].strip())
		self.voices = section["param2"].split("|")
		
	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		
		for player in spaceEntity._spaceRoles:
			winTimes = player.qianNengData.get("WinTimes", 0)
			if winTimes >= self.winTimes:
				player.showMessagePlaySound(self.voices[0])
			else:
				player.showMessagePlaySound(self.voices[1])
		
SEActionBase.setActionClass("SEAction152", SEAction152)
SEActionBase.setActionClass("SEAction270", SEAction270)
SEActionBase.setActionClass("SEAction316", SEAction316)
SEActionBase.setActionClass("SEAction433", SEAction433)
SEActionBase.setActionClass("SEAction434", SEAction434)
SEActionBase.setActionClass("SEAction435", SEAction435)
SEActionBase.setActionClass("SEAction436", SEAction436)
SEActionBase.setActionClass("SEAction437", SEAction437)