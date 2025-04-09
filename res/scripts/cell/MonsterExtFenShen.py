# -*- coding: utf-8 -*-

import time, random

import math
import Math
import KBEDebug
import KBEngine
import Monster
import csstatus
import csdefine
import Functions

from StateInterface.MonsterStateInterface import MonsterStateInterface
import CoreInterface.MonsterCombatInterface as MonsterCombatInterface

class MonsterExtFenShen( Monster.Monster ):
	"""
	分身怪物
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.initFenShen()
		
	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_FENSHEN)
		
	def calcAttachProperties( self ):
		"""
		重新计算战斗属性
		"""
		pass
		
	def initFenShen(self):
		"""
		"""
		owner = self.getOwnerEntity()
		if owner is None:
			KBEDebug.ERROR_MSG("not found owner")
			return
		
		self.mExtCallCopyOwnerEnemyList()
		if owner.hasEffectState(csdefine.EFFECT_STATE_PROTECT):
			self.addMonsterExtCallProtect()
		
	def getRelation( self, targetEntity ):
		"""
		"""
		player = self.getOwnerEntity()
		if not player:
			return
		
		return player.queryRelation(targetEntity)
		
	def getOwnerEntity( self ):
		"""
		"""
		return KBEngine.entities.get( self.ownerID,None )

		
	def beforeDestroy( self ):
		"""
		"""
		owner = self.getOwnerEntity()
		if owner is None:
			KBEDebug.ERROR_MSG("not found owner[%s]" %(self.ownerID))
			return
		
		owner.updateFenShenData(self.id, self.HP, self.HP_Max, self.MP, self.MP_Max)
		
	def cancelMonsterAIQuitPead( self ):
		"""
		取消延迟退出准备状态，并设置monsterAIQuitPeadTimeID不为0 以免切换状态时重新加monsterAIQuitPeadTimeID
		"""
		if self.monsterAIQuitPeadTimeID:
			self.popTimer(self.monsterAIQuitPeadTimeID)
		self.monsterAIQuitPeadTimeID = 1

	def addMonsterExtCallProtect(self):
		"""
		"""
		self.behControlReset(0)
		self.cancelMonsterAIQuitPead()
		self.changeState( csdefine.ENTITY_STATE_PEAD )
		
	def removeMonsterExtCallProtect(self):
		"""
		"""
		self.onMonsterAIQuitPeadCB()
		
	def mExtCallAddEnemyCheck( self, entityID ):
		"""
		检测能否添加当前目标入敌人列表
		"""
		targetEntity = KBEngine.entities.get(entityID,None)
		if not targetEntity:
			return False
		
		owner = self.getOwnerEntity()
		if not owner:
			return False
		
		if targetEntity.position.flatDistTo(owner.position)>self.territoryRange:
			return False
			
		return True
		
	def mExtCallCopyOwnerEnemyList( self ):
		"""
		怪物复制玩家的敌人列表
		"""
		owner = self.getOwnerEntity()
		if not owner:
			return
		
		for enemyID in owner.enemyList.keys():
			if self.mExtCallAddEnemyCheck(enemyID):
				self.addEnemy( enemyID )
				
	def monsterExtCallChaseOwner( self, minDist, maxDist ):
		"""
		追击主人
		"""
		owner = self.getOwnerEntity()
		if owner is None:
			return
		
		distance = self.position.distTo( owner.position )
		if distance < maxDist:
			self.behControlReset(0)
			self.setTargetID(0)
			self.chaseEntity( owner,minDist)
		else:
			radian = random.uniform(-3.14,3.14)
			self.position = Math.Vector3( (owner.position.x + minDist*math.sin(radian), owner.position.y, owner.position.z + minDist*math.cos(radian)) )
			#self.position = owner.position
			self.behControlReset(0)
			self.setTargetID(0)

	def chooseTarget(self):
		"""
		选择在视野范围内的怪物作为攻击目标(优先选择owenr当前的目标)
		"""
		if  self.targetID:
			return
		
		self.getScript().chooseTarget( self )
	
#---------------------------重载方法-----------------------------------------------------
	def monsterAICheckInViewRange( self, id ):
		"""
		是否在视野范围
		"""
		entity = KBEngine.entities.get( id, None )
		ownerEntity = self.getOwnerEntity()
		if entity and ownerEntity:
			if entity.position.flatDistTo( ownerEntity.position ) <= self.territoryRange and self.checkScoutHeight( entity ):
				return True
		
		return False

	def onViewRange( self ):
		"""
		当攻击目标出了视野范围重新选定下一个攻击目标
		return :None
		"""
		ownerEntity = self.getOwnerEntity()
		if not ownerEntity:
			return
		
		if not self.monsterAICheckInViewRange( self.targetID ):
			self.setTargetID(0)
			
		self.chooseTarget()

	def addDamageList( self, entityID, damage ):
		"""
		添加伤害列表 如果距离主人位置超过跟随距离则不反击
		@param entityID  : entityID
		@param damage	 : 伤害值
		"""

		ownerEntity = self.getOwnerEntity()
		if ownerEntity:
			if self.position.distTo( ownerEntity.position ) > self.territoryRange:
				return
		MonsterCombatInterface.MonsterCombatInterface.addDamageList( self, entityID, damage )
	
	def onEnterReset( self ):
		"""
		进入回走状态
		"""
		ownerEntity = self.getOwnerEntity()
		if ownerEntity:
			self.spawnPos = Math.Vector3( ownerEntity.position )
		self.getScript().onEnterReset( self )

	def changeState( self, newState ):
		"""
		改变状态。
			@param newState	:	新的状态
			@type newState	:	integer
		"""
		if self.state == newState:
			return
		MonsterStateInterface.changeState(self,newState)
		
		if newState == csdefine.ENTITY_STATE_FREE:
			self.startRandomWalk(self.getSpeed(), True)
		else:
			self.stopMoving( csdefine.MOVE_TYPE_RANDOM)

		if newState == csdefine.ENTITY_STATE_FIGHT:
			self.startWander()
		else:
			self.stopWander()
		
		if newState == csdefine.ENTITY_STATE_DEAD:
			if self.isPlayDeadEffect():
				self.allClients.CLIENT_PlayDeadEffect()
			if self.isPlayDeadMortuaryEffect():
				self.allClients.PlayDeadMortuaryEffect()		
		
		#记录战斗状态开始时间
		if newState == csdefine.ENTITY_STATE_FIGHT:
			self.monsterAICombatTime = Functions.getTime()
			self.chooseTarget()		
		else:
			self.monsterAICombatTime = 0	
		
	def turnToSkillTarget( self, target):
		"""
		旋转方向
		@param target: 施展对象
		@type  target: 一个包装过的对象entity 被包装对象可能是 (位置，entity, item)详细请看SkillTargetObjImpl.py
		"""
		# 转向处理, 需要精确的方向
		position = target.getObjectPosition()		# 因为分身使用玩家带位移的技能，所以朝向要准确
		self.turnToPos(position)
		
	def onSkillBegin( self, skillInstance, target ):
		"""
		virtual method.
		技能开始
		"""
		Monster.Monster.onSkillBegin( self, skillInstance, target )
		owner = self.getOwnerEntity()
		if owner and owner.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ) and self.controlledBy != owner.base:
			self.controlledBy = owner.base
		self.allClients.BeginPosSyncServer()
		
	def onSkillEnd( self, skillInstance, castResult ):
		"""
		virtual method.
		技能结束

		@param  skillInstance: 技能实例
		@type   skillInstance: SPELL
		"""
		Monster.Monster.onSkillEnd( self, skillInstance, castResult )
		self.addTimerCallBack( 0.1, "delayRemoveControl", () )
		self.allClients.EndPosSyncServer()
			
	def delayRemoveControl( self ):
		"""延迟移除控制"""
		self.controlledBy = None
