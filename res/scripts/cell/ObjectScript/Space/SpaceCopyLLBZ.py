# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
from ObjectScript.Space.SpaceCopy import SpaceCopy
import Const
import Math
import math
import Functions
import KBEMath
from ConfigObject.SpaceCopyLLBZNoticeLoader import g_SpaceCopyLLBZNotice
from ConfigObject.SpaceCopyLLBZRewardsLoader import g_SpaceCopyLLBZRewards

class SpaceCopyLLBZ( SpaceCopy ):
	"""
	玲珑宝珠副本
	"""

	def __init__( self ):
		SpaceCopy.__init__( self )
		self.NPCToMonsterDir = {}

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		NPCToMonsterStr = configData["SpaceData"].get("NPCToMonster","")
		if NPCToMonsterStr:
			for i in NPCToMonsterStr.split("|"):
				List  = i.split(":")
				self.NPCToMonsterDir[List[0]] = List[1]

	def onPlayLingQiLock(self, player, scriptID, difficulty, time):
		"""
		玩灵气锁游戏回调
		"""
		spaceEntity = player.getCurrentSpace()
		spaceEntity.gameCount += 1


		notice = g_SpaceCopyLLBZNotice.getLingQiNotice( difficulty, time )
		self.onConditionChange( spaceEntity, "LLBZ", None, notice, "")

		NPCList = spaceEntity.getEntityMailBoxRecord(scriptID)
		if not len(NPCList):
			return
		NPC = NPCList[0]
		if time > 20:
			self.createMonster(NPC.position, NPC.direction, scriptID, spaceEntity)
			return
		NPC.destroySelf()

	def onPlayLingHuanJue(self, player, scriptID, difficulty, time):
		"""
		玩灵幻决游戏回调
		"""
		spaceEntity = player.getCurrentSpace()
		spaceEntity.gameCount += 1

		notice = g_SpaceCopyLLBZNotice.getLingHuanNotice( difficulty, time )
		self.onConditionChange( spaceEntity, "LLBZ", None, notice, "")

		NPCList = spaceEntity.getEntityMailBoxRecord(scriptID)
		if not len(NPCList):
			return
		NPC = NPCList[0]
		if time > 20:
			self.createMonster(NPC.position, NPC.direction, scriptID, spaceEntity)
			return
		NPC.destroySelf()

	def onLLBZGameComplete(self):
		"""
		玲珑宝珠完成所有游戏
		"""
		spaceEntity = player.getCurrentSpace()
		if spaceEntity.gameCount >= 8:
			self.onConditionChange( spaceEntity, "LLBZ", None, "complete", "")


	def createMonster(self, position, direction, scriptID, spaceEntity):
		"""
		游戏未及时完成创建小怪
		"""
		offsetFront = 5   #向前偏移
		yaw = direction.z
		pos = Math.Vector3(position)
		pos.x += offsetFront * math.sin( yaw )
		pos.z += offsetFront * math.cos( yaw )
		newEntity = spaceEntity.createEntityByScriptID(self.NPCToMonsterDir[scriptID], pos, direction,{ "spawnPos":pos,"spawnDir":direction})

	def setDiffcultyDatas(self, spaceEntity):
		"""	
		设置随机难度数据
		"""
		for scriptID in self.NPCToMonsterDir:
			spaceEntity.diffcultyDatas[scriptID] = g_SpaceCopyLLBZNotice.getLingQiDiffculty()

