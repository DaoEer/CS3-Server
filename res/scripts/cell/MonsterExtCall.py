# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import csdefine
import Math
import math
import random
import Functions
import Const
import Monster
import FightRuleMgr
from CoreObject import MonsterHasBaseObject
from CoreObject import MonsterObject
from StateInterface.MonsterStateInterface import MonsterStateInterface
import CoreInterface.MonsterCombatInterface as MonsterCombatInterface
from SpaceCopy import SpaceCopy
from SpacePlane import SpacePlane


class MonsterExtCall(  MonsterHasBaseObject.MonsterHasBaseObject ):
	"""
	召唤类怪物
	"""

	def __init__( self ):
		MonsterHasBaseObject.MonsterHasBaseObject.__init__( self )
		self.isSetServerPosFilter = False
		self.setMonsterType( csdefine.MONSTER_TYPE_MONSTER_EXT_CALL )
		if self.owner:
			self.owner.cell.registerCallMonster( self.scriptID, self.base )
			self.mExtCallCopyOwnerEnemyList()
			if self.getOwnerEntity().hasEffectState(csdefine.EFFECT_STATE_PROTECT):
				self.addMonsterExtCallProtect()
		self.chaseOwnerDistance = 10.0


	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt( csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_CALL )

	def setVisible(self, isVisible):
		"""
		设置其他玩家对自身是否可见
		"""
		self.isVisible = isVisible


	def getOwnerEntity(self):
		"""
		"""
		if not self.owner:
			return None
		owner = KBEngine.entities.get( self.owner.id,None )
		if owner and  self.spaceID == owner.spaceID: #不在一个地图，默认为找不到
			return owner
			
		return None


	def addToEntityRecord(self, scriptID, entityID):
		"""
		添加到地图记录(大地图不记录)
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.addEntityRecord(self.scriptID,self.id)		
			spaceEntity.addEntityMailBoxRecord( self.scriptID, self )

	def removeFromEntityRecord(self, scriptID, entityID):
		"""
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.delEntityRecord(self.scriptID,self.id)				
			spaceEntity.delEntityMailBoxRecord( self.scriptID, self )

	def followOwner( self, spaceScriptID, cellMB, position, direction ):
		"""
		<Define method>
		跟随归属者
		"""
		if spaceScriptID in self.enableSpace or len( self.enableSpace ) == 0:
			self.spawnPos = position
			self.spawnDir = direction
			oldSpaceID = self.spaceID
			KBEDebug.DEBUG_MSG("MonsterExtCall:%d:%s followOwner %s, %s" %(self.id, self.scriptID, spaceScriptID, self.enableSpace))
			oldSpaceScriptID = self.getCurrentSpaceData( Const.SPACE_DATA_SCRIPT_ID )
			self.removeFromEntityRecord(self.scriptID, self.id)
			self.teleport( cellMB, position, direction )
			self.onMExtCallEnterSpaceNotify( oldSpaceID, oldSpaceScriptID )

	def monsterExtCallChaseOwner( self, minDist, maxDist ):
		"""
		追击主人
		"""
		master = KBEngine.entities.get( self.owner.id, None )
		if not master:
			return	
		distance = self.position.distTo( master.position )
		if distance < maxDist:
			self.behControlReset(0)
			self.setTargetID(0)
			self.chaseEntity( master,minDist)
		if distance >= maxDist:
			radian = random.uniform(-3.14,3.14)
			self.position = Math.Vector3( (master.position.x + minDist*math.sin(radian), master.position.y, master.position.z + minDist*math.cos(radian)) )
			#self.position = master.position
			self.behControlReset(0)
			self.setTargetID(0)
		


	def onMExtCallEnterSpaceNotify( self, oldSpaceID, oldSpaceScriptID ):
		"""
		define method
		怪物传送后的回调
		"""
		if oldSpaceID != self.spaceID:
			newSpaceScriptID = self.getCurrentSpaceData( Const.SPACE_DATA_SCRIPT_ID )
			self.triggerSkillEvent( csdefine.SKILL_EVENT_SPACE_CHANGE, self.id, { "OldSpaceID" : oldSpaceScriptID, "NewSpaceID" :newSpaceScriptID ,"isInNewSpace":1 if oldSpaceScriptID == newSpaceScriptID else 0 } )
		self.addToEntityRecord(self.scriptID, self.id)


	def mExtCallAddEnemyCheck( self, entityID ):
		"""
		检测能否添加当前目标入敌人列表
		"""
		targetEntity = KBEngine.entities.get(entityID,None)
		if not targetEntity:
			return False
		ownerEntity = self.getOwnerEntity()
		if not ownerEntity:
			return False
		if targetEntity.position.flatDistTo(ownerEntity.position)>self.territoryRange:
			return False
		return True


	def mExtCallCopyOwnerEnemyList( self ):
		"""
		怪物复制玩家的敌人列表
		"""
		ownerEntity = KBEngine.entities.get( self.owner.id, None )
		if not ownerEntity:
			return	
		for enemyID in ownerEntity.enemyList.keys():
			if self.mExtCallAddEnemyCheck(enemyID):
				self.addEnemy( enemyID )

	def clearEnemyList( self ):
		"""
		清空敌人列表
		"""
		for id in list(self.enemyList):
			enemyEntity = KBEngine.entities.get( id, None )
			if enemyEntity:
				FightRuleMgr.g_fightMgr.breakEnemyRelation( self ,enemyEntity )
			else:
				self.removeEnemy(id)


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


	def chooseTargetByDistance(self):
		"""
		选择距离玩家最近且在视野范围内的怪物作为攻击目标
		"""
		if  self.targetID:
			return
		self.getScript().chooseTargetByDistance( self )
		

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
		self.chooseTargetByDistance()					
		

	def monsterAICheckInTerritory( self ):
		"""
		是否在领域范围 以到主人的距离为领域范围
		"""
		ownerEntity = KBEngine.entities.get( self.owner.id, None )
		if not ownerEntity:
			return	
		return self.position.distTo( ownerEntity.position ) <= self.territoryRange



	def addDamageList( self, entityID, damage ):
		"""
		添加伤害列表 如果距离主人位置超过跟随距离则不反击
		@param entityID  : entityID
		@param damage	 : 伤害值
		"""

		ownerEntity = KBEngine.entities.get( self.owner.id, None )
		if ownerEntity:
			if self.position.distTo( ownerEntity.position ) > self.territoryRange:
				return
		MonsterCombatInterface.MonsterCombatInterface.addDamageList( self, entityID, damage )
	
	def onEnterReset( self ):
		"""
		进入回走状态
		"""
		ownerEntity = KBEngine.entities.get( self.owner.id, None )
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
			attackID = self.chooseTargetByDistance()		#切换成战斗状态时自动将敌人列表中的距离主人最近的敌人作为攻击目标
			if attackID:
				self.setTargetID(attackID)
		else:
			self.monsterAICombatTime = 0	

		#重置状态后可以被再次呼叫
		if newState == csdefine.ENTITY_STATE_RESET:
			self.callSign = False
