# -*- coding: utf-8 -*-

#engine
import KBEngine
import KBEDebug
#common
import csdefine
import csconst
from ConfigObject.Skill.Buff.BuffHold import BuffHold
#cell
import Functions


class BuffMountCarrier( BuffHold ):
	""""
	骑上载具
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self.modelid = ""
		self.scriptID = ""
		self.delyCreateTime = 0.0
		self._conflictPriority = csdefine.BUFF_CONFLICT_PRIORITY_FUC
		self.addConflictType(csdefine.BUFF_CONFLICT_TYPE_MODEL)

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self.modelid = dictDat["Param1"]
		self.scriptID = dictDat["Param2"]
		if dictDat["Param3"]:
			self.delyCreateTime = float( dictDat["Param3"] )

	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE: #此buff只给玩家加
			return False
		return BuffHold.addBuffCheck( self, caster, receiver )

	def onClientActorCreate( self, receiver, buffData, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		BuffHold.onClientActorCreate( self, receiver, buffData, srcEntityID )
		if srcEntityID == receiver.id:
			clientEntity = receiver.client
		else:
			playerEntity = KBEngine.entities.get( srcEntityID )
			if not playerEntity:
				return
			clientEntity = playerEntity.clientEntity( receiver.id )

		clientEntity.OnMountCarrier( self.modelid )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.disMountPet()		#变模型开始时，中断骑乘
		BuffHold.doBegin( self, receiver, buffData )
		casterEntity = KBEngine.entities.get( buffData.casterID, None )
		if casterEntity:
			receiver.changeDirection(casterEntity.direction, csdefine.REASON_CHANGE_DIR_FORCE)
			receiver.position = casterEntity.position
		receiver.allClients.OnMountCarrier( self.modelid )

	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.disMountPet()		#变模型开始时，中断骑乘
		BuffHold.doReload( self, receiver, buffData )
		casterEntity = KBEngine.entities.get( buffData.casterID, None )
		if casterEntity:
			receiver.changeDirection(casterEntity.direction, csdefine.REASON_CHANGE_DIR_FORCE)
			receiver.position = casterEntity.position
		receiver.allClients.OnMountCarrier( self.modelid )

	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData,reason )
		receiver.allClients.OnDisMountCarrier()
		if self.scriptID:
			spaceEntity = receiver.getCurrentSpace()
			pos = receiver.position
			dir = receiver.direction
			if not spaceEntity:
				return
			if self.delyCreateTime:
				spaceEntity.addTimerCallBack( self.delyCreateTime, "createEntityByScriptID", (self.scriptID, pos, dir, {}) )
			else:
				spaceEntity.createEntityByScriptID( self.scriptID,pos, dir, {} )

	def registerEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.registerEvent( self, receiver, buffData )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_INTERRUPT_BUFF_CHANGEMODEL, buffData.index )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_SPACE_CHANGE, buffData.index )

	def unRegisterEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.unRegisterEvent( self, receiver, buffData )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_INTERRUPT_BUFF_CHANGEMODEL, buffData.index )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_SPACE_CHANGE, buffData.index )

	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_INTERRUPT_BUFF_CHANGEMODEL:
			receiver.removeBuffByIndex( buffData.index )
			self.doInterrupt( receiver, buffData )

		BuffHold.triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict )