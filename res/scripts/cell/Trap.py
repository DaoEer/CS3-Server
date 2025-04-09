# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import csdefine
import Const
from CoreObject.TrapObject import TrapObject
from StateInterface.TrapStateInterface import TrapStateInterface
from CoreInterface.SkillInterface import SkillInterface

from CoreInterface.EntityRelationTable import EntityRelationTable


class Trap( TrapObject, TrapStateInterface, SkillInterface, EntityRelationTable ):
	"""
	陷阱类
	"""
	def __init__( self ):
		TrapObject.__init__( self )
		TrapStateInterface.__init__(self)
		SkillInterface.__init__( self )
		EntityRelationTable.__init__( self )
		self.enterEntityRecd = {}			#记录进入过陷阱的entity
		self.leaveEntityRecd = {}			#记录离开过陷阱的entity		
		self.delayOnEnterDead()


	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		if self.entityScript == "ClientTriggerTrap" or self.entityScript == "ClientTriggerTrapDoOnce" or self.entityScript == "ClientTriggerTrapVortex":
			self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_CLIENT_TRIGGER_TRAP)
		else:
			TrapObject.setSelfEntityFlagExt(self)

	def delayOnEnterDead( self ):
		"""
		延迟进入死亡状态
		"""
		dT = self.getScript().delayDeadTime
		if dT:
			self.addTimerCallBack(float(dT),"changeState",(csdefine.ENTITY_STATE_DEAD,))
			

	def onEnterCommonTrap( self, entity, rangeXZ, rangeY, controllerID ):
		"""
		callback method.
		进入陷阱
		"""
		if not entity.isReady() or entity.inDestroying():
			return
		if self.isState(csdefine.ENTITY_STATE_DEAD):
			return
		
		if entity.id  not in self.enterIDs:
			self.enterIDs.append( entity.id )
		self.getScript().onEnterTrap( self, entity.id )
	
	def onLeaveCommonTrap( self, entity, controllerID ):
		"""
		callback method.
		离开陷阱
		"""
		if not entity.isReady() or entity.inDestroying():
			return
		if self.isState(csdefine.ENTITY_STATE_DEAD):
			return

		if entity.id in self.enterIDs:
			self.enterIDs.remove( entity.id )
		self.getScript().onLeaveTrap( self, entity.id )

	def CELL_onEnter( self, exposed, enterID ):
		"""
		<Exposed Method>
		进入客户端陷阱
		"""
		if self.getEntityFlagExt() != csdefine.ENTITY_FLAG_EXT_CLIENT_TRIGGER_TRAP and self.getEntityFlagExt() != csdefine.ENTITY_FLAG_EXT_MOVE_TRAP:
			return
		if self.isState(csdefine.ENTITY_STATE_DEAD):
			return

		if enterID == self.id:
			return

		if enterID  not in self.enterIDs:
			self.enterIDs.append( enterID )
		self.getScript().onEnterClientTrap( self, enterID )
	
	def CELL_onLeave( self, exposed, enterID ):
		"""
		<Exposed Method>
		离开客户端陷阱
		"""
		if self.getEntityFlagExt() != csdefine.ENTITY_FLAG_EXT_CLIENT_TRIGGER_TRAP and self.getEntityFlagExt() != csdefine.ENTITY_FLAG_EXT_MOVE_TRAP:
			return
		if self.isState(csdefine.ENTITY_STATE_DEAD):
			return
		if enterID == self.id:
			return

		if enterID in self.enterIDs:
			self.enterIDs.remove( enterID )
			self.getScript().onLeaveClientTrap( self, enterID )

	def beforeUseSkill( self, skill, target ):
		"""
		在使用技能之前要做的事情
		"""
		pass
		
	def addEnemyCheck( self, entityID ):
		"""
		extend method.
		"""
		return False
		
	def onWitnessed( self, isWitnessed ):
		"""
		玩家视野范围内才开始执行
		"""
		self.getScript().onWitnessed( self, isWitnessed )


	def playAction( self, actionID ):
		"""
		播放动作
		"""
		self.allClients.CLIENT_OnPlayAction(actionID,-1.0)
	

	def delayToAddTrap(self):
		"""
		延時添加陷阱
		"""
		self.allClients.CLIENT_DelayToAddTrap(self.getScript().delayStartTime)

	def cycleBegin(self):
		"""
		开启周期行为
		"""
		self.getScript().cycleBegin(self)

	def delayCycleBegin(self):
		"""
		延时开启周期行为
		"""
		delayStartTime = self.getScript().delayStartTime
		if delayStartTime ==0:
			self.cycleBegin()
		else:
			self.addTimerCallBack(delayStartTime, "cycleBegin", ())
	#----------------------重载方法-------------------------------
	
	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		self.delayToAddTrap()
		self.delayCycleBegin()


	def onEnterDead( self ):
		"""
		virtual method
		进入死亡状态
		"""
		TrapStateInterface.onEnterDead( self )
		self.getScript().onEnterDead( self )
		self.getCurrentSpace().onTrapDie( self.id )
		for entityID in self.enterIDs:
			if self.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_CLIENT_TRIGGER_TRAP:
				self.getScript().onLeaveClientTrap( self, entityID )
			else:
				self.getScript().onLeaveTrap( self, entityID )
		effectID = self.getScript().deadEffectID
		if effectID:
			self.allClients.CLIENT_PlayDeadEffect(effectID)
		destroyTime = self.getScript().destroyTime
		if destroyTime:
			self.delayDestroy( destroyTime )
		else:
			self.destroySelf()

	def onStateChanged(self, new, old):
		"""
		"""
		TrapStateInterface.onStateChanged(self, new, old)
		self.triggerSkillEvent( csdefine.SKILL_EVENT_STATE_CHANGE, self.id, {"oldState":old, "newState":new} )
		self.triggerEntityEvent(csdefine.ENTITY_EVENT_ENTITY_STATE_CHANGE, {"oldState":old, "newState":new})

	def onActWordChangedTrigger(self, params):
		"""
		"""
		TrapStateInterface.onActWordChangedTrigger(self, params)
		act, disabled =  params
		self.triggerSkillEvent( csdefine.SKILL_EVENT_ACT_WORD_CHANGE, self.id, {"actWord":act, "disabled": disabled})