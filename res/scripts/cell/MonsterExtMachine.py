# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import csdefine
import csstatus
import Math
import math
import random

import Monster
import CoreInterface.MonsterCombatInterface as MonsterCombatInterface
from ConfigObject import PatrolRouteLoader



class MonsterExtMachine(  Monster.Monster ):
	"""
	机关怪（箭塔，滚石之类）
	"""

	def __init__( self ):
		Monster.Monster.__init__( self )


		
#---------------------------重载方法-----------------------------------------------------

	def onAddEnemy( self, entityID ):
		"""
		重载此方法，添加敌人时不会进入战斗状态
		"""
		self.onEnemyListChange( entityID )
		#将第一进入敌人列表的entity作为攻击目标
		if len(self.enemyList) == 1:
			self.setTargetID(entityID)


	def onMonsterAIQuitPeadCB( self ):
		"""
		退出准备状态回调
		重载此方法，退出准备状态时切换到稳定状态
		"""
		#战斗列表为空切换到自由状态,战斗列表不为空切换到战斗状态
		if self.getState()!=csdefine.ENTITY_STATE_PEAD:
			return
		self.changeState( csdefine.ENTITY_STATE_STABLE )

	def chaseEntity( self, entity, distance ):
		"""
		当前怪物不需要追击
		"""
		pass



