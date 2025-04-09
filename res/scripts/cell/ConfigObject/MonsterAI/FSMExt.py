# -*- coding: utf-8 -*-
import csdefine
import KBEDebug
from ConfigObject.MonsterAI.AIBase import AIFSM

#为了减少配置量，加入在不同状态机的拓展支持

class AIFSMCommon( AIFSM.AIFSM ):
	"""
	普通状态机
	根据怪物的状态决定进入AI组状态
	"""
	def __init__( self, AIID ):
		AIFSM.AIFSM.__init__( self, AIID )
		
	def start( self, entity ):
		"""
		开始AI
		"""
		if entity.state == csdefine.ENTITY_STATE_PEAD and entity.monsterAIQuitPeadTimeID == 0:
			entity.monsterAIQuitPeadTimeID = entity.addTimerCallBack( entity.monsterAIQuitPeadDelayTime, "onMonsterAIQuitPeadCB", () )
			entity.isInPending = 1
		AIFSM.AIFSM.start( self, entity )
		self.trigger( entity, csdefine.ENTITY_EVENT_ENTITY_STATE_CHANGE,[ entity.getState(), entity.getState() ], None)#以状态作用切换逻辑的条件，避免了怪物在AI没运行的情况下，切换了状态
	
	def tick( self, entity ):
		"""
		AI 循环
		"""
		tickID = entity.monsterAITickCallBackID
		if entity.isState( csdefine.ENTITY_STATE_FIGHT):
			if not self.checkIsInTerritory(  entity ):
				entity.changeState(csdefine.ENTITY_STATE_RESET)
				return
			entity.onViewRange()

		#如果在前面已经切换了状态，那么中断此tick
		if tickID != entity.monsterAITickCallBackID:
			return
		if self.getAIDataType() == "AIDatas1":
			AIFSM.AIFSM.tick( self,  entity )



class AIFSMExt1( AIFSMCommon ):
	"""
	机关怪状态机
	根据怪物的状态决定进入AI组状态
	"""
	def __init__( self, AIID ):
		AIFSMCommon.__init__( self, AIID )

	def trigger( self,  entity, eventType, args, triggerEntity ):
		AIFSMCommon.trigger( self,  entity, eventType, args, triggerEntity )
				
	def tick( self, entity ):
		"""
		AI 循环
		"""
		tickID = entity.monsterAITickCallBackID

		entity.onViewRange()

		#如果在前面已经切换了状态，那么中断此tick
		if tickID != entity.monsterAITickCallBackID:
			return
		if self.getAIDataType() == "AIDatas1":
			AIFSM.AIFSM.tick( self,  entity )

class AIFSM_YCDMD_BOSS( AIFSMCommon ):
	"""
	CST-8727 勇闯夺命岛Boss 状态机
	"""
	def __init__( self, AIID ):
		AIFSMCommon.__init__( self, AIID )

	def startOnEnter(self, entity):
		"""
		"""
		for groupStateObj in self._groupStates.values():
			if  groupStateObj.isCanEnter( entity, csdefine.ENTITY_EVENT_SPECIAL_ATTRIBUTES_CHANGE, [ "levelYCJMD",entity.getYCJMDBossLevel(), entity.getYCJMDBossLevel()  ], None ):
				groupStateObj.onEnter(entity)
				return

	def tick( self, entity ):
		"""
		AI 循环
		"""
		tickID = entity.monsterAITickCallBackID

		entity.onViewRange()

		#如果在前面已经切换了状态，那么中断此tick
		if tickID != entity.monsterAITickCallBackID:
			return
		if self.getAIDataType() == "AIDatas1":
			AIFSM.AIFSM.tick( self,  entity )



class AIFSMSoldier( AIFSMCommon ):
	"""
	攻城战小兵状态机
	"""
	def __init__( self, AIID ):
		AIFSM.AIFSM.__init__( self, AIID )
		
	def startOnEnter(self, entity):
		"""
		"""
		for groupStateObj in self._groupStates.values():
			if  groupStateObj.isCanEnter( entity, csdefine.ENTITY_EVENT_SPECIAL_ATTRIBUTES_CHANGE, [ "aiStatus",entity.getAIStatus()], None ):
				groupStateObj.onEnter(entity)
				return
	
	def tick( self, entity ):
		"""
		AI 循环
		"""
		tickID = entity.monsterAITickCallBackID
		if entity.isState( csdefine.ENTITY_STATE_FIGHT):
			if not self.checkIsInTerritory(  entity ):
			 	entity.changeState(csdefine.ENTITY_STATE_RESET)
			 	return
			entity.onViewRange()

		#如果在前面已经切换了状态，那么中断此tick
		if tickID != entity.monsterAITickCallBackID:
			return
		if self.getAIDataType() == "AIDatas1":
			AIFSM.AIFSM.tick( self,  entity )


AIFSM.AIFSM.setFSMClass( "AIFSMCommon", AIFSMCommon )
AIFSM.AIFSM.setFSMClass( "AIFSMExt1", AIFSMExt1 )
AIFSM.AIFSM.setFSMClass( "AIFSM_YCDMD_BOSS", AIFSM_YCDMD_BOSS )
AIFSM.AIFSM.setFSMClass( "AIFSMSoldier", AIFSMSoldier )
