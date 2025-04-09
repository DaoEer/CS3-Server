# -*- coding: utf-8 -*-
import Const
import Math
import KBEMath
import KBEngine
import random
import csdefine
from ObjectScript import Space
from ObjectScript.Space.SpaceCopyMagicMazeChild import SpaceCopyMagicMazeChild
import KBEDebug

class SpaceCopyMagicMazeChildLuck( SpaceCopyMagicMazeChild ):
	"""
	幻阵迷宫 气运玩法
	"""
	def __init__( self ):
		SpaceCopyMagicMazeChild.__init__( self )
		self.delayTeleportTime = 0
		self.delayNotifyTime = 0
		self.voiceList = ""
		self.extraBuffBonus = []
		
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopyMagicMazeChild.initData( self, configData )
		self.delayTeleportTime = configData["SpaceData"].get("delayTeleportTime", 0)
		self.delayNotifyTime = configData["SpaceData"].get("delayNotifyTime", 0)
		voiceID = configData["SpaceData"].get("LuckvoiceID", "")
		if voiceID != "":
			self.voiceList = [i.strip() for i in voiceID.split("|")]
		extraBuffBonus = configData["SpaceData"].get("extraBuffBonus", "")
		if extraBuffBonus != "":
			self.extraBuffBonus = [i.strip() for i in extraBuffBonus.split("|")]

	def random_index( self, rate ):
		"""
		随机变量的概率
		"""
		start = 0 
		index = 0 
		randnum = random.uniform( 1, sum(rate) ) 
		for index, scope in enumerate(rate):
			start += scope
			if randnum <= start:
				break
		return index

	def randomZhuanPan( self, selfEntity):
		"""
		随机结果
		"""
		rate = [7.58,9.09,15.15,11.365,22.72,7.58,15.15,11.365]
		index = self.random_index( rate )
		result = index + 1
		extraRewardRate = 0.0
		extraRewardCount = 0
		belongType,spaceKey = self.getPlayerBelongTypeAndSpaceKey(selfEntity)
		if result == Const.MAGIC_MAZE_LUCK_COPY_TIAN:  		# 天
			extraRewardRate = 0.25
		elif result == Const.MAGIC_MAZE_LUCK_COPY_DI:		# 地
			extraRewardRate = 0.2
		elif result == Const.MAGIC_MAZE_LUCK_COPY_XUAN:		# 玄
			extraRewardRate = 0.15
		elif result == Const.MAGIC_MAZE_LUCK_COPY_HUAN1:	# 黄1
			extraRewardRate = 0.1
		elif result == Const.MAGIC_MAZE_LUCK_COPY_DAY:		# 日
			KBEngine.globalData["MagicMazeSpaceManager"].setSpaceExtraBuffBonus( belongType, spaceKey, int(self.extraBuffBonus[0]),selfEntity.createArgs["mainScriptID"] )
		elif result == Const.MAGIC_MAZE_LUCK_COPY_MONTH:	# 月
			KBEngine.globalData["MagicMazeSpaceManager"].setSpaceExtraBuffBonus( belongType, spaceKey, int(self.extraBuffBonus[1]),selfEntity.createArgs["mainScriptID"] )
		elif result == Const.MAGIC_MAZE_LUCK_COPY_HUAN2:	# 黄2
			extraRewardRate = 0.1

		KBEngine.globalData["MagicMazeSpaceManager"].setSpaceExtraReward( belongType, spaceKey, extraRewardCount, extraRewardRate,selfEntity.createArgs["mainScriptID"] )
		
		#告知玩家效果
		for playerCell in selfEntity._spaceRoles:
			player = KBEngine.entities.get( playerCell.id, None )
			if player:
				player.client.CLIENT_MagicMazeLuckResult(result)
				
		selfEntity.addTimerCallBack( self.delayTeleportTime, "closeSpace", () )
		selfEntity.addTimerCallBackForScript( self.delayNotifyTime, "noticePlayerVoiceMsg", (result,) )
				
	def noticePlayerVoiceMsg(self, selfEntity, result):
		"""
		给予玩家语音提示信息
		"""
		voiceID = ""
		if len(self.voiceList) >= 7:
			if result == Const.MAGIC_MAZE_LUCK_COPY_TIAN:
				voiceID = self.voiceList[0]
			elif result == Const.MAGIC_MAZE_LUCK_COPY_DI:
				voiceID = self.voiceList[1]
			elif result == Const.MAGIC_MAZE_LUCK_COPY_XUAN:
				voiceID = self.voiceList[2]
			elif result == Const.MAGIC_MAZE_LUCK_COPY_HUAN1 or result == Const.MAGIC_MAZE_LUCK_COPY_HUAN2:
				voiceID = self.voiceList[3]
			elif result == Const.MAGIC_MAZE_LUCK_COPY_DAY:
				voiceID = self.voiceList[4]
			elif result == Const.MAGIC_MAZE_LUCK_COPY_MONTH:
				voiceID = self.voiceList[5]
			else:
				voiceID = self.voiceList[6]
		if voiceID != "":
			for playerCell in selfEntity._spaceRoles:
				player = KBEngine.entities.get( playerCell.id, None )
				if player:
					player.showMessagePlaySound( voiceID )
	
	def onEnter( self, selfEntity, playerRole, packArgs ):
		"""
		进入副本通知创建转盘
		"""
		SpaceCopyMagicMazeChild.onEnter( self, selfEntity, playerRole, packArgs )
		player = KBEngine.entities.get( playerRole.id, None )
		if player:
			player.client.CLIENT_CreateLuckZhuanPan()

