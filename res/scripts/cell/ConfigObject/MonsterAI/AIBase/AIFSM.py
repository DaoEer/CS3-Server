# -*- coding: utf-8 -*-
import KBEDebug
import csdefine
from ConfigObject.MonsterAI.AIBase import AIEventBase
from ConfigObject.MonsterAI.AIBase import AIGroupState

class AIFSM:
	#状态机基础类
	_FSM_CLASS = {}
	@classmethod
	def setFSMClass( SELF, FSMType, FSMClass ):
		SELF._FSM_CLASS[ FSMType ] = FSMClass
	
	@classmethod
	def getFSMClass( SELF, FSMType, AIID ):
		return SELF._FSM_CLASS[ FSMType ]( AIID )
		
	@classmethod
	def isHasFSM(SELF,FSMType):
		if FSMType in SELF._FSM_CLASS:
			return True
		else:
			return False

	def __init__( self, AIID ):
		self._AIDataType = "AIDatas1"
		self._id = AIID
		self._groupIsStartTick = {}
		self._groupStates = {}
		self._eventToGroupStates = {} #为了提高效果，不用每次都进行状态循环验证是否切换，保存一个列表作为事件的响应
	
	def initData( self, FSMConfig, AIConfig ):
		#加载状态AI
		if 'AIDataType' in AIConfig:
			self._AIDataType = AIConfig["AIDataType"]
		for groupDatas in FSMConfig[ "groupStates" ]:
			groupID = groupDatas[ "groupID" ]
			tiggerEventType = int( groupDatas[ "tiggerEventType" ] )
			self._groupIsStartTick[groupID] = int( groupDatas[ "isStartTick" ] )
			groupStateDatas = AIConfig.get( groupID, None )
			self._groupStates[ groupID ] = AIGroupState.AIGroupState( groupID )
			self._groupStates[ groupID ].initData( groupDatas, groupStateDatas )

						
			#保存到事件触发列表
			if tiggerEventType not in self._eventToGroupStates:
				self._eventToGroupStates[ tiggerEventType ] = []
			self._eventToGroupStates[ tiggerEventType ].append( self._groupStates[ groupID ] )
		
		
	#--------------------------
	#外部获取配置的方法
	#--------------------------
	def getAIID( self ):
		return self._id
	
	def getAIDataType(self):
		"""
		"""
		return self._AIDataType

	def getCurrentGroupState( self, entity ):
		"""
		获取当前状态组
		"""
		return self._groupStates[ entity.monsterAIGetCurGroupState() ]

	def getCurrentGroupStateIsStartTick( self, entity ):
		"""
		获取当前状态组是否开启Tick
		"""
		return self._groupIsStartTick[ entity.monsterAIGetCurGroupState() ]
	
	#--------------------------
	#检查
	#--------------------------
	def checkIsInTerritory( self, entity  ):
		return entity.monsterAICheckInTerritory()
		
	#--------------------------
	#AI流程
	#--------------------------
	
	def startOnEnter(self, entity):
		"""
		"""
		for groupStateObj in self._groupStates.values():
			if  groupStateObj.isCanEnter( entity, csdefine.ENTITY_EVENT_ENTITY_STATE_CHANGE, [ entity.getState(), entity.getState() ], None ):
				groupStateObj.onEnter(entity)
				return

	def start( self, entity ):
		"""
		开始AI
		"""
		self.startOnEnter(entity)
		if entity.attackRange > 1 and entity.state != csdefine.ENTITY_STATE_PEAD and entity.state != csdefine.ENTITY_STATE_SHOW:	#如果主动攻击范围大于1才开启主动攻击陷阱
			entity.monsterAIAddAttackTrap() #开启主动陷阱

	def stop( self, entity ):
		"""
		结束AI
		"""
		self.getCurrentGroupState( entity ).onLeave( entity )
		if entity.attackRange > 1 :	#只有开启的主动攻击陷阱才需要关闭主动攻击陷阱
			entity.monsterAICancelAttackTrap() #关闭主动陷阱
	
	def changeGroupState( self, entity, oldGroupState, newGroupState ):
		"""
		改变组状态
		"""
		if newGroupState in self._groupStates:
			self._groupStates[ oldGroupState ].onLeave( entity )
			self._groupStates[ newGroupState ].onEnter( entity )
		else:
			KBEDebug.ERROR_MSG( "Monster( scriptID:%s, id:%d ) not groupState:%s!!"%( entity.scriptID, entity.id, newGroupState ) )
			
	def changeSubState( self, entity, oldSubState, newSubState ):
		"""
		切换子状态
		"""
		self._groupStates[ entity.monsterAIGetCurGroupState() ].changeSubState( entity, oldSubState, newSubState )
	
	def tick( self, entity ):
		"""
		AI 循环
		"""
		self.getCurrentGroupState( entity ).tick( entity )
	

	def _triggerCheck(self, entity, eventType, eventArgs, triggerEntity):
		"""
		"""
		if eventType in self._eventToGroupStates:
			for groupStateObj in self._eventToGroupStates[ eventType ]:
				if entity.monsterAIGetCurGroupState() != groupStateObj.getGroupStateID() and groupStateObj.isCanEnter( entity, eventType, eventArgs, triggerEntity ):
					self.changeGroupState( entity, entity.monsterAIGetCurGroupState(), groupStateObj.getGroupStateID() )
					return False
		return True


	def _onTrigger(self, entity, eventType, eventArgs, triggerEntity):
		"""
		"""
		self.getCurrentGroupState( entity ).trigger( entity, eventType, eventArgs, triggerEntity )

	def trigger( self, entity, eventType, eventArgs, triggerEntity ):
		"""
		触发事件AI
		"""
		if self._triggerCheck(entity, eventType, eventArgs, triggerEntity):
			self._onTrigger(entity, eventType, eventArgs, triggerEntity)
	