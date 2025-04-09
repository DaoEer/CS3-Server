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




class MonsterExtQuest(  Monster.Monster ):
	"""
	任务怪（处理特定任务目标状态下的表现，比如屏蔽主动攻击，语音喊话等）
	"""

	def __init__( self ):
		Monster.Monster.__init__( self )

	
#---------------------------重载方法-----------------------------------------------------



	def onEnterTrap( self, entity, rangeXZ, rangeY, controllerID, userArg = 0 ):
		"""
		进入触发陷阱内
		"""
		if not entity.isReady() or entity.inDestroying():
			return
		
		if not self.getScript().checkQuestStatues(entity):
			return		

		if controllerID not in self.proximityInfo:	#是刚创建陷阱就触发的情况
			if controllerID in self.entersOnAddProximity:
				if entity.id not in self.entersOnAddProximity[ controllerID ]:
					self.entersOnAddProximity[ controllerID ].append( entity.id )
			else:
				self.entersOnAddProximity[ controllerID ] = [ entity.id ]
			return
		
		isSquare = self.proximityInfo[ controllerID ][3]
		if isSquare:	#方形
			if rangeY > 0 and abs( self.position.y - entity.position.y ) > rangeY:	#引擎的陷阱是一个高度无限延伸的“井”，因此加个高度验证避免在高空也能触发地面的陷阱
				return
			userArg = self.proximityInfo[ controllerID ][0]
			self.callEnterTrapCB( entity, rangeXZ, rangeY, controllerID, userArg )
		
		else:	#是“其他形状”陷阱：只添加到记录，不执行进陷阱回调
			if controllerID not in self.shapeProximityEnters:
				self.shapeProximityEnters[controllerID] = [ entity.id ]
			else:
				self.shapeProximityEnters[controllerID].append( entity.id )


	def CELL_onClientEnterAIAttackTrap( self, srcEntityID, enterID ):
		"""
		exposed method
		触发客户端主动攻击陷阱
		"""
		if not self.hasAttackTrap:
			return
		
		entity = KBEngine.entities.get( enterID )
		if not entity:
			return
		if not entity.isReady() or entity.inDestroying():
			return
		if not self.getScript().checkQuestStatues(entity):
			return	
		
		self.monsterAIOnEnterAIAttackTrap( entity, 0, 0, 0 )



	def CELL_onClientEnterInitiativeTrap( self, srcEntityID, enterID ):
		"""
		exposed method
		触发客户端主动反应陷阱
		"""
		if not self.hasInitiativeTrap:
			return
		
		entity = KBEngine.entities.get( enterID )
		if not entity:
			return
		if not entity.isReady() or entity.inDestroying():
			return
		if not self.monsterAIGetCurSubStateObj(): #目前看来，没有子状态的状态上，主动反应陷阱也没有作用
			return
		if not self.getScript().checkQuestStatues(entity):
			return	

		self.monsterAIOnEnterInitiativeTrap( entity, 0, 0, 0 )



	def monsterAIShowMessagePlaySound(self, player, voiceID):
		"""
		播放语音并显示半身像
		"""
		if not player or player.getEntityFlag()!=csdefine.ENTITY_FLAG_ROLE:
			return
		if not self.getScript().checkQuestStatues(player):
			return
		player.showMessagePlaySound(voiceID)