# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEDebug
import Math
import csdefine
import csconst
import csstatus
import time, random
import Functions
import KBEMath

class SpaceCopySparHunTing( SpaceCopy ):
	"""
	晶石狩猎场
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
	
	def initData( self, configData ):
		"""
		"""
		SpaceCopy.initData( self, configData )
		self.minLevel = configData["SpaceData"].get("minLevel",0)
		self.maxLevel = configData["SpaceData"].get("maxLevel",0)
		self.maxCampEnter = configData["SpaceData"].get("maxCampEnter",0)
		self.exchange = configData["SpaceData"].get("exchange",0)
		self.buffID = int(configData["SpaceData"].get("buffID", 0))
		self.luckySpaceTimes = configData["SpaceData"].get("luckySpaceTimes",0)
		self.storyID = configData["SpaceData"].get("storyID", "")
		self.killRoleFeat = configData["SpaceData"].get("killRoleFeat", "")
		self.startNotify = configData["SpaceData"].get("startNotify","")
		
	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopy.initEntity( self, selfEntity )
		selfEntity.setExchMoneyScale( self.exchange )
		selfEntity.setIntegralOverflowBuffID( self.buffID )

	def activeStart( self, selfEntity ):
		"""
		活动开始
		"""
		self.startSpaceLife( selfEntity )
		self.spaceEvent_onConditionChange( selfEntity, "", selfEntity.id, self.startNotify, {} )

	def startSpaceLife( self, selfEntity ):
		"""
		开始计时
		"""
		spaceLifeSecond = self.spaceLife + selfEntity.dynamicTime
		selfEntity.lifeTime = self.spaceLife		# 副本时长
		selfEntity.lifeStartTime = time.time()		# 副本计时开始时间
		for e in selfEntity._spaceRoles:
			e.client.ShowSpaceLife( str(spaceLifeSecond * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() ) )

	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		selfEntity.addSparHunTingMemberData( playerRole )
		selfEntity.setIntegralMax(1000)  	#这里暂定为金精上限1000
		
		tempSparHunTingIntegral = 0
		
		if playerRole.playerDBID in selfEntity.luckySpaceRoles:
			selfEntity.luckySpaceRoles.pop(playerRole.playerDBID)
			selfEntity.addPlayerIntegral(playerRole, playerRole.sparHunTingIntegral, True)
			tempSparHunTingIntegral = playerRole.sparHunTingIntegral
			playerRole.setSparHunTingIntegral(0)
			
			playerDBIDList = selfEntity.queryTemp("playerDBIDList", [])
			if playerRole.playerDBID not in playerDBIDList:
				playerDBIDList.append(playerRole.playerDBID)
				selfEntity.setTemp("playerDBIDList", playerDBIDList)
		
		#CST-11806 需求（机缘玩法）——出机缘玩法后播放公告
		if tempSparHunTingIntegral >= 2000:
			for role in selfEntity._spaceRoles:
				role.statusMessage(csstatus.SPARHUNTING_GET_MANAY_GIFT, playerRole.playerName)

	def onLeave( self, selfEntity, playerRole, packArgs ):
		if playerRole.playerDBID not in selfEntity.luckySpaceRoles: #如果是进入机缘玩法副本，则不自动换成金钱
			selfEntity.playerExchangeToMoney(playerRole)
		playerRole.removeBuffByID(self.buffID)
		selfEntity.removeSparHunTingMemberData( playerRole )
		SpaceCopy.onLeave( self, selfEntity, playerRole, packArgs )

	def getPackDomainData( self, playerEntity, args ):
		"""
		"""
		packDict = SpaceCopy.getPackDomainData( self, playerEntity, args )
		packDict["playerDBID"] = playerEntity.playerDBID
		packDict["camp"] = playerEntity.getCamp()
		packDict["level"] = playerEntity.getLevel()
		return packDict
		
	def onTrigger_luckySpace( self, selfEntity, playerEntity ):
		"""
		触发机缘副本
		"""
		if not self.storyID:
			return
		
		data = selfEntity.queryTemp("JiyuanSpaceData", {})
		if playerEntity.playerDBID not in data:
			data[playerEntity.playerDBID] = self.luckySpaceTimes
			selfEntity.setTemp("JiyuanSpaceData", data)
		
		luckySpaceTimes = data.get(playerEntity.playerDBID)
		if self.luckySpaceTimes and luckySpaceTimes > 0:
			#playerEntity.onTriggerLuckySpace()
			self.onEnterLuckySpace(selfEntity, playerEntity)
			for e in selfEntity._spaceRoles:
				e.statusMessage(csstatus.SPARHUNTING_ROLE_GET_LUCKY, playerEntity.getName())
			
	def onEnterLuckySpace( self, selfEntity, playerEntity ):
		"""
		"""
		playerEntity.hideStatusMessage(csstatus.SPARHUNTING_INTEGRAL_MAX)
		data = selfEntity.queryTemp("JiyuanSpaceData", {})
		luckySpaceTimes = data.get(playerEntity.playerDBID, 0)
		if luckySpaceTimes <= 0:
			return
		
		data[playerEntity.playerDBID] -= 1
		selfEntity.setTemp("JiyuanSpaceData", data)
		
		if playerEntity.playerDBID not in selfEntity.luckySpaceRoles:
			selfEntity.luckySpaceRoles[playerEntity.playerDBID] = playerEntity.base
		
		playerEntity.sparHunTingpIntegral = 0
		playerEntity.setTemp("copy_exchMoneyScale", selfEntity.exchMoneyScale)
		playerEntity.client.StartPlayStory(self.storyID, 1)
	
	def onTeleportCompleted( self, selfEntity, playerRole ):
		#只有第一次进来的时候播放语音
		playerDBIDList = selfEntity.queryTemp("playerDBIDList", [])
		if playerRole.playerDBID in playerDBIDList:
			return
		
		# 播放场景语音
		if self.spaceIntroduce:
			if self.sceneVoiceTriggerNum:
				if selfEntity.scriptID not in playerRole.sceneVoiceTriggerNum:
					playerRole.showMessagePlaySound( self.spaceIntroduce["voiceID"] )
					playerRole.sceneVoiceTriggerNum[ selfEntity.scriptID ] = 1
				elif playerRole.sceneVoiceTriggerNum[ selfEntity.scriptID ] < self.sceneVoiceTriggerNum:
					playerRole.showMessagePlaySound( self.spaceIntroduce["voiceID"] )
					playerRole.sceneVoiceTriggerNum[ selfEntity.scriptID ] += 1
			else:
				playerRole.showMessagePlaySound( self.spaceIntroduce["voiceID"] )

	def getKillRoleFeat(self):
		return self.killRoleFeat