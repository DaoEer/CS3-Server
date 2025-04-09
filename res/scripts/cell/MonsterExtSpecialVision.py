# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import csdefine
import csstatus
import Math
import math
import random
import csarithmetic
import copy
import FightRuleMgr

import Monster
import CoreInterface.MonsterCombatInterface as MonsterCombatInterface
from ConfigObject import PatrolRouteLoader


VIEW_HEIGTH = 10.0   #视野高度

class MonsterExtSpecialVision(Monster.Monster ):
	"""
	妖卫，CST-3248
	"""

	def __init__( self ):
		"""
		Monster.json配置表
		param1:  radius|angle，半径|角度（扇形）
		"""
		Monster.Monster.__init__( self )
		self.warningList = []
		if self.getScript().param1:
			param1 = self.getScript().param1.split("|")
		else:
			param1 = [30, 90]
		self.viewRadius = float(param1[0])
		self.viewAngle = float(param1[1])
		self.isPlayerInView = False 			#玩家是否在视野范围 交给客户端tick检测


	def checkWarningList(self):
		"""
		检查警告列表，并清理已经不在视野内的所有警告列表
		"""
		for entity in range(len(self.warningList)-1, -1, -1):
			if not self.monsterAICheckInViewRange(entity.id):
				self.warningList.remove(entity)
		

#---------------------------重载方法-----------------------------------------------------
		
	def onViewRange( self ):
		"""
		视野范围，这里的视野范围是整个地图，玩家和妖卫之间没有光墙就在视野范围之内
		"""
		return

		#清理已经不在视野内的所有敌人
		for id in list(self.enemyList):
			if not self.monsterAICheckInViewRange( id ):
				enemyEntity = KBEngine.entities.get( id, None )
				if enemyEntity:
					FightRuleMgr.g_fightMgr.breakEnemyRelation( self, enemyEntity )
				else:
					self.removeEnemy(id)
		self.checkWarningList()

	def monsterAICheckInViewRange(self, id):
		"""
		是否在视野范围
		"""
		return self.isPlayerInView

	def getPlayer(self):
	  	"""
	  	获取玩家
	  	"""
	  	spaceEntity = self.getCurrentSpace()
	  	if not spaceEntity:
	  		KBEDebug.ERROR_MSG("getCurrentSpace is None!")
	  		return
	  	playerList = spaceEntity.getSpaceRoles()
	  	if not len(playerList):
	  		#KBEDebug.ERROR_MSG("playerList length is None!")
	  		return
	  	player = playerList[0]
	  	return player

	def addViewShapeTrap(self):
		"""
		添加视野陷阱
		"""
		player = self.getPlayer()
		if not player:
			KBEDebug.ERROR_MSG("player is not exist!")
			return

		player.clientEntity(self.id).CLIENT_CreateViewShapeTrap(self.viewRadius, self.viewAngle, VIEW_HEIGTH)
		#player.clientEntity(self.id).CLIENT_OpenInitiactiveTrapEffect(4, self.viewRadius, int(self.viewAngle), 5.0)
		

	def CELL_SetIsPlayerInViewRange(self, srcEntityID, isPlayerInView):
		"""
		"""
		oldState = self.isPlayerInView
		self.isPlayerInView = isPlayerInView

		#从无到有 建立战斗关系 从有到无移除战斗关系
		player = self.getPlayer()
		if not player:
			return
		if self.isPlayerInView:
			if self.canBuildEnemyRelation(player) :
				FightRuleMgr.g_fightMgr.buildEnemyRelation( self, player)


	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		Monster.Monster.CELL_onClientReady(self, srcEntityID)
		self.addViewShapeTrap()
		