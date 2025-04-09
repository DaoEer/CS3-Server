# -*- coding: utf-8 -*-

import KBEngine
from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEDebug
import Math
import time
import csstatus
import Const
import Functions
import csdefine
import csconst


class SpaceCopyLingYuShouHun( SpaceCopy ):
	"""
	灵域狩魂(CST-3232 程序需求——35级环任务“灵域狩魂”需求)
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )

	
	def initData( self, configData ):
		"""
		"""
		SpaceCopy.initData( self, configData )
		self.monsterData = configData["SpaceData"]["monsterData"]
		self.playerDeadPunish = configData["SpaceData"]["playerDeadPunish"]

	def onEnter( self, selfEntity, playerRole, packArgs ):
		playerRole.disMountPet()
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		self.spaceEvent_addCount(selfEntity, "LYSH_score", 0)

	def startSpaceLife( self, selfEntity ):
		"""
		开始计时
		"""
		spaceLifeSecond = self.spaceLife + selfEntity.dynamicTime
		selfEntity.lifeTime = self.spaceLife		# 副本时长
		selfEntity.lifeStartTime = time.time()		# 副本计时开始时间
		if self.getSpaceType() == csdefine.SPACE_TYPE_STORY_COPY:
			selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( spaceLifeSecond - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_PLANE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		else:
			selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( spaceLifeSecond - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		for e in selfEntity._spaceRoles:
			e.client.ShowSpaceLife( str(spaceLifeSecond * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() ))


	def onMonsterDie(self, selfEntity, monsterID, monsterScriptID):
		"""
		"""
		SpaceCopy.onMonsterDie(self, selfEntity, monsterID, monsterScriptID)
		self.updateScore_1(selfEntity, monsterScriptID)


	def onPlayerDie( self, selfEntity, playerID, playerMB ):
		"""
		玩家死亡
		"""
		SpaceCopy.onPlayerDie(self, selfEntity, playerID, playerMB )
		selfEntity.score = max(self.playerDeadPunish + selfEntity.score, 0)
		playerMB.client.UpdateScoreForLHSL(1, selfEntity.score)
		self.spaceEvent_addCount(selfEntity, "LYSH_score", self.playerDeadPunish)

		
	def updateScore_1(self, selfEntity, monsterScriptID, isOpen=1):
		"""
		1技能 更新计分
		isOpen = 0 :关闭界面
		isOpen = 1 :更新界面
		"""
		#根据关系计分
		player = selfEntity._spaceRoles[0]
	
		for  value in self.monsterData:
			if monsterScriptID in value["scriptID"]:
				if value["relation"] == 0:
					score = value["reward"][0]
				else:
					score = value["reward"][1]
				selfEntity.score = max(score+selfEntity.score, 0)
				player.client.UpdateScoreForLHSL(isOpen, selfEntity.score)
				self.spaceEvent_addCount(selfEntity, "LYSH_score", score)
				#KBEDebug.ERROR_MSG("LHSL-------------score--------------:",self.score)
				return

	def updateScore_2(self, selfEntity, monsterScriptID, isOpen=1):
		"""
		2技能 更新计分
		isOpen = 0 :关闭界面
		isOpen = 1 :更新界面
		"""
		#根据关系计分
		player = selfEntity._spaceRoles[0]
	
		for  value in self.monsterData:
			if monsterScriptID in value["scriptID"]:
				if value["relation"] == 1:
					score = value["reward"][0]
				else:
					score = value["reward"][1]
				selfEntity.score = max(score+selfEntity.score, 0)
				player.client.UpdateScoreForLHSL(isOpen, selfEntity.score)
				self.spaceEvent_addCount(selfEntity, "LYSH_score", score)
				#KBEDebug.ERROR_MSG("LHSL-------------score--------------:",self.score)
				return

		
	def LHSL_SetScoreUI(self, selfEntity, player, isOpen):
		"""
		设置积分面板(开启/关闭)
		"""
		player.client.UpdateScoreForLHSL(isOpen, max(0,selfEntity.score))



